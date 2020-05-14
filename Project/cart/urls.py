from django.urls import path
from . import views

# PAttern matching
urlpatterns = [
    path('add/<int:id>/', views.addToCart, name="addToCart"),
    path('', views.getCart, name="getCart"),
    path('remove/<int:id>/', views.removeFromCart, name="removeFromCart"),
    path('checkout/', views.checkout, name="checkout"),
    path('checkout/confirm', views.confirmOrder, name="confirmOrder"),
    # path('checkout/shippingMethod', views.shippingMethod, name="shippingMethod"),

]