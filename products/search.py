from .models import SearchTerm 
from products import stats
from products.models import Product 
from django.db.models import Q

STRIP_WORDS = ['a','an','and','by','for','from','in','no','not', 'of','on','or','that','the','to','with']
# store the search text in the database 
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def store(request, q):
    # If the search term is at least three characters long, store it in the database
    if len(q) > 3:
        term = SearchTerm()
        term.q = q
        
        # Use get_client_ip to obtain the client's IP address
        term.ip_address = get_client_ip(request)
        
        term.tracking_id = stats.tracking_id(request)
        term.user = None
        if request.user.is_authenticated:
            term.user = request.user
        
        term.save()



    
# get products matching the search text 
def products(search_text):
    words = _prepare_words(search_text)
    products = Product.published.all() 
    results = {}
    results['products'] = []
# iterate through keywords 
    for word in words:
        products = products.filter(Q(title__icontains=word) |
       # Q(overview__icontains=word) | Q(sku__iexact=word) | 
       # Q(brand__icontains=word) | 
        Q(description__icontains=word) )
        #Q(meta_keywords__icontains=word)) 
        results['products'] = products
    return results

# strip out common words, limit to 5 words 
def _prepare_words(search_text):
    words = search_text.split() 
    for common in STRIP_WORDS:
        if common in words: 
            words.remove(common)
    return words[0:5]