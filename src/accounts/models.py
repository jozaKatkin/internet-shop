from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('The Email must be set')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        superuser = self.create_user(email, password, **kwargs)
        superuser.is_admin = True
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()
        return superuser


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=False, unique=True)
    created = models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=225, null=True, blank=True)
    updated = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return f'{self.first_name}, {self.last_name}'

    def __str__(self):
        return self.email
