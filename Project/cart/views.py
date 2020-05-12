from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from product.models import Product
from django.contrib import messages


# Create your views here.


def addToCart(request, id):
    product = Product.objects.get(id=id)
    # request.session.setdefault('cart', {})[str(id)] = product.productToDict()
    if request.session['cart'] is None:
        request.session['cart'] = {}
    request.session['cart'][str(id)] = product.productToDict(id)
    # request.session['cart'].append(product.productToDict())
    # return render(request, 'base.html', request.session['cart'])
    # return render(request, 'product/index.html')
    request.session.modified = True
    messages.success(request, 'Added to cart')
    return redirect("/")


def getCart(request):
    context = {'cart': request.session['cart']}
    return render(request, 'cart/cart.html', context)


def removeFromCart(request, id):
    print(request.session['cart'][str(id)])
    del request.session['cart'][str(id)]
    request.session.modified = True
    context = {'cart': request.session['cart']}
    return render(request, 'cart/cart.html', context)
