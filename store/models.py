from django.db import models
from datetime import datetime
from customers.models import Profile
from django.contrib.auth.models import User

#category for the products
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    

      


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250,  blank=False, null=True)
    image = models.ImageField('uploads/products')
    model_image_1 = models.ImageField('uploads/products', blank=True, null=True)
    model_image_2 = models.ImageField('uploads/products', blank=True, null=True)
    sale = models.IntegerField(default=0)
    new_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)


    def save(self, *args, **kwargs):
        self.new_price = self.price - (self.price * self.sale) / 100
        super().save(*args, **kwargs)

    def __str__(self) -> str:
         return self.name
    

class ProductSize(models.Model):
    CHOICES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=100, choices=CHOICES)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('product', 'size')        


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=False)
    phone = models.CharField(max_length=50, blank=False, default='' )
    order_date = models.DateField(datetime.today())
    status = models.BooleanField(default=False)


    def __str__(self) -> str:
         return self.product    
    








