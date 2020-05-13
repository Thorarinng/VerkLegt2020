from django.urls import path
from . import views

# PAttern matching
urlpatterns = [
    path('add/<int:id>/', views.addToCart, name="addToCart"),
    path('', views.getCart, name="getCart"),
    path('remove/<int:id>/', views.removeFromCart, name="removeFromCart"),
]