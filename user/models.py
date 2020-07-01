from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date  = models.DateField(null=True, blank=True)
    customer_id = models.CharField(max_length=100)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwawgs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
