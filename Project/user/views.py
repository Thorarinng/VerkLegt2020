from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from user.forms import AccountAuthenticationForm, RegistrationForm, EditProfileForm, ShippingAddressForm, PaymentMethodForm, SearchForm
from .models import User, ShippingAddress, PaymentMethod, SearchHistory
from product.models import Product

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from product.views import index


def registerUser(request):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('/user/account')
        else:
            context['registerForm'] = form

    else:
        form = RegistrationForm()
        context['registerForm'] = form
    return render(request, 'user/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')


def loginUser(request):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    context = {}

    user = request.user
    if user.is_authenticated:
        request.content_params
        return redirect('/user/account')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                try:
                    if request.session['redirect'] == None:
                        return redirect('/')
                    else:
                        return redirect(str(request.session['redirect']))
                except:
                    return redirect('/')

    else:
        form = AccountAuthenticationForm()

    context['loginForm'] = form

    # print(form)
    return render(request, 'user/login.html', context)


def getProfile(request):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    request.session['redirect'] = None

    # TODO: return the payment-method information stored about a user
    sa = ShippingAddress()
    pm = PaymentMethod()
    # Check if a shippingAddress exists
    context = {}
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
    try:
        context['ss'] = request.session['searchHistory']
    except KeyError:
        context['ss'] = {}
    try:
        sh = __getSearchHistory(request)
        so = __sortedSearchHistory(request)
        context['sh'] = sh
        context['so'] = so
        context['hasSearchHistory'] = True
    except KeyError:
        context['hasSearchHistory'] = False
    return render(request, 'user/account/account_details.html', context)


def editProfile(request):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    if request.POST:
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            if user:
                user.__setUserAttributes__(form)
                user.save()
                login(request, user)
                return redirect('/user/account')
    else:
        form = EditProfileForm(

            initial={
                'firstName': request.user.firstName,
                'lastName': request.user.lastName,
                'imgURL': request.user.imgURL,
                'phoneNumber': request.user.phoneNumber,
                'password': request.user.password

            }
        )

    context = {'editProfileForm': form}

    return render(request, 'user/account/profile/profile_edit.html', context)


# This was originally editBillingAddress, because we had two different functions essentially doing the same thing
# Update and ADding BillingAddress are now one function
def updateBillingAddress(request):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    # Try to find a BillingAddress that exists exists
    try:
        sa = ShippingAddress.objects.get(user_id=request.user.id)
    except ShippingAddress.DoesNotExist:
        sa = ShippingAddress()

    if request.POST:
        form = ShippingAddressForm(request.POST, instance=request.user)
        if form.is_valid():
            sa.setShippingAddressAttributes(request, form)
            sa.save()
            request.session['hasShippingMethod'] = True
            request.session.modified = True
            try:
                if request.session['redirect'] == None:
                    return redirect('/user/account')
                else:
                    return redirect(str(request.session['redirect']))
            except:
                return redirect('/user/account')

    form = ShippingAddressForm(

        initial={
            'address1': sa.address1,
            'address2': sa.address2,
            'city': sa.city,
            'country': sa.country,
            'region': sa.region,
            'postalCode': sa.postalCode
        })
    context = {'updateShippingAddressForm': form}
    return render(request, 'user/account/shippingaddress/shippingaddress_update.html', context)


def updatePaymentMethod(request):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    # Try to find a BillingAddress that exists exists
    context = {}
    try:
        pm = PaymentMethod.objects.get(user_id=request.user.id)
    except PaymentMethod.DoesNotExist:
        pm = PaymentMethod()

    if request.POST:
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            # cardNumber = form.cleaned_data.get('cardNumber')
            # form.cleanCardNumber()
            # pm.validateAttributes(request, form)
            pm.setPaymentMethodAttributes(request, form)
            pm.save()
        else:
            messages.warning(request, 'Not valid Payment info')

        try:
            if request.session['redirect'] == None:
                return redirect('/user/account')
            else:
                return redirect(str(request.session['redirect']))
        except:
            return render(request, 'user/account/paymentmethod/paymentmethod_update.html', context)

    form = PaymentMethodForm(

        initial={
            'nameOnCard': pm.nameOnCard,
            'cardNumber': pm.cardNumber,
            'cardExpiry': pm.cardExpiry,
            'cvc': pm.cvc
        })

    context['updatePaymentMethod'] = form
    return render(request, 'user/account/paymentmethod/paymentmethod_update.html', context)


def __sortedSearchHistory(request):
    dateList = []
    try:
        for string in request.session['searchHistory']:
            dateList.append(request.session['searchHistory'][string])
        slr = sorted(dateList, reverse=True)
        retList = []
        count = 0
        for date in slr:
            if count == 5:
                break
            for string in request.session['searchHistory']:
                if request.session['searchHistory'][string] == date:
                    retList.append(string)
                    count += 1
                    break
        return retList

    except KeyError:
        return []


def __getSearchHistory(request):
    ret_list = {}
    for searchString in request.session['searchHistory']:
        products = [{
            'id': x.id,
            'name': x.name,
            'color': x.color,
            'price': x.price,
            'imgURL': x.imgURL,
            'description': x.description,
            'discount': x.discount,
        } for x in Product.objects.filter(name__icontains=searchString)]
        for object in products:
            object['date'] = request.session['searchHistory'][searchString]
            ret_list[str(object['id'])] = object
    return ret_list


def getSearchHistory(request):
    # checks if a user has inputted in the search field in the navbar
    if 'search_filter' in request.GET:
        return index(request)
    try:
        context = {'sh': __getSearchHistory(request)}
    except KeyError:
        context = {'sh': {}}
    return render(request, 'user/account/searchhistory/searchhistory_page.html', context)
