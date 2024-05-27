from django.shortcuts import render
from django.views.generic import View
from users.models import CustomUser
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required 
from .models import LeBrons,Followers
from django.db.models import Q
from .forms import NewLebronForm
from django.utils.timezone import now
from django.contrib import messages
# Create your views here.

class Home(View):
    template_name = "home.html"
    def get(self, request):
        if request.user.is_authenticated :
            form = NewLebronForm()
            uid = request.user.pk
            followers = Followers.get_my_followers(uid)
            followed = Followers.get_my_followed(uid)
            counts = {
                "followers_count" : Followers.count_my_followers(uid),
                "followed_count" :Followers.count_my_followed(uid)
            }
            lebrons = LeBrons.objects.filter(lebroner__in=followed).order_by('time_lebroned').reverse()
            context= {
            "followers" : followers,
            "lebrons"   :  lebrons,
            "counts"    : counts,
            "form"      : form,
            } 
            return render(request,self.template_name,context) 
        return redirect('users:login')

    
    def post(self, request):
        pk = request.user.pk
        user = request.user
        form = NewLebronForm(request.POST)
        if form.is_valid():
            img = form.cleaned_data["image"]
            lebron = form.cleaned_data["lebron"]
            LeBrons.objects.create(image=img , lebron=lebron, lebroner = user)
            messages.success(request,"You LeBroned !")
            return redirect('main:home')




class Profile(View):
    template_name = "profile.html"
    def get(self, request ,uid):
        pk = request.user.pk
        lebrons = LeBrons.objects.filter(lebroner =uid)
        followers = Followers.objects.filter(followed = uid)
        context = {
            "lebrons":lebrons,
            "followers": followers,
                   }
        return render (request,self.template_name,lebrons,context)
    



