from django.db import models
from django.contrib.auth.models import AbstractUser
from base.manager import UserManager

# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True)
    
    objects = UserManager()
    username = None
    REQUIRED_FIELDS = []  # Add any additional required fields here

    def __str__(self) -> str:
        return self.email