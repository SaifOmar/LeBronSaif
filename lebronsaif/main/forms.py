from django import forms
from .models import LeBrons


class NewLebronForm(forms.ModelForm):
    class Meta :
        model = LeBrons
        fields = ["lebron","image"]

    
        