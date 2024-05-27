from django import forms
from .models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput,required=True)



class SignUpForm(forms.ModelForm):
    class Meta :
        fields = ["first_name","last_name","username","email","phone","password","date_of_birth"]
        model = CustomUser


class ChangePasswordForm(forms.Form):
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

class FrogotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=30)
    
