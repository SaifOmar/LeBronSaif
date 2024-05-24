from django.shortcuts import render
from django.views.generic import View
from users.models import CustomUser
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
class Home(View):
    template_name = "home.html"
    def get(self, request):
        return render(request,self.template_name) 
    def post(self, request):
        return render(request,self.template_name)

@login_required
class Profile(View):
    template_name = "profile.html"
    def get(self, request):
        return render (request,self.template_name)


