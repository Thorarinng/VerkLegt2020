from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from psycopg2.extensions import JSON

from cart.models import orders
from product.models import Product
from django.contrib import messages

# Create your views here.
from user.forms import AccountAuthenticationForm, ShippingAddressForm, EditProfileForm
from user.models import ShippingAddress, PaymentMethod


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
    print(request.session['cart'])
    return redirect("/cart")
    # return render(request, 'cart/cart.html', context)


def checkout(request):
    try:
        if request.session['cart'] == {}:
            return getCart(request)
        else:
            request.session['redirect'] = '/cart/checkout'
            print("Redirect path: ", request.session['redirect'])
            context = {}
            if request.user.is_authenticated:
                return __getCheckoutDetails(request)
            else:
                print("redirect")
                form = AccountAuthenticationForm(request.POST)
                context['loginForm'] = form
                # redirect to cart when logging in from checkout
                request.session['redirect'] = '/cart'
                return render(request, "user/login.html", context)
    except:
        return redirect("/")


@login_required
def __getCheckoutDetails(request):
    # TODO: return the payment-method information stored about a user
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
    except ShippingAddress.DoesNotExist:
        context['hasShippingAddress'] = False
    # Check if a PaymentMethod exists
    # pm.checkIfExists(request.user.pk)
    try:
        pm = PaymentMethod.objects.get(user_id=request.user.pk)
        context['pm'] = pm
        context['hasPaymentMethod'] = True
    except PaymentMethod.DoesNotExist:
        context['hasPaymentMethod'] = False

    total = 50
    for item in context['cart']:
        print(int(context['cart'][item]['price']))
        total += int(context['cart'][item]['price'])
    request.session['total'] = total
    context['total'] = request.session['total']
    request.session.modified = True

    return render(request, 'cart/checkout_shipping.html', context)


@login_required
def getPayment(request):
    context = {}
    pm = PaymentMethod.objects.get(user_id=request.user.pk)
    context['hasPaymentMethod'] = True
    context['pm'] = pm
    context['cart'] = request.session['cart']
    context['total'] = request.session['total']
    return render(request, 'cart/checkout_payment.html', context)


@login_required
def reviewOrder(request):
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
    pm = PaymentMethod.objects.get(user_id=request.user.pk)
    sa = ShippingAddress.objects.get(user_id=request.user.pk)
    context = {}
    context['cart'] = request.session['cart']
    context['total'] = request.session['total']
    # Add to database.
    # credit cart
    cardNumber = {'cardNumber': str(pm.getCardNumber), 'name': str(pm.nameOnCard)}
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
