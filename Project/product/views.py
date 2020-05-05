from django.shortcuts import render
# Dont need this, this was just an example
# from django.http import HttpResponse


# Create your views here.
# This gets rendered when http://127.0.0.1:8000/products is run, which is also the default
def index(request):
    return render(request, 'product/index.html')