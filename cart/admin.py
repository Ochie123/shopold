from django.contrib import admin
from .models import Cart, CartLine
from cart import models
# Register your models here.
class CartLineInline(admin.TabularInline):
    model = models.CartLine
    raw_id_fields = ("product",)

class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "count")
    list_editable = ("status",)
    list_filter = ("status",)
    inlines = (CartLineInline,)

admin.site.register(Cart, CartAdmin)