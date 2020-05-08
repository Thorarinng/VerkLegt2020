from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from user.models import User
from user.forms import AccountAuthenticationForm, RegistrationForm, EditProfileForm


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
            return redirect('/user/profile')
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
        return redirect("home")

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
                return redirect("/user/profile")

    else:
        form = AccountAuthenticationForm()

    context['loginForm'] = form

    # print(form)
    return render(request, "user/login.html", context)

def getProfile(request):
    return render(request, 'user/profile.html', {
    })

def editProfile(request):

    if not request.user.is_authenticated:
        return redirect("login")

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
                return redirect("/user/profile")
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

    context['editForm'] = form

    return render(request, "user/edit.html", context)

