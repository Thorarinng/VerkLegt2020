from user.forms import AccountAuthenticationForm, RegistrationForm, EditProfileForm, ShippingAddressForm
from .models import User, ShippingAddress

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


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
    if request.POST:
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            if user:
                user.__setUserAttributes__(form)
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

    context = {'editProfileForm': form}

    return render(request, "user/account/edit-profile.html", context)


# This was originally editBillingAddress, because we had two different functions essentially doing the same thing
# Update and ADding BillingAddress are now one function
def updateBillingAddress(request):
    # Try to find a BillingAddress that exists exists
    try:
        sa = ShippingAddress.objects.get(user_id=request.user.id)
    except ShippingAddress.DoesNotExist:
        sa = ShippingAddress()

    if request.POST:
        form = ShippingAddressForm(request.POST, instance=request.user)
        if form.is_valid():
            sa.__setShippingAddressAttributes__(request, form)
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
    return render(request, "user/account/update-billing-address.html", context)
