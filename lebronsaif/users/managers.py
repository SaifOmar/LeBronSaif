from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields ):
        if not email :
            raise ValueError("Please enter your email")
        if not username :
            raise ValueError("Please enter your username")
        user = self.model(username=username,email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, password,email, **extra_fields):
        if not extra_fields.get("first_name"):
            raise ValueError("please enter your first name")
        if not extra_fields.get("last_name"):
            raise ValueError("please enter your last name") 
        user = self._create_user(username=username,email=email,password=password,**extra_fields)
        return user
    
    def create_superuser(self, username,password, email, **extra_fields):
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_verified",True)
        extra_fields.setdefault("is_superuser",True)
        user = self._create_user(username=username,email=email,password=password,**extra_fields)
        return user
        
        