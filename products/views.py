from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import View
from django.utils.functional import LazyObject

from cart.forms import CartAddProductForm
from .forms import ProductFilterForm
from .models import Product, Tag

###NEW HOMEPAGE
from products import stats
#from shop.settings import PRODUCTS_PER_ROW

##Search
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from products import search

PAGE_SIZE = getattr(settings, "PAGE_SIZE", 3)
# Create your views here.

def tag(request, slug=None):
    tag = get_object_or_404(Tag, slug=slug)
    products = Product.objects.filter(tags__slug=slug)
    title = 'products tagged with "%s"' % tag
    return render(request, 'products/tag.html', {'products': products,
                                             'tag': tag,
                                             'title': title
                                             })

class ProductList(ListView):
    model = Product

def products(request):
    # get current search phrase
    q = request.GET.get('q', '')
    # get current page number. Set to 1 is missing or invalid 
    try:
        page = int(request.GET.get('page', 1)) 
    except ValueError:
        page = 1
# retrieve the matching products
    #f = ProductFilter( matching = search.products(q).get('products', []) ))
    #f = ProductFilter(request.GET, queryset=Product.objects.all())

    #f = ProductFilter(request.GET, queryset=Product.objects.filter('q', ''))

    #f = ProductFilter(request.GET, queryset=Product.objects.filter(bestdeals=1))
    #f = ProductFilter(request.GET.get('q', ''))

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

    paginator = Paginator(results, 4)
    page = request.GET.get('page')
    
    results = paginator.get_page(page)
    #f = ProductFilter(request.GET, queryset=Product.objects.filter(results))
    bestseller_products = Product.objects.filter(bestseller=1)
    toprated_products = Product.objects.filter(toprated=1)

    return render(request, "search/results.html", {
        "results": results,
        #'filter': f,
            'q': q,
             "bestseller_products": bestseller_products,
            "toprated_products": toprated_products,
            })

def product_detail_modal(request, pk):

        product = get_object_or_404(Product, 
                                         uuid=pk,
                                         )
        stats.log_product_view(request, product)
        return render(request,
                  'products/product_detail_modal.html',
                  {'product': product,
                  })

def product_detail(request, pk, slug):

        product = get_object_or_404(Product, 
                                        uuid=pk,
                                         slug=slug,
        
                                         )
        
        cart_product_form = CartAddProductForm()
        stats.log_product_view(request, product)
        view_recs = stats.recommended_from_views(request)
        search_recs = stats.recommended_from_search(request)
        recently_viewed = stats.get_recently_viewed(request)

        bestseller_products = Product.objects.filter(bestseller=1)
        toprated_products = Product.objects.filter(toprated=1)

        return render(request,
                  'products/product_detail.html',
                  {'product': product,
                   'view_recs': view_recs,
                   'search_recs': search_recs,
                   'recently_viewed': recently_viewed,
                   'cart_product_form': cart_product_form ,
                    "bestseller_products": bestseller_products,
                    "toprated_products": toprated_products,
                  })

def product_list(request):
    qs = Product.objects.order_by("title")
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

def product_toprated(request):
    toprated_products = Product.objects.filter(toprated=1)
  
    #product_filter = RangeFilter(request.GET)

    return render(request, 
                'homepage/toprated.html',
                {'toprated_products': toprated_products}
                )




def filter_facets(facets, qs, form, filters):
    for query_param, filter_param in filters:
        value = form.cleaned_data[query_param]
        if value:
            selected_value = value

            facets["selected"][query_param] = selected_value
            filter_args = {filter_param: value}
            qs = qs.filter(**filter_args).distinct()
    return qs


#class ProductListView(View):
    form_class = ProductFilterForm
    template_name = "products/product_lists.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(data=request.GET)
        qs, facets = self.get_queryset_and_facets(form)
        page = self.get_page(request, qs)
        context = {"form": form, "facets": facets, "object_list": page}
        return render(request, self.template_name, context)

    def get_queryset_and_facets(self, form):
        qs = Product.objects.order_by("title")
        facets = {
            "selected": {},
            "categories": {
               
                "categories": form.fields["category"].queryset,
    
            },
        }
        if form.is_valid():
            filters = (
                # query parameter, filter parameter
             
                ("category", "categories"),
    
            )
            qs = self.filter_facets(facets, qs, form, filters)
        return qs, facets

    @staticmethod
    def filter_facets(facets, qs, form, filters):
        for query_param, filter_param in filters:
            value = form.cleaned_data[query_param]
            if value:
                selected_value = value
    
                facets["selected"][query_param] = selected_value
                filter_args = {filter_param: value}
                qs = qs.filter(**filter_args).distinct()
        return qs

    def get_page(self, request, qs):
        paginator = Paginator(qs, PAGE_SIZE)
        page_number = request.GET.get("page")
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
   #     return page

###search

def product_toprated(request):
    toprated_products = Product.objects.filter(toprated=1)
  
    #product_filter = RangeFilter(request.GET)

    return render(request, 
                'homepage/toprated.html',
                {'toprated_products': toprated_products}
                )

def product_bestseller(request):
    bestseller_products = Product.objects.filter(bestseller=1)
  
    #product_filter = RangeFilter(request.GET)

    return render(request, 
                'homepage/bestdeals.html',
                {'bestseller_products': bestseller_products})
def index(request):
    """ site home page """
    # Create the filter form and apply any filtering if necessary
    form = ProductFilterForm(data=request.GET)
    products, facets = get_queryset_and_facets(form)

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
    bestseller_products = Product.objects.filter(bestseller=1)
    toprated_products = Product.objects.filter(toprated=1)
    recently_viewed = stats.get_recently_viewed(request)
    view_recs = stats.recommended_from_views(request)
    page_title = 'SVGhippo - Home to svgs'

    return render(
        request,
        "catalog/index.html",
        {
            "page_title": page_title,
            "products": page,
            "form": form,
            "facets": facets,
            "search_recs": search_recs,
            "bestseller_products": bestseller_products,
            "toprated_products": toprated_products,
            "recently_viewed": recently_viewed,
            "view_recs": view_recs,
        },
    )

def get_queryset_and_facets(form):
    qs = Product.objects.order_by("title")
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