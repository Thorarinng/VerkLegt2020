from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from user.forms import ContactForm, UserLoginForm


def register(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            # new_user = authenticate(email=user.email, password=user.password)
            # login(request, new_user)
            return redirect('login')
    return render(request, 'user/register.html', {
        'form': ContactForm()
    })

def login(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)

    context = {
        'form':form
    }
    return render(request, "user/login.html", context)


#
# def register(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         user = form.save(commit=False)
#         password = form.cleaned_data.get('password')
#         user.set_password(password)
#         user.save()
#         new_user = authenticate(email=user.email, password=user.password)
#         login(request, new_user)
#         return redirect('/')
#     else:
#         form = ContactForm()
#
#     return render(request, 'user/register.html', {'form': form})
#
