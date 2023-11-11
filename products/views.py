import os
import logging
from django.contrib.auth import login, authenticate 
from django.contrib import messages
<<<<<<< HEAD
from django.views import View
=======

>>>>>>> 309766bdf0e7bfa8ea615d7bf18962f3fa438035
from django.db.models import Q
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.text import slugify
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import View
from django.utils.functional import LazyObject
from django.db.models import Count
from django.views.generic.edit import FormView 
from django.contrib.auth.mixins import (
     LoginRequiredMixin, 
     UserPassesTestMixin
)

from django.forms.models import modelform_factory 
from cart.forms import CartAddProductForm
from .forms import ProductFilterForm, SearchsForm
from .models import Product, Tag

from orders.models import Order
###NEW HOMEPAGE
from products import stats
#from shop.settings import PRODUCTS_PER_ROW

##Search
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from products import search

from products import forms

PAGE_SIZE = getattr(settings, "PAGE_SIZE", 21)
logger = logging.getLogger(__name__)
# Create your views here.
class LogoutView(FormView): 
    template_name = "logout.html" 

class SignupView(FormView): 
    template_name = "signup.html" 
    form_class = forms.UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/") 
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form) 
        form.save()

        email = form.cleaned_data.get("email") 
        raw_password = form.cleaned_data.get("password1") 
        logger.info(
            "New signup for email=%s through SignupView", email )
        user = authenticate(email=email, password=raw_password) 
        login(self.request, user)

        form.send_mail()
    
        messages.info(
        self.request, "You signed up successfully."
)
        return response

<<<<<<< HEAD

class LogoutView(FormView): 
    template_name = "registration/logged_out.html" 
=======
>>>>>>> 309766bdf0e7bfa8ea615d7bf18962f3fa438035

def tag(request, slug=None):
    tag = get_object_or_404(Tag, slug=slug)
    products = Product.objects.filter(tags__slug=slug)
    title = 'products tagged with "%s"' % tag

    paginator = Paginator(products, PAGE_SIZE)
    page_number = request.GET.get("page")
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, show first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, show last existing page.
        page = paginator.page(paginator.num_pages)

    bestseller_products = Product.published.all().filter(bestseller=1)
    toprated_products = Product.published.all().filter(toprated=1)
    return render(request, 'products/tag.html', {
                                                "products": page,
                                               
                                                "bestseller_products": bestseller_products,
                                                "toprated_products": toprated_products,
                                               'tag': tag,
                                                'title': title
                                             })


class ContactUsView(FormView):
    template_name = "products/support.html"
    form_class = forms.ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)
    
class ProductList(ListView):
    model = Product

def products(request):
    # get current search phrase
    q = request.GET.get('q', '')
    cart_product_form = CartAddProductForm()
    # get current page number. Set to 1 is missing or invalid 
    try:
        page = int(request.GET.get('page', 30)) 
    except ValueError:
        page = 1
    matching = search.products(q).get('products', []) 
    # generate the pagintor object
    paginator = Paginator(matching,settings.PRODUCTS_PER_PAGE)
    try:
        results = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        results = paginator.page(1).object_list
    # store the search
    search.store(request, q)
    # the usual...
    page_title = 'Search Results for: ' + q
    paginator = Paginator(results, PAGE_SIZE)
    page_number = request.GET.get("page")
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, show first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, show last existing page.
        page = paginator.page(paginator.num_pages)
    #paginator = Paginator(results, 1)
    #page = request.GET.get('page')
    
    results = paginator.get_page(page)
    #f = ProductFilter(request.GET, queryset=Product.objects.filter(results))
    bestseller_products = Product.published.all().filter(bestseller=1)
    toprated_products = Product.published.all().filter(toprated=1)
    #"products/search_results.html

    return render(request, "search/results.html", {
            "results": results,
        #'filter': f,
            'q': q,
             "bestseller_products": bestseller_products,
            "toprated_products": toprated_products,
            "results": page,
            'cart_product_form': cart_product_form ,
            })

def product_detail_modal(request, slug):

        product = get_object_or_404(Product, 
                                         slug=slug,
                                         )
<<<<<<< HEAD
                                         
=======
>>>>>>> 309766bdf0e7bfa8ea615d7bf18962f3fa438035
        cart_product_form = CartAddProductForm()
        stats.log_product_view(request, product)
        return render(request,
                  'products/product_detail_modal.html',
                  {'product': product,
                   'cart_product_form': cart_product_form ,
                  })

