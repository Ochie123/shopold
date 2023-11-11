from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from products.models import Product
from cart import models
from .cart import Cart
from .forms import CartAddProductForm



@require_POST
def cart_add(request, product_uuid):
    cart = request.cart  # Retrieve the cart from the request
    product = get_object_or_404(Product, uuid=product_uuid)
<<<<<<< HEAD

    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    override = request.POST.get('override', False)

    # Create a new cart line
    if not request.cart:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        cart = models.Cart.objects.create(user=user)
        request.session["cart_id"] = cart.id
    cartline, created = models.CartLine.objects.get_or_create(cart=cart, product=product)
    if not created:
        cartline.quantity += 1
        cartline.save()
    if override:
        cartline.quantity = quantity
    else:
        cartline.quantity += quantity
    cartline.save()

    # Calculate the updated cart count using the count() method
    cart_count = cart.count()
    #cart_count = len(request.cart)

    # Return the cart count and a message in the JSON response
    response_data = {
        'message': 'Product added to cart successfully',
        'cart_count': cart_count
    }
    return JsonResponse(response_data)


def cart_count(request):
    cart = request.cart   # Create an instance of the Cart model
    cart_count = cart.count()  # Call the count method on the instance
    response_data = {'cart_count': cart_count}
    return JsonResponse(response_data)


def get_cart_items(request):
    cart = request.cart
    cart_items = []

    try:
        for cartline in cart.cartline_set.all():  # Iterate through cart lines
            product = cartline.product
            if product:
                cart_items.append({
                    'product_uuid': product.uuid,
                    'title': product.title,
                    'quantity': cartline.quantity,
                    'price': product.price,
                    'image_url': product.productimage_set.first().image.url
                })
    except (AttributeError, KeyError):
        return JsonResponse({'error': 'Invalid cart data'})

   # total_price = cart.get_total_price()

    return JsonResponse({'cart_items': cart_items,})
=======
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
    
>>>>>>> 309766bdf0e7bfa8ea615d7bf18962f3fa438035


@require_POST
def cart_remove(request, product_uuid):
    cart = request.cart 
    product = get_object_or_404(Product, uuid=product_uuid)
    cart.remove(product)
    cart_count = cart.count() # Calculate the updated cart count
    response_data = {'message': 'Product removed from the cart', 'cart_count': cart_count}
    return JsonResponse(response_data)


def cart_detail(request):
<<<<<<< HEAD
    cart = request.cart
    cart_count = cart.count()
    cart_lines = cart.cartline_set.all()  # Retrieve cart lines
    for cartline in cart_lines:
        cartline.update_quantity_form = CartAddProductForm(initial={
            'quantity': cartline.quantity,
            'override': True
        })
    return render(request, 'cart/new_detail.html', {'cart': cart, 'cart_count': cart_count, 'cart_lines': cart_lines})
=======
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    return render(request, 'cart/new_detail.html', {'cart': cart})
>>>>>>> 309766bdf0e7bfa8ea615d7bf18962f3fa438035
