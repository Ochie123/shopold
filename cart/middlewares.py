from cart import models  # Import your Cart model

def cart_middleware(get_response):
    def middleware(request):
        if 'cart_id' in request.session:
            cart_id = request.session['cart_id']
            try:
                cart = models.Cart.objects.get(id=cart_id)
            except models.Cart.DoesNotExist:
                # If the cart doesn't exist, create a new one
                cart = models.Cart.objects.create()
                request.session['cart_id'] = cart.id  # Update the session with the new cart ID
        else:
            # If 'cart_id' is not in the session, create a new cart
            cart = models.Cart.objects.create()
            request.session['cart_id'] = cart.id  # Update the session with the new cart ID

        request.cart = cart  # Set the cart in the request

        response = get_response(request)
        return response

    return middleware
