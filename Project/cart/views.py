from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from product.models import Product
from django.contrib import messages


# Create your views here.


def addToCart(request, id):
    product = Product.objects.get(id=id)
    # Guard against default cookies without cart.
    # If cart hasn't been created in the cookies before, we do it here
    __cartExists(request)
    request.session['cart'][str(id)] = product.productToDict(id)
    request.session.modified = True
    messages.success(request, 'Added to cart')
    return redirect("/")


def __cartExists(request):
    try:
        # See if cart exists
        context = {'cart': request.session['cart']}
    except KeyError:
        # If not, we create it
        request.session['cart'] = {}
        context = {}
    return context


def getCart(request):
    context = __cartExists(request)
    return render(request, 'cart/cart.html', context)


def removeFromCart(request, id):
    # This guard should prevent crash
    context = __cartExists(request)
    print(request.session['cart'][str(id)])
    # Removing the certain product from the cart
    del request.session['cart'][str(id)]
    # Committing the changes
    request.session.modified = True
    # dictionary ret value to return
    context = {'cart': request.session['cart']}
    # Message displayed when item removed
    messages.warning(request, 'Item removed from cart')
    # render(request, 'cart/cart.html', context)
    return redirect('/cart')
