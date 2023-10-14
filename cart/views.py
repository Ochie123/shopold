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
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        
        # Calculate the updated cart count
        cart_count = len(cart)  # Assuming the cart is an iterable
        
        # Return the cart count in the JSON response
        return JsonResponse({'message': 'Product added to cart successfully', 'cart_count': cart_count})
    else:
        return JsonResponse({'error': 'Invalid form data'}, status=400)
    


@require_POST
def cart_remove(request, product_uuid):
    cart = Cart(request)
    product = get_object_or_404(Product, uuid=product_uuid)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    return render(request, 'cart/new_detail.html', {'cart': cart})
