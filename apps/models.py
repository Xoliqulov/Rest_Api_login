from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import EmailField
from apps.menager import CustomUserManager


class User(AbstractUser):
    username = None
    email = EmailField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

