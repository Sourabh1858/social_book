from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .manager import CustomUserManager

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    publicVisibility = models.BooleanField(default=False)
    birthYear = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=200,  null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    objects = CustomUserManager()


    def __str__(self):
        return self.email

