from django.urls import path

from . import views
from .views import ( 
               ProductListView,
               
    
)


urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path('<uuid:pk>/', views.product_detail_modal,name='product_detail_modal'),
    path('<uuid:pk>/<slug:slug>/', views.product_detail,name='product_detail'),
    path('search/', views.products, name="search_products"),
    
   # path('<slug:slug>/', ProductDetail.as_view(), name="product-detail"),
]
