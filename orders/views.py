from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site

from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

from .models import Order, OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart


    
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from decimal import Decimal
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id) # set the order in the session 
            request.session['order_id'] = order.id
            # redirect to the payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/order/new_create.html', {'cart': cart, 'form': form,})


def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
        # Add product download URLs to the context

        # Get the current site's domain (you need to have the 'sites' app configured)
    current_site = get_current_site(request)
    domain = current_site.domain


    # Add product download URLs to the context with the full URL
    product_download_urls = [f'http://{domain}/product/download/{item.product.download_url}' for item in order.items.all()]
    context = {
        'order': order,
        'product_download_urls': product_download_urls,
    }

    html = render_to_string('orders/order/pdf.html', context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response

#nXg2GNuSoVgGClgoklz5 http://127.0.0.1:8000/product/download/nXg2GNuSoVgGClgoklz5