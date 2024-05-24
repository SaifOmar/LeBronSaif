from django.forms import ModelForm
from .models import CustomUser
class LoginForm(ModelForm):

    class Meta :
        fields = ["email","password"]
        model = CustomUser 



class SignUpForm(ModelForm):
    class Meta :
        fields = ["first_name","last_name","username","email","phone","password","date_of_birth"]
        model = CustomUser