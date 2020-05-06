from django.urls import path
from . import views

# PAttern matching
urlpatterns = [
    path('', views.index, name="product-index"),
    path('<int:id>', views.getProductById, name="product_details"),
]