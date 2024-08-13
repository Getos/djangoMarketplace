import uuid
from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cartitems")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name
