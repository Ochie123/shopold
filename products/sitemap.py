from categories.models import Category 
from products.models import Product
from django.contrib.sitemaps import Sitemap

class ProductSitemap(Sitemap):
    def items(self):
        return Product.published.all()

class CategorySitemap(Sitemap): 
    def items(self):
        return Category.objects.all()

SITEMAPS = {'categories': CategorySitemap, 
            'products': ProductSitemap}