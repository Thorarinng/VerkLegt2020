from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product, ProductImage
# Dont need this, this was just an example
from django.http import JsonResponse
# INSERT INTO product_product (name,color,price,"imgURL",description,discount)
import datetime

# Create your views here.
# This gets rendered when http://127.0.0.1:8000/products is run, which is also the default
def __addToSearchHistory(search,request):
    try:
        request.session['searchHistory'][search] = str(datetime.datetime.now())
        print(len(request.session['searchHistory']))
        print(request.session['searchHistory'])
    except KeyError:
        request.session['searchHistory'] = {}
        request.session['searchHistory'][search] = str(datetime.datetime.now())
    request.session.modified = True

def index(request):
    print('INDEX')
    if 'search_filter' in request.GET:
        print('saerched')
        print(request.GET)
        search_filter = request.GET['search_filter']
        print(search_filter)
        products = [ {
            'id': x.id,
            'name': x.name,
            'color': x.color,
            'price': x.price,
            'imgURL': x.imgURL,
            'description': x.description,
            'discount': x.discount,
            'type': x.type
        } for x in Product.objects.filter(name__icontains=search_filter)]
        __addToSearchHistory(search_filter, request)
        #
        # return JsonResponse({'data': products})
        # return redirect('/')
        return render(request,'product/index.html', {'products': products})

    if 'color' in request.GET or 'price' in request.GET or 'type' in request.GET or 'sort' in request.GET:
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

        if 'type' in request.GET:
            type_filter = request.GET['type']
            type_query = Product.objects.filter(type__icontains=type_filter)
            print(type_query)
            query = query & type_query
            print(query)

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
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    # TODO: Get product images from imageDB by productID
    context = {}
    images = ProductImage.objects.filter(product_id=id)
    context['product'] = get_object_or_404(Product, pk=id)
    context['images'] = images
    return render(request, 'product/product_details.html', context)