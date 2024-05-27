from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import MyUserManager
from datetime import datetime
# Create your models here.




class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, default=None, unique=True,null=True,blank=True)
    email = models.EmailField(max_length=255, default=None)
    is_verified = models.BooleanField(default=False)
    img = models.ImageField(default=None,null=True,blank=True)
    bio = models.TextField(max_length=80,default=None,null=True,blank=True)
    # date_joined = models.DateTimeField(default=now)
    date_of_birth= models.DateTimeField(default=None,null=True,blank=True)




    objects = MyUserManager()

    REQUIRED_FIELDS = ["email"]
    

    def __str__(self) :
        return f"{self.username}"
 
 







        