def product_detail(request, year, month, day, slug):

        product = get_object_or_404(Product, 
                                        publish__year=year, 
                                        publish__month=month, 
                                        publish__day=day,
                                         slug=slug,
                                         status=Product.Status.PUBLISHED,
        
                                         )
<<<<<<< HEAD
        
        # Get the previous and next products
        previous_product = Product.published.filter(publish__lt=product.publish).order_by('-publish').first()
        next_product = Product.published.filter(publish__gt=product.publish).order_by('publish').first()

        # Add logic to handle navigation to previous and next products
        if request.method == 'POST':
            if 'prev_product' in request.POST and previous_product:
                return redirect('product_detail', year=previous_product.publish.year, month=previous_product.publish.month, day=previous_product.publish.day, slug=previous_product.slug)
        elif 'next_product' in request.POST and next_product:
            return redirect('product_detail', year=next_product.publish.year, month=next_product.publish.month, day=next_product.publish.day, slug=next_product.slug)

=======
>>>>>>> 309766bdf0e7bfa8ea615d7bf18962f3fa438035
        cart_product_form = CartAddProductForm()
        stats.log_product_view(request, product)
        view_recs = stats.recommended_from_views(request)
        search_recs = stats.recommended_from_search(request)
        recently_viewed = stats.get_recently_viewed(request)

        bestseller_products = Product.published.all().filter(bestseller=1)
        toprated_products = Product.published.all().filter(toprated=1)

        product_tags_ids = product.tags.values_list('id', flat=True)
        similar_products = Product.published.filter(tags__in=product_tags_ids)\
                                  .exclude(pk=product.pk)
        similar_products = similar_products.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:5]
        
        return render(request,
                  'products/product_detail_new.html',
                  {'product': product,
                    'previous_product': previous_product, 
                    'next_product': next_product, 
                   'view_recs': view_recs,
                   'search_recs': search_recs,
                   'recently_viewed': recently_viewed,
                   'cart_product_form': cart_product_form ,
                    "bestseller_products": bestseller_products,
                    "toprated_products": toprated_products,
                    'similar_products': similar_products,
                  })

def product_list(request):
    qs = Product.published.all().order_by("-published")
    form = ProductFilterForm(data=request.GET)

    facets = {
        "selected": {},
        "categories": {
            "authors": form.fields["author"].queryset,
            "categories": form.fields["category"].queryset,
        },
    }

    if form.is_valid():
        filters = (
            # query parameter, filter parameter
            ("author", "author"),
            ("category", "categories"),
        )
        qs = filter_facets(facets, qs, form, filters)

    if settings.DEBUG:
        # Let's log the facets for review when debugging
        import logging

        logger = logging.getLogger(__name__)
        logger.info(facets)

    paginator = Paginator(qs, PAGE_SIZE)
    page_number = request.GET.get("page")
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, show first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, show last existing page.
        page = paginator.page(paginator.num_pages)

    context = {"form": form, "facets": facets, "object_list": page}
    return render(request, "products/product_list.html", context)






def filter_facets(facets, qs, form, filters):
    for query_param, filter_param in filters:
        value = form.cleaned_data[query_param]
        if value:
            selected_value = value

            facets["selected"][query_param] = selected_value
            filter_args = {filter_param: value}
            qs = qs.filter(**filter_args).distinct()
    return qs


def product_toprated(request):
    toprated_products = Product.published.filter(toprated=1).order_by("-publish")
  
    #product_filter = RangeFilter(request.GET)

    return render(request, 
                'homepage/toprated.html',
                {'toprated_products': toprated_products}
                )

def product_bestseller(request):
    bestseller_products = Product.published.filter(bestseller=1).order_by("-publish")
  
    #product_filter = RangeFilter(request.GET)

    return render(request, 
                'homepage/bestdeals.html',
                {'bestseller_products': bestseller_products})

def product_toprated(request):
    toprated_products = Product.published.all().filter(toprated=1).order_by("-publish")
  
    #product_filter = RangeFilter(request.GET)

    return render(request, 
                'homepage/toprated.html',
                {'toprated_products': toprated_products}
                )

from django.http import JsonResponse
from django.template.loader import render_to_string

def index(request):
    """ site home page """
    sort_param = request.GET.get("sort")
    if sort_param == "oldest":
        qs = Product.published.all().order_by("publish")
    elif sort_param == "":
        qs = Product.published.all().order_by("-popularity")
    elif sort_param == "":
        qs = Product.published.all().order_by("-rating")
    else:
        qs = Product.published.all().order_by("-publish")
    form = ProductFilterForm(data=request.GET)
    cart_product_form = CartAddProductForm()
    products, facets = get_queryset_and_facets(form, request)
    # Paginate the products
    paginator = Paginator(products, PAGE_SIZE)
    page_number = request.GET.get("page")
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    # Get other data
    search_recs = stats.recommended_from_search(request)
    bestseller_products = Product.published.all().filter(bestseller=1)
    toprated_products = Product.published.all().filter(toprated=1)
    recently_viewed = stats.get_recently_viewed(request)
    view_recs = stats.recommended_from_views(request)
    page_title = 'SVG Craft - Home to svgs'
    
    # AJAX search functionality
    url_parameter = request.GET.get("q")
    if url_parameter:
        products = Product.objects.filter(title__icontains=url_parameter)
    else:
        products = Product.objects.all()
    
    # Check if the request is AJAX
    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"
    if is_ajax_request:
        html = render_to_string(
            template_name="catalog/products-partial.html",
            context={"products": products}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(
        request,
        "catalog/index.html",
        {
            "page_title": page_title,
            "products": page,
            "form": form,
            "cart_product_form": cart_product_form,
            "facets": facets,
            "search_recs": search_recs,
            "bestseller_products": bestseller_products,
            "toprated_products": toprated_products,
            "recently_viewed": recently_viewed,
            "view_recs": view_recs,
        },
    )

def get_queryset_and_facets(form, request):
    sort_param = request.GET.get("sort")
    if sort_param == "oldest":
        qs = Product.published.all().order_by("publish")
    elif sort_param == "":
        qs = Product.published.all().order_by("-popularity")
    elif sort_param == "":
        qs = Product.published.all().order_by("-rating")
    else:
        qs = Product.published.all().order_by("-publish")

    categories = form.fields["category"].queryset.annotate(
        product_count=Count("category_products")
    )
    facets = {
        "selected": {},
        "categories": {
            "categories": form.fields["category"].queryset,
        },
    }
    if form.is_valid():
        filters = [("category", "categories")]
        qs = filter_facets(facets, qs, form, filters)
    return qs, facets

def filter_facets(facets, qs, form, filters):
    for query_param, filter_param in filters:
        value = form.cleaned_data[query_param]
        if value:
            selected_value = value
            facets["selected"][query_param] = selected_value
            filter_args = {filter_param: value}
            qs = qs.filter(**filter_args).distinct()
    return qs


<<<<<<< HEAD
def download_product_file(request, pk):
    product = get_object_or_404(Product, pk=pk)
=======
def download_product_file(request, pk, slug):
    product = get_object_or_404(Product, uuid=pk, slug=slug)
>>>>>>> 309766bdf0e7bfa8ea615d7bf18962f3fa438035
    
    if product.file:
        # Extract filename and extension from the FieldFile's name
        filename = os.path.basename(product.file.name)
        base_filename, extension = os.path.splitext(filename)
        extension = extension[1:]  # remove the dot
        
        response = FileResponse(
            product.file, content_type=f"application/zip"
        )
        slug = slugify(product.title)[:100]
        response["Content-Disposition"] = (
            "attachment; filename="
            f"{slug}.{extension}"
        )
    else:
        response = HttpResponseNotFound(
            content="File unavailable"
        )
    
    return response
<<<<<<< HEAD
class MyOrderView(LoginRequiredMixin, View):
    login_url = '/login/'  # Set the login URL

    def get(self, request):
        email = request.user
        orders = Order.objects.filter(email=email)
        ordered_products = []

        for order in orders:
            ordered_product = Order.objects.filter(id=order.id)
            ordered_products.append(ordered_product)

        return render(request, 'my_order.html', {'data': zip(ordered_products, orders)})

from django.http import Http404, FileResponse
from django.shortcuts import get_object_or_404
from .models import Product


def download_free_product(request, random_url):
    product = get_object_or_404(Product, download_url=random_url)

    if product.file:
        # Extract filename and extension from the FieldFile's name
        filename = product.file.name.split('/')[-1]
        base_filename, extension = filename.split(".")

        response = FileResponse(product.file, content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{base_filename}.{extension}"'
        return response

    raise Http404("The requested product is not available for download.")
=======
>>>>>>> 309766bdf0e7bfa8ea615d7bf18962f3fa438035
