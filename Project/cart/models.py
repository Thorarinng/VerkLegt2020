from django.db import models
from user.models import User
from product.models import Product


class orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    product = models.CharField(max_length=255)
    shippingAddress = models.CharField(max_length=999)
    creditCard = models.CharField(max_length=255)

    def setOrderAttirbutes(self, request, context):
        self.user_id = request.user.pk
        self.product = context['cartList']
        self.creditCard = context['cardNumber']
        self.shippingAddress = context['address']
