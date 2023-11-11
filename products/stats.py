import requests  # Import the requests library
from products.models import SearchTerm
from products.models import Product
from products.models import ProductView
from . models import ProductView
#from shop.settings import PRODUCTS_PER_ROW

import os
import base64

def tracking_id(request): 
    try:
        return request.session['tracking_id'] 
    except KeyError:
        request.session['tracking_id'] = base64.b64encode(os.urandom(36)).decode('ascii') 
        return request.session['tracking_id']


def recommended_from_search(request):
# get the common words from the stored searches 
    common_words = frequent_search_words(request) 
    from products import search
    matching = []
    for word in common_words:
        results = search.products(word).get('products',[]) 
        for r in results:
            #if len(matching) < PRODUCTS_PER_ROW and not r in matching:
                matching.append(r)
    return matching

def frequent_search_words(request):
# get the ten most recent searches from the database. 
    searches = SearchTerm.objects.filter(tracking_id=tracking_id(request)).values('q').order_by('-search_date')[0:10] 
# join all of the searches together into a single string. 
    search_string = ''.join([search['q'] for search in searches])
# return the top three most common words in the searches
    return sort_words_by_frequency(search_string)[0:3]

def sort_words_by_frequency(some_string):
# convert the string to a python list
    words = some_string.split()
# assign a rank to each word based on frequency
    ranked_words = [[word, words.count(word)] for word in set(words)] 
# sort the words based on descending frequency
    sorted_words = sorted(ranked_words, key = lambda word: -word[1]) 
    # return the list of words, most frequent first
    return [p[0] for p in sorted_words]

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location_from_ip(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        data = response.json()
        city = data.get("city", "")
        country = data.get("country", "")
        return f"{city}, {country}"
    except Exception as e:
        return "Location information not available"

def log_product_view(request, product):
    t_id = tracking_id(request)
    try:
        v = ProductView.objects.get(tracking_id=t_id, product=product)
        v.save()
    except ProductView.DoesNotExist:
        v = ProductView()
        v.product = product
        v.user = None
        v.ip_address = get_client_ip(request)
        v.tracking_id = t_id

        # Fetch and store the location information
        v.location = get_location_from_ip(v.ip_address)

        v.save()




def recommended_from_views(request):
###get product recommendations based on products that the customer has viewed;
##gets list of tracking IDs of other customers who have viewed the products in the current customer's 
##viewed products, and gets products that these other customers also viewed.
    t_id = tracking_id(request)
# get recently viewed products
    viewed = get_recently_viewed(request)
# if there are previously viewed products, get other tracking ids that have 
# # viewed those products also
    if viewed:
        productviews = ProductView.objects.filter(product__in=viewed).values('tracking_id')
        t_ids = [v['tracking_id'] for v in productviews]
# if there are other tracking ids, get other products. 
        if t_ids:
            all_viewed = Product.objects.filter(productview__tracking_id__in=t_ids) 
# if there are other products, get them, excluding the
# products that the customer has already viewed.
            if all_viewed:
                other_viewed = ProductView.objects.filter(product__in= all_viewed).exclude(product__in=viewed)
                if other_viewed:
                    return Product.objects.filter(productview__in=other_viewed).distinct()

def get_recently_viewed(request):
    t_id = tracking_id(request)
    views = ProductView.objects.filter(tracking_id=t_id).values('product_id').order_by('-date')
    product_ids = [v['product_id'] for v in views] 
    return Product.objects.filter(uuid__in=product_ids)


    #published.all()