from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=225, null=True, blank=True)


def user_profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)


post_save.connect(user_profile_receiver, sender=settings.AUTH_USER_MODEL)


