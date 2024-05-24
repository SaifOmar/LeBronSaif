from django.shortcuts import render
from django.views.generic import View
from .forms import SignUpForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from .tokens import account_activation_token
from .models import CustomUser
from  main.views import Home
# Create your views here.

class Login(View):
    html_template = "login.html"
    def get(self, request):
        form = LoginForm()
        context = {"form": form}
        return render(request,self.html_template, context)
    
    def post(self,request):
        form = LoginForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try :
                user = authenticate(request,u_e_p = email,password = password)
            except : 
                user = None
            if user :
                login(request, user)
            else :
                return redirect(Login) 
        return render(request, self.html_template, context)
    


class SignUp(View):
    html_template = "signup.html"
    def get(self, request):
        form = SignUpForm()
        context = {"form":form}
        return render(request, self.html_template,context)
    
    def post(self, request):
        form = SignUpForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            form.save()
        else :
            return redirect(Home)
        return render(request, self.html_template,context)
    

@login_required
class Logout(View):
    html_template = "logedout.html"
    def get(self, request):
        logout(request)
        return render(request,self.html_template)


class VerifiyEmail(View):
    html_template = "verifiy_email.html"
    def post(self,request):
        if user.is_verified != True :
            domain = get_current_site(request)
            user = request.user
            email = request.user.email
            subject = "Please verifiy your email"
            html_content = "verifiymsg.html"
            message = render_to_string(
                html_content,{
                    "request": request,
                    "domain": domain.domain.site,
                    "user": user,
                    "uid":urlsafe_base64_encode(force_bytes(user.id)),
                    "token": account_activation_token.make_token(user),
                }
            )

            emai = EmailMessage(
                subject,message,to=[emai] 
            )
            email.conetet_subtype = "html"        
            email.send()
            return redirect(PendingVerification)
        else : return redirect(AlreadyVerified)
    def get(self,request):
       return render(request,"verifiy_email")

        
class AlreadyVerified(View):
    html_template= "already_verified.html"
    def get(self,request):
        return render(request,self.html_template)
class CheckVerification(View):
    def get(self,request, uid64, token):
        try :
            uid = urlsafe_base64_decode(force_str(uid64))
            user = CustomUser.objects.get(id = uid)
        except :
            (TypeError,ValueError,CustomUser.DoesNotExist,OverflowError)
            user = None
        if user is not None and account_activation_token.check_token(user,token):
            user.is_verified = True
            user.save()
            return redirect(VerificationComplete)
        else : messages.warning(request,"link is invalid")
        return render(request, "checkverification") 


class VerificationComplete(View):
    html_template = "verificationcomplete.html"
    def get(self,request):
        return render(request,self.html_template)

class PendingVerification(View):
    html_template = "pending_verification.html"
    def get(self,request):
        return render(request,self.html_template)




        

