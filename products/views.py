import os
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
from cart.forms import CartAddProductForm
from .forms import ProductFilterForm, SearchsForm
from .models import Product, Tag

###NEW HOMEPAGE
from products import stats
#from shop.settings import PRODUCTS_PER_ROW

##Search
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from products import search

PAGE_SIZE = getattr(settings, "PAGE_SIZE", 30)
# Create your views here.

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

def product_detail_modal(request, pk):

        product = get_object_or_404(Product, 
                                         uuid=pk,
                                         )
        cart_product_form = CartAddProductForm()
        stats.log_product_view(request, product)
        return render(request,
                  'products/product_detail_modal.html',
                  {'product': product,
                   'cart_product_form': cart_product_form ,
                  })

def product_detail(request, pk, slug):

        product = get_object_or_404(Product, 
                                        uuid=pk,
                                         slug=slug,
                                         status=Product.Status.PUBLISHED,
        
                                         )
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
                  'products/product_detail.html',
                  {'product': product,
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

def index(request):
    """ site home page """
    # Create the filter form and apply any filtering if necessary
    # Get the sort parameter from the query strin

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
    page_title = 'SVGhippo - Home to svgs'

    return render(
        request,
        "catalog/index.html",
        {
            "page_title": page_title,
            "products": page,
            "form": form,
            'cart_product_form': cart_product_form ,
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


def download_product_file(request, pk, slug):
    product = get_object_or_404(Product, uuid=pk, slug=slug)
    
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

def search_page(request): 
    search_form = SearchsForm() 
    products = [] 
    show_results = False
    if 'query' in request.GET: 
        show_results = True
        query = request.GET['query'].strip() 
        if query:
            keywords = query.split() 
            q = Q()
            for keyword in keywords:
                q = q & Q(title__icontains=keyword)
            search_form = SearchsForm({'query' : query}) 
            products = Product.objects.filter(q)[:10]
    context = { 
        'search_form': search_form,
        'products': products, 
        'show_results': show_results, 
}

    if 'ajax' in request.GET:
        return render(request, 'bookmark_list.html', context)
    else:
        return render(request, 'search.html', context)



def indexs(request):
    """ site home page """
    # Create the filter form and apply any filtering if necessary
    search_form = SearchsForm() 
    products = [] 
    form = ProductFilterForm(data=request.GET)
    products, facets = get_queryset_and_facets(form)

    # Paginate the products
    paginator = Paginator(products, PAGE_SIZE)
    page_number = request.GET.get("page")
    show_results = False
    if 'query' in request.GET: 
        show_results = True
        query = request.GET['query'].strip() 
        if query:
            keywords = query.split() 
            q = Q()
            for keyword in keywords:
                q = q & Q(title__icontains=keyword)
            search_form = SearchsForm({'query' : query}) 
            products = Product.objects.filter(q)[:10]
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
 
    if 'ajax' in request.GET:
        return render(request, 'bookmark_list.html',  {           
            "page_title": page_title,
            "products": page,
            'search_form': search_form,
            "form": form,
            "facets": facets,
            "search_recs": search_recs,
            "bestseller_products": bestseller_products,
            "toprated_products": toprated_products,
            "recently_viewed": recently_viewed,
            "view_recs": view_recs,
            'search_form': search_form,
        'products': products, 
        'show_results': show_results},)
    else:
        return render(request,  "catalog/index.html", {          
            "page_title": page_title,
            "products": page,
            'search_form': search_form,
            "form": form,
            "facets": facets,
            "search_recs": search_recs,
            "bestseller_products": bestseller_products,
            "toprated_products": toprated_products,
            "recently_viewed": recently_viewed,
            "view_recs": view_recs,
            'search_form': search_form,
        'products': products, 
        'show_results': show_results
            }, )