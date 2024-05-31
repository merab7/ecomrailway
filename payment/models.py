from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=300)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    per_id = models.CharField(max_length=200, null=True)
    add_information = models.TextField( null=True)


    def __str__(self) -> str:
        return f'Shipping Address - {str(self.id)}'


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        ShippingAddress.objects.create(user=instance)
    instance.profile.save()


# general order
class Order(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
     fullname = models.CharField(max_length=300)
     email = models.EmailField(max_length=200)
     address = models.TextField(max_length=150000)
     total_paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
     date = models.DateTimeField(auto_now_add=True)
     phone = models.CharField(max_length=200)
     per_id = models.CharField(max_length=200, null=True)
     shipped = models.BooleanField(default=False)
     shipped_date = models.DateTimeField(blank=True, null=True)

     def __str__(self) -> str:
         return f'Order -- {str(self.fullname)} -- {str(self.id)}'
     

#automatically add shipping date
@receiver(pre_save, sender=Order)
def shipped_date_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.shipped_date = now



#each item in order
class Order_item(models.Model):
     order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
     quantity = models.PositiveBigIntegerField(default=1)
     price = models.DecimalField(max_digits=10, decimal_places=2)
     size = models.CharField(max_length=100, default='')

     def __str__(self) -> str:
        return f'Order Item -- {str(self.id)}'





