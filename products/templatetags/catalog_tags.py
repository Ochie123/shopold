from django import template
#from django.contrib.flatpages.models import FlatPage

from products.models import Product

register = template.Library()

@register.inclusion_tag("tags/product_list.html") 

def product_list(products, header_text):
    return { 'products': products,
            'header_text': header_text }


#@register.inclusion_tag("tags/footer.html") 
#def footer_links():
 #   flatpage_list = FlatPage.objects.all() 
 #   return {'flatpage_list': flatpage_list }
