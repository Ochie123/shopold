from categories.models import Category 
from products.models import Product

from shop import settings

def utils(request): 
    categories = Category.objects.all()
    products = Product.objects.all()
    return {
            'categories': categories,
            'products': products,
            'categories': Category(request),
            'products': Product(request),
           
            'request': request }

def categories(request): 
    return {
        'categories': Category.objects.all(),
        'products': Product.objects.all(),
    }