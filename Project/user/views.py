from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import User, ShippingAddress
from user.forms import AccountAuthenticationForm, RegistrationForm, EditProfileForm, ShippingAddressForm


def registerUser(request):
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
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("/user/account")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            print(email)
            print(password)
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("/user/account")

    else:
        form = AccountAuthenticationForm()

    context['loginForm'] = form

    # print(form)
    return render(request, "user/login.html", context)


def getProfile(request):
    # TODO: return the payment-method information stored about a user
    try:
        sa = ShippingAddress.objects.get(user_id=request.user.pk)
        context = {
            'sa': sa,
            'hasBillingAddress': True
        }
    except:
        context = {'hasBillingAddress': False}
    return render(request, 'user/account/account.html', context)


def editProfile(request):
    context = {}
    if request.POST:
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            password = form.cleaned_data['password']
            print(password)
            print(request.user.password)
            user = User.objects.get(pk=request.user.pk)
            if user:
                user.firstName = form.cleaned_data['firstName']
                user.lastName = form.cleaned_data['lastName']
                user.phoneNumber = form.cleaned_data['phoneNumber']
                user.imgURL = form.cleaned_data['imgURL']
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect("/user/account")
            else:
                print("user not ")
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

    context['editProfileForm'] = form

    return render(request, "user/account/edit/edit-profile.html", context)


def editBillingAddress(request):
    sa = ShippingAddress.objects.get(user_id=request.user.id)
    if request.POST:
        form = ShippingAddressForm(request.POST, instance=request.user)
        if form.is_valid():
            print('Valid form')
            sa = __setShippingAddressAttributes(request, form, sa)
            print(sa.city)
            sa.save()
            return redirect("/user/account")

    form = ShippingAddressForm(

    initial={
        'address1': sa.address1,
        'address2': sa.address2,
        'city': sa.city,
        'country': sa.country,
        'region': sa.region,
        'postalCode': sa.postalCode
    })
    context = {'editShippingAddressForm': form}
    return render(request, "user/account/edit/edit-billing-address.html", context)


def addBillingAddress(request):
    # TODO: should return a form that a user can manipulate
    if request.POST:
        sa = ShippingAddress()
        form = ShippingAddressForm(request.POST, instance=request.user)
        if form.is_valid():
            obj = __setShippingAddressAttributes(request, form, sa)
            print(obj.city)
            obj.save()
            return redirect("/user/account")
        else:
            print("NOT VALID")
    else:
        form = ShippingAddressForm()
    context = {'addShippingAddressForm': form}
    return render(request, "user/account/add/add-billing-address.html", context)


# Sets attributes to a shippingAddress object and returns it
def __setShippingAddressAttributes(request, form, obj):
    obj.user_id = request.user.pk
    obj.address1 = form.cleaned_data.get('address1')
    obj.address2 = form.cleaned_data.get('address2')
    obj.city = form.cleaned_data.get('city')
    obj.country = form.cleaned_data.get('country')
    obj.region = form.cleaned_data.get('region')
    obj.postalCode = form.cleaned_data.get('postalCode')
    return obj
