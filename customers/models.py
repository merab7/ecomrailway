from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    city =  models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=100, null=True)
    old_cart =  models.CharField(max_length=200, blank=True, null=True)
    
  
   
    def __str__(self):
            return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
