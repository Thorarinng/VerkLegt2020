from django.db import models



# Create your models here.
class Product(models.Model):
    # TODO: Add the rest of the attributes required
    # Id attribute is both auto-generated and auto-incremental
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    price = models.IntegerField()
    imgURL = models.CharField(max_length=999)
    description = models.CharField(max_length=255, blank=True)
    discount = models.FloatField()

    type = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    def productToDict(self, id):
        productDict = {
            'id': id,
            'name': self.name,
            'color': self.color,
            'price': self.price,
            'imgURL': self.imgURL,
            'description': self.description,
            'discount': self.discount,
            'type': self.type
        }
        return productDict


class ProductImage(models.Model):
    image = models.CharField(max_length=999)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)