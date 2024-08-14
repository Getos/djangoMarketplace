from django.db import models
# from django.db.models.signals import post_save
# from .signals import Order_confirmation_email
# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.IntegerField()
    imageUrl = models.URLField(
        default='https://upload.wikimedia.org/wikipedia/commons/2/2f/Blue_vacuum_cleaner.svg')

    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.8)

    def __str__(self):
        return f"{self.title} (Quantity: {self.quantity})"


# def emailConfig(sender, instance, created, *args, **kwargs):
#     if instance.title == "emailCongir":
#         print("welcome sir")
#         Order_confirmation_email.send(sender=sender, instance=instance)


# post_save.connect(emailConfig, sender=Product)
