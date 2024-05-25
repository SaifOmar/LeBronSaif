from django.db import models
from users.models import CustomUser
from datetime import datetime


now = datetime.now()

# Create your models here.
class LeBrons(models.Model):
    time_lebroned = models.DateField(default=now)
    lebron = models.TextField(null=False,blank= False, max_length=400)
    dunks  = models.PositiveIntegerField(default=0,null=False,blank=False)
    passes = models.PositiveIntegerField(default=0,null=False,blank=False)
    comments = models.TextField(max_length=200)
    user = models.ForeignKey(CustomUser,related_name="lebrone3'",on_delete=models.CASCADE)
    image = models.ImageField(blank=True,null=True)
    
    
    def __str__(self):
        return f""
