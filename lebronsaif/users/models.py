from django.db import models
from django.contrib.auth.models import AbstractUser
from managers import MyUserManager
from datetime import datetime
# Create your models here.

now = datetime.now()
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, default=None, unique=True)
    email = models.EmailField(max_length=255, default=None)
    is_verified = models.BooleanField(default=False)
    img = models.ImageField(default=None)
    bio = models.TextField(max_length=80,default=None)
    date_joined = models.DateTimeField(default=now)
    date_of_birth= models.DateTimeField(default=None)
    


    objects = MyUserManager()

    REQUIRED_FIELDS = ["email","phone"]

    def __str__(self) :
        return f"{self.first_name}"