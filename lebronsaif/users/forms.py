from django import forms
from .models import CustomUser
class LoginForm(forms.ModelForm):
    class Meta :
        fields = ["email","password"]
        model = CustomUser 



class SignUpForm(forms.ModelForm):
    class Meta :
        fields = ["first_name","last_name","username","email","phone","password","date_of_birth"]
        model = CustomUser


class ChangePasswordForm(forms.Form):
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

class FrogotPasswordForm(forms.form):
    password = forms.PasswordInput()

