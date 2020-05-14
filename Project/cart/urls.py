from django.urls import path
from . import views

# PAttern matching
urlpatterns = [
    path('add/<int:id>/', views.addToCart, name="addToCart"),
    path('', views.getCart, name="getCart"),
    path('remove/<int:id>/', views.removeFromCart, name="removeFromCart"),
    path('checkout/shipping', views.checkout, name="checkoutShipping"),
    path('checkout/payment', views.getPayment, name="paymentOrder"),
    path('checkout/review', views.reviewOrder, name="reviewOrder"),
    path('checkout/confirm', views.confirmOrder, name="confirmOrder"),
]