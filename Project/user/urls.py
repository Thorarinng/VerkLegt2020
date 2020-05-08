from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

# PAttern matching
urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    # path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(next_page='/'), name='logout')
]