"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from categories.models import Category 
from products import views
from django.contrib.sitemaps import GenericSitemap # new
from django.contrib.sitemaps.views import sitemap

from products.models import Product # new

from products import forms

info_dict = {
    'queryset': Category.objects.all(),
    'queryset': Product.objects.all(),
}

urlpatterns = [
    path("ad-ui/", admin.site.urls),
       path(
        "support/",
        views.ContactUsView.as_view(),
        name="contact_us",
    ),
    path(
        'signup/', 
        views.SignupView.as_view(), name="signup"),
    path(
        "login/", auth_views.LoginView.as_view( template_name="login.html",
        form_class=forms.AuthenticationForm, ),
        name="login",
), 

   path('logout/', auth_views.LogoutView.as_view( template_name="registration/logged_out.html"), name='logout'),

   

    path('my-order/', views.MyOrderView.as_view(), name='my_order'),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    #path('search/', views.products, name="search_products"),
    #path('search/', views.index_view, name="index_view"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('', views.index, name='index'),
    path('category/', views.index, name='category_filter'),
    #
    #path("", views.product_list, name="product_list"),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('product/', include(("products.urls", "products"), namespace="products")),

 
    path('sitemap.xml', sitemap, # new
        {'sitemaps': {'categories': GenericSitemap(info_dict, priority=0.6)}},
        name='django.contrib.sitemaps.views.sitemap'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

