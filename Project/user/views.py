from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render

from user.forms import AccountAuthenticationForm, RegistrationForm


def registerUser(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('/')
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
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("/")

    else:
        form = AccountAuthenticationForm()

    context['loginForm'] = form

    # print(form)
    return render(request, "user/login.html", context)
