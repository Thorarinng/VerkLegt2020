from django.urls import path
from . import views

# PAttern matching
urlpatterns = [
    path('register', views.register, name="register"),
    # path('<int:id>', views.getProductById, name="product_details"),
]