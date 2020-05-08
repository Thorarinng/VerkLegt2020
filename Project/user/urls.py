from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

# PAttern matching
urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.getProfile, name='profile'),
    path('edit/', views.editProfile, name='edit'),

]