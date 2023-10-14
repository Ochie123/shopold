# products/models.py
import os
import uuid
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.db import models
from django.utils.timezone import now as timezone_now
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField 

from ordered_model.models import OrderedModel

#class ActiveProductManager(models.Manager): 
   # def get_query_set(self):
     #   return super(ActiveProductManager, self).get_query_set().filter(is_active=True)



class Tag(models.Model):
    title = models.CharField(max_length=255, default='') 
    slug = models.SlugField(default='', blank=True)

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.title) 
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s' % self.title
    
    def get_absolute_url(self):
        return reverse('tag', args=[str(self.slug)])

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=Product.Status.PUBLISHED)


class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    uuid = models.UUIDField(primary_key=True, default=None, editable=False)
    categories = models.ManyToManyField( "categories.Category", 
                            verbose_name=_("Categories"),
                            
                            related_name="category_products",
                        )
    
    tags = models.ManyToManyField(Tag,related_name="tag_products", blank=True)
    toprated = models.BooleanField(default=False, help_text="1=toprated")
    bestseller = models.BooleanField(default=False, help_text="1=bestseller")
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, unique_for_date='publish')
    file = models.FileField(upload_to='files', blank=True, null=True)

    description = RichTextUploadingField(_("description"), blank=True)
    price = models.DecimalField(
        _("price ($)"), max_digits=8, decimal_places=2, blank=True, null=True
    )
    is_active = models.BooleanField(default=True) 

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
           


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('products:product_detail',
                       args=[self.publish.year, 
                             self.publish.month,
                             self.publish.day,
                             self.slug,
                             #self.uuid,
                             ])
    

    def get_url_path(self):
        return reverse("products:product_detail_modal", kwargs={"slug": self.slug, 
                                                                #"pk":self.uuid
                                                                })

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
    