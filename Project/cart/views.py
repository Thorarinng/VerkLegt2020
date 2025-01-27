from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from product.views import index
from cart.models import orders
from product.models import Product
from user.forms import AccountAuthenticationForm, ShippingAddressForm, EditProfileForm
from user.models import ShippingAddress, PaymentMethod

from psycopg2.extensions import JSON


def addToCart(request, id):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    product = Product.objects.get(id=id)
    # Guard against default cookies without cart.
    # If cart hasn't been created in the cookies before, we do it here
    __cartExists(request)
    request.session['cart'][str(id)] = product.productToDict(id)
    request.session.modified = True
    messages.success(request, 'Added to cart')
    return redirect('/')


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
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    context = __cartExists(request)
    return render(request, 'cart/cart.html', context)


def removeFromCart(request, id):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    # This guard should prevent crash
    context = __cartExists(request)
    # Removing the certain product from the cart
    del request.session['cart'][str(id)]
    # Committing the changes
    request.session.modified = True
    # dictionary ret value to return
    context = {'cart': request.session['cart']}
    # Message displayed when item removed
    messages.warning(request, 'Item removed from cart')
    return redirect('/cart')


def checkout(request):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    request.session['redirect'] = '/cart/checkout/shipping'
    request.session.modified = True
    try:
        if request.session['cart'] == {}:
            return getCart(request)
        else:
            context = {}
            if request.user.is_authenticated:
                return __getCheckoutDetails(request)
            else:
                form = AccountAuthenticationForm(request.POST)
                context['loginForm'] = form
                # redirect to cart when logging in from checkout
                request.session['redirect'] = '/cart'
                request.session.modified = True
                return render(request, 'user/login.html', context)
    except:
        return redirect('/')


def __getCheckoutDetails(request):
    sa = ShippingAddress()
    pm = PaymentMethod()
    # Check if a shippingAddress exists
    context = {}
    try:
        context['cart'] = request.session['cart']
    except:
        pass
    try:
        sa = ShippingAddress.objects.get(user_id=request.user.pk)
        context['sa'] = sa
        context['hasShippingAddress'] = True
        request.session['hasShippingAddress'] = True
    except ShippingAddress.DoesNotExist:
        context['hasShippingAddress'] = False
        messages.warning(request, 'Missing shipping method')
        context = {'hasShippingAddress': False}
        context['cart'] = request.session['cart']
        return render(request, 'cart/checkout_shipping.html', context)
    try:
        pm = PaymentMethod.objects.get(user_id=request.user.pk)
        context['pm'] = pm
        context['hasPaymentMethod'] = True
        request.session['hasPaymentMethod'] = True
    except PaymentMethod.DoesNotExist:
        context['hasPaymentMethod'] = False
    total = 50
    for item in context['cart']:
        total += int(context['cart'][item]['price'])
    request.session['total'] = total
    context['total'] = request.session['total']
    request.session.modified = True
    return render(request, 'cart/checkout_shipping.html', context)


@login_required
def getPayment(request):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    request.session['redirect'] = '/cart/checkout/payment'
    request.session.modified = True
    context = {}
    try:
        pm = PaymentMethod.objects.get(user_id=request.user.pk)
        context['hasPaymentMethod'] = True
        context['pm'] = pm
        context['cart'] = request.session['cart']
        context['total'] = request.session['total']
    except:
        context['cart'] = request.session['cart']
        context['total'] = request.session['total']
        messages.warning(request, 'Missing Payment')
        context['hasPaymentMethod'] = False
        return render(request, 'cart/checkout_payment.html', context)
    return render(request, 'cart/checkout_payment.html', context)


@login_required
def reviewOrder(request):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    context = {}
    context['cart'] = request.session['cart']
    sa = ShippingAddress.objects.get(user_id=request.user.pk)
    context['sa'] = sa
    pm = PaymentMethod.objects.get(user_id=request.user.pk)
    context['pm'] = pm
    context['total'] = request.session['total']
    return render(request, 'cart/review_order.html', context)


@login_required
def confirmOrder(request):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    pm = PaymentMethod.objects.get(user_id=request.user.pk)
    sa = ShippingAddress.objects.get(user_id=request.user.pk)
    context = {}
    context['cart'] = request.session['cart']
    context['total'] = request.session['total']
    # Add to database.
    # credit cart
    cardNumber = {'cardNumber': str(
        pm.getCardNumber), 'name': str(pm.nameOnCard)}
    context['cardNumber'] = cardNumber
    # Address
    address = {'address': sa.address1, 'city': sa.city, 'country': sa.country, 'region': sa.region,
               'postal': sa.postalCode}
    context['address'] = address
    # Orders
    cartList = []
    for item in context['cart']:
        cartList.append(context['cart'][item]['id'])
    context['cartList'] = cartList
    # save to database
    orderModel = orders()
    orderModel.setOrderAttirbutes(request, context)
    orderModel.save()
    # clear cart
    del request.session['cart']
    del request.session['total']
    request.session.modified = True
    return render(request, 'cart/confirm_order.html', context)
