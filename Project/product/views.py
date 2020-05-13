from django.shortcuts import render, get_object_or_404
from product.models import Product
# Dont need this, this was just an example
from django.http import JsonResponse
# INSERT INTO product_product (name,color,price,"imgURL",description,discount)

from django.http import JsonResponse


# Create your views here.
# This gets rendered when http://127.0.0.1:8000/products is run, which is also the default
def filter_funk(filter_string):
    pass


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
            'discount': x.discount,
            'type': x.type
        } for x in Product.objects.filter(name__icontains=search_filter)]
        return JsonResponse({'data': products})


    if 'color' in request.GET or 'price' in request.GET or 'type' in request.GET or 'sort' in request.GET:
        query = Product.objects.all()
        print(query)
        if 'color' in request.GET:
            color_filter = request.GET['color']
            color_query = Product.objects.filter(color=color_filter)
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

    if 'color' in request.GET:
        color_filter = request.GET['color']
    if 'price' in request.GET:
        price_filter = request.GET['price']
        if price_filter == 'low':
            products = [ {
                'id': x.id,
                'name': x.name,
                'description': x.description,
                'Image': x.imgURL,
                'price': x.price
            } for x in Product.objects.filter(price__gte=0, price__lte=100)]
            return JsonResponse({'data': products})
        elif price_filter == 'mid':
            products = [{
                'id': x.id,
                'name': x.name,
                'description': x.description,
                'Image': x.imgURL,
                'price': x.price
            } for x in Product.objects.filter(price__gt=100, price__lte=500)]
            return JsonResponse({'data': products})
        elif price_filter == 'max':
            products = [{
                'id': x.id,
                'name': x.name,
                'description': x.description,
                'Image': x.imgURL,
                'price': x.price
            } for x in Product.objects.filter(price__gt=500)]
            return JsonResponse({'data': products})
    if 'brand' in request.GET:
        brand_filter = request.GET['brand']


        if 'sort' in request.GET:
            sort_filter = request.GET['sort']
            if sort_filter == "lowhigh":
                sort_query = Product.objects.order_by('price')
                query = query & sort_query
            elif sort_filter == "highlow":
                sort_query = Product.objects.order_by('-price')
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