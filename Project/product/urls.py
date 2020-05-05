from django.urls import path
from . import views

# PAttern matching
urlpatterns = [
    path('', views.index, name="product-index"),
]