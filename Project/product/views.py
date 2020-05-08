from django.shortcuts import render, get_object_or_404
from product.models import Product
# Dont need this, this was just an example
# from django.http import HttpResponse

# INSERT INTO product_product (name,color,price,"imgURL",description,discount)

from django.http import JsonResponse


# Create your views here.
# This gets rendered when http://127.0.0.1:8000/products is run, which is also the default
def index(request):
    context = {'products': Product.objects.all()}
    return render(request, 'product/index.html', context)


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
        return JsonResponse({'data': products})

    context = {'products': Product.objects.all()}
    return render(request, 'product/index.html', context)


# SUPPORTS -> /product/1
def getProductById(request, id):
    return render(request, 'product/product_details.html', {
        'product': get_object_or_404(Product, pk=id)
    })