# products/models.py
import os
import uuid
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.db import models
from django.utils.timezone import now as timezone_now
from django.utils.translation import gettext_lazy as _

from ordered_model.models import OrderedModel

class ActiveProductManager(models.Manager): 
    def get_query_set(self):
        return super(ActiveProductManager, self).get_query_set().filter(is_active=True)


class FeaturedProductManager(models.Manager): 
    def all(self):
        return super(FeaturedProductManager, self).all() .filter(is_active=True).filter(featured=True)

class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, default=None, editable=False)
    categories = models.ManyToManyField( "categories.Category", 
                            verbose_name=_("Categories"),
                            
                            related_name="category_products",
                        )
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200)
    description = models.TextField(_("description"), blank=True)
    price = models.DecimalField(
        _("price ($)"), max_digits=8, decimal_places=2, blank=True, null=True
    )
    is_active = models.BooleanField(default=True) 

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    objects = models.Manager() 
    active = ActiveProductManager()               


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('products:product_detail',
                       args=[self.uuid, self.slug])
    

    def get_url_path(self):
        return reverse("products:product_detail_modal", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.pk = uuid.uuid4()
        super().save(*args, **kwargs)

class ProductImage(OrderedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(_("image"), upload_to="product-images")
    thumbnail = models.ImageField( upload_to="product-thumbnails", null=True)

    order_with_respect_to = "product"

    class Meta(OrderedModel.Meta):
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.image.name

class SearchTerm(models.Model):
    q = models.CharField(max_length=200)
    tracking_id = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True) 
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    def __unicode__(self): 
        return self.q

    def __str__(self):
        return self.q
    
class PageView(models.Model): 
    ##model class for tracking the pages that a customer views """
    class Meta:
        abstract = True
    
    date = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=255, db_index=True)
    
class ProductView(PageView):
    ##""" tracks product pages that customer views """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.tracking_id
    