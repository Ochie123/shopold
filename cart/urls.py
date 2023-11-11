from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('count/', views.cart_count, name='cart_count'),
    path('items/', views.get_cart_items, name='get_cart_items'),
    
    path('add/<uuid:product_uuid>/', views.cart_add, name='cart_add'),
    path('remove/<uuid:product_uuid>/', views.cart_remove, name='cart_remove'),
]

