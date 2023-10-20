from django import template
from products.models import Product 

register = template.Library()

@register.inclusion_tag('tags/footerp.html', takes_context=True)

def display_bestsellers(context):
    bestseller_products = Product.published.all().filter(bestseller=1)
    toprated_products = Product.published.all().filter(toprated=1)
    products = Product.published.all().order_by("-publish")
   

    return {
        'bestseller_products': bestseller_products,
        'toprated_products': toprated_products,
        'products': products,
   
    }
