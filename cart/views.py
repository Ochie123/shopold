from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm



@require_POST
def cart_add(request, product_uuid):
    cart = Cart(request)
    product = get_object_or_404(Product, uuid=product_uuid)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    override = request.POST.get('override', False)

    cart.add(product=product, quantity=quantity, override_quantity=override)

    # Calculate the updated cart count
    cart_count = len(cart)

    # Return the cart count and a message in the JSON response
    response_data = {
        'message': 'Product added to cart successfully',
        'cart_count': cart_count
    }
    return JsonResponse(response_data)


def cart_count(request):
    cart = Cart(request)
    cart_count = len(cart)
    response_data = {'cart_count': cart_count}
    return JsonResponse(response_data)

def get_cart_items(request):
    cart = Cart(request)
    cart_items = []

    try:
        for item in cart:
            product = item.get('product')
            if product:
                cart_items.append({
                    #'uuid': product.uuid,
                    'title': product.title,
                    'quantity': item.get('quantity'),
                    'price': product.price,
                    'image_url': product.productimage_set.first().image.url
                })
    except (AttributeError, KeyError):
        return JsonResponse({'error': 'Invalid cart data'})

    total_price = cart.get_total_price()

    return JsonResponse({'cart_items': cart_items, 'total_price': total_price})


@require_POST
def cart_remove(request, product_uuid):
    cart = Cart(request)
    product = get_object_or_404(Product, uuid=product_uuid)
    cart.remove(product)
    cart_count = len(cart)  # Calculate the updated cart count
    response_data = {'message': 'Product removed from the cart', 'cart_count': cart_count}
    return JsonResponse(response_data)


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    return render(request, 'cart/new_detail.html', {'cart': cart})
