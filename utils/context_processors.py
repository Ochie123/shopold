from categories.models import Category 
from products.models import Product

from shop import settings

def utils(request): 
    return {
            'categories': Category(request),
            'products': Product(request),
           
            'request': request }

def categories(request): 
    return {
        'categories': Category.objects.all(),
        'products': Product.objects.all(),
    }