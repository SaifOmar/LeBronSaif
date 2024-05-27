from django.contrib import admin
from .models import CustomUser
from main.models import LeBrons,Followers
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(LeBrons)
admin.site.register(Followers)
