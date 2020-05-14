from django.shortcuts import render, get_object_or_404
from product.models import Product
# Dont need this, this was just an example
from django.http import JsonResponse
# INSERT INTO product_product (name,color,price,"imgURL",description,discount)

from django.http import JsonResponse


# Create your views here.
# This gets rendered when http://127.0.0.1:8000/products is run, which is also the default
def __addToSearchHistory(search,request):
    try:
        request.session['searchHistory'][search] = search
        print(len(request.session['searchHistory']))
        print(request.session['searchHistory'])
    except KeyError:
        request.session['searchHistory'] = {}
        request.session['searchHistory'][search] = search
    request.session.modified = True

def index(request):
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        products = [ {
            'id': x.id,
            'name': x.name,
            'color': x.color,
            'price': x.price,
            'imgURL': x.imgURL,
            'description': x.description,
            'discount': x.discount
        } for x in Product.objects.filter(name__icontains=search_filter)]
        __addToSearchHistory(search_filter, request)
        return JsonResponse({'data': products})

    if 'color' in request.GET or 'price' in request.GET or 'brand' in request.GET or 'sort' in request.GET:
        query = Product.objects.all()
        if 'color' in request.GET:
            color_filter = request.GET['color']
            color_query = Product.objects.filter(color__icontains=color_filter)
            query = query & color_query
        if 'price' in request.GET:
            price_filter = request.GET['price']
            if price_filter == 'low':
                price_query = Product.objects.filter(price__gte=0, price__lte=100)
                query = query & price_query
            elif price_filter == 'mid':
                price_query = Product.objects.filter(price__gt=100, price__lte=500)
                query = query & price_query
            elif price_filter == 'max':
                price_query = Product.objects.filter(price__gt=500)
                query = query & price_query

        if 'brand' in request.GET:
            brand_filter = request.GET['brand']
            brand_query = Product.objects.filter(name__icontains=brand_filter)
            query = query & brand_query

        if 'sort' in request.GET:
            sort_filter = request.GET['sort']
            if sort_filter == "lowhigh":
                sort_query = Product.objects.order_by('price')
                query = query & sort_query
            elif sort_filter == "highlow":
                sort_query = Product.objects.order_by('-price')
                query = query & sort_query
            elif sort_filter == "az":
                sort_query = Product.objects.order_by('name')
                query = query & sort_query
            elif sort_filter == "za":
                sort_query = Product.objects.order_by('-name')
                query = query & sort_query

        products = [{
            'id': x.id,
            'name': x.name,
            'description': x.description,
            'imgURL': x.imgURL,
            'price': x.price
        } for x in query]
        return JsonResponse({'data': products})

    context = {'products': Product.objects.all()}
    return render(request, 'product/index.html', context)

# SUPPORTS -> /product/1
def getProductById(request, id):
    return render(request, 'product/product_details.html', {
        'product': get_object_or_404(Product, pk=id)
    })