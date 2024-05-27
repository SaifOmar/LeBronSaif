from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from django.db.models import Q
from .models import CustomUser

class MyBackend(BaseBackend):
    def authenticate(self, request ,u_e_p=None,password=None):
        try :
            user = CustomUser.objects.get(
                Q(email = u_e_p) | Q (username = u_e_p) | Q(phone = u_e_p)
            )
            if user.check_password(password):
                return user
            return None
        except : 
            CustomUser.DoesNotExist
            return ValueError("we couldn't find an account with either this username or password")
    def get_user(self,uid):
        try :
            user = CustomUser.objects.get(pk = uid)
            return user
        except :
            CustomUser.DoesNotExist
            return None


        