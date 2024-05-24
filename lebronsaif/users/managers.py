from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def _create_user(self, email, phone, username, password, **extra_fields ):
        if not email :
            raise ValueError("Please enter your email")
        if not username :
            raise ValueError("Please enter your username")
        user = self.model(username=username,phone=phone,email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, phone, username, password,email, **extra_fields):
        if not extra_fields.get("first_name"):
            raise ValueError("please enter your first name")
        if not extra_fields.get("last_name"):
            raise ValueError("please enter your last name")
        if not phone :
            raise ValueError("please enter your phone")
        user = self._create_user(phone=phone,username=username,email=email,password=password,**extra_fields)
        return user
    
    def create_superuser(self, username,password, email, **extra_fields):
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_verified",True)
        user = self._create_user(username=username,email=email,password=password,**extra_fields)
        return user
        
        