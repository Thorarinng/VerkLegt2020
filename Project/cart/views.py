from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from product.models import Product
from django.contrib import messages


# Create your views here.


def addToCart(request, productId):
    product = Product.objects.get(id=id)
    # Guard against default cookies without cart.
    # If cart hasn't been created in the cookies before, we do it here
    try:
        if request.session['cart'] is None:
            request.session['cart'] = {}
    except:
        request.session['cart'] = {}
    request.session['cart'][str(productId)] = product.productToDict(productId)
    request.session.modified = True
    messages.success(request, 'Added to cart')
    return redirect("/")


def getCart(request):
    context = {'cart': request.session['cart']}
    return render(request, 'cart/cart.html', context)


def removeFromCart(request, productId):
    print(request.session['cart'][str(productId)])
    # Removing the certain product from the cart
    del request.session['cart'][str(productId)]
    # Committing the changes
    request.session.modified = True
    # dictionary ret value to return
    context = {'cart': request.session['cart']}
    # Message displayed when item removed
    messages.warning(request, 'Item removed from cart')
    return render(request, 'cart/cart.html', context)
