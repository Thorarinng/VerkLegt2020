from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

# Pattern matching
urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('account/', views.getProfile, name='account'),
    path('account/profile/edit/', views.editProfile, name='editProfile'),
    path('account/shippingaddress/edit/',
         views.updateBillingAddress, name='updateBillingAddress'),
    path('account/paymentmethod/edit/',
         views.updatePaymentMethod, name='updatePaymentMethod'),
    path('account/searchhistory', views.getSearchHistory, name='getSearchHistory'),
]
