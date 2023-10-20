from django.urls import path

from . import views
#from .views import ( ProductListView)


urlpatterns = [
   path('', views.index, name='index'),
   path('category/', views.index, name='category_filter'),
   # path("", ProductListView.as_view(), name="product_list"),
  # path(
    #    "support/",
    #    views.ContactUsView.as_view(),
     #   name="contact_us",
   # ),
    path('my-order/', views.my_order_view,name='my_order'),
    path('toprated/', views.product_toprated, name='product_toprated'),
     path('bestseller/', views.product_bestseller, name='product_bestseller'),
    path('tags/<slug:slug>/', views.tag, name='tag'),
    #path('<slug:slug>/<uuid:pk>', views.product_detail_modal,name='product_detail_modal'),
    path('<slug:slug>/', views.product_detail_modal,name='product_detail_modal'),
    #path('<int:year>/<int:month>/<int:day>/<slug:slug>/<uuid:pk>', views.product_detail,name='product_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.product_detail,name='product_detail'),
   path(
    "<uuid:pk>/download-file/",
    views.download_product_file,
    name='download_product_file'
),
    path('download/<str:random_url>/', views.download_free_product, name='download_free_product'),
    path('search/', views.products, name="search_products"),

   # path('search/', views.index_view, name="index_view"),
   
    
   # path('<slug:slug>/', ProductDetail.as_view(), name="product-detail"),
]
