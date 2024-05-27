from django.shortcuts import render
from django.views.generic import View
from .forms import SignUpForm,LoginForm,FrogotPasswordForm,ChangePasswordForm
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
from django.conf import settings
import requests
from  main.views import Home
# Create your views here.

class Loged_in(View):
    def get(self,request):
        return render(request, "Loged_in.html")

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
                messages.error(request,"We couldn't log you in with these creds")
                return render(request, self.html_template, context)
            if user :
                login(request, user)
                if not user.is_verified :
                    return redirect(VerifiyEmail)
                return redirect(Loged_in)
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
    

# @login_required
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
            name = request.user.first_name
            subject = "Please verifiy your email"
            html_content = "verifiymsg.html"
            message = render_to_string(
                html_content,{
                    "name": name,
                    "request": request,
                    "domain": domain.domain,
                    "user": user,
                    "uid":urlsafe_base64_encode(force_bytes(user.pk)),
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
            user = CustomUser.objects.get(pk = uid)
        except :
            (TypeError,ValueError,CustomUser.DoesNotExist,OverflowError)
            user = None
        if user is not None and account_activation_token.check_token(user,token):
            user.is_verified = True
            user.save()
            return redirect(VerificationComplete)
        else :
            messages.warning(request,"link is invalid")
        return render(request, "checkverification") 


class VerificationComplete(View):
    html_template = "verificationcomplete.html"
    def get(self,request):
        return render(request,self.html_template)

class PendingVerification(View):
    html_template = "pending_verification.html"
    def get(self,request):
        return render(request,self.html_template)

# @login_required
class ChangePassword(View):
    html_template = "change_password.html"
    def get(self,request):
        return render(request,self.html_template)
    def post(self,request):
        form = ChangePasswordForm(request.POST)
        user = request.user
        if form.is_valid():
            p1 = form.cleaned_data["password1"]
            p2 = form.cleaned_data["password2"]
            if p1 == p2 :
                user.set_password(p1)
                user.save()
            else :
                messages.error(request,"Please make sure that both passwords match")
        else : 
            return redirect(ChangePassword)
        return render(request,"password_changed.html")


class ForgotPassword(View):
    html_template = "forgot_password.html"
    def get(self,request):
        return render(request,self.html_template)
    def post(self,request):
        html_content = "forgot_pw_message.html"
        form = FrogotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
        else : messages.warning("Please enter a valid email adress")
        user = CustomUser.objects.get(email=email)
        if user :
            uid = user.pk
            name = user.first_name
            domain = get_current_site(request)
            subject = f"Change your {domain.name} password"
            message= render_to_string(
                html_content,{
                    "name": name,
                    "token":account_activation_token.make_token(user),
                    "uid":urlsafe_base64_encode(force_bytes(uid)),
                    "domain":domain.domain,
                    "user" : user,
                    "request":request,
                }
            )
            send_email = EmailMessage(subject,message,to=[email])
            send_email.content_subtype = 'html'
            send_email.send()
            return render(request,"pending_password_change.html")
        else :
            messages.error("We couldn't find an account that has this email")


# make validation for the forgot password scenario #
class ValidatePasswordChange(View):
    def get(self,request, uid64, token):
        try :
            uid = urlsafe_base64_decode(force_str(uid64))
            user = CustomUser.objects.get(pk=uid)
        except :
            (TypeError,ValueError,CustomUser.DoesNotExist)
            user = None
        if user is not None and account_activation_token.check_token(user,token):
            if user.is_authenticated == False:
                login(request,user)
                return redirect(ChangePassword)
            else :
                return redirect(ChangePassword)
        else :
            messages.error(request,"Invalid link plase try again")
            return render(request,"password_change_failed.html") 


class SocialLogin(View):
    def get(self,reuqest):
        google_redirect_url = (
        "https://accounts.google.com/o/oauth2/auth"
        "?response_type=code"
        "&client_id={client_id}"
        "&redirect_uri={redirect_uri}"
        "&scope=openid%20email%20profile"
        ).format(client_id = settings.GOOGLE_CILENT_ID,
        redirect_uri =settings.GOOGLE_REDIRECT_URI)
        return redirect(google_redirect_url)

class CallBack(View):
    def get(self,request):
        code = request.GET.get("code")
        token_url = "https://oauth2.googleapis.com/token"
        token_date = {
            "code": code,
            "clinet_id": settings.GOOGLE._CLIENT_ID,
            "clinet_secret":settings.GOOGLE_CLINET_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type":"authorization_code",
        }
        token_r = requests.post(token_url, data = token_date)
        token_json = token_r.json()
        access_token = token_json.get("access_token")

        user_info_url= "https://www.googleapis.com/oauth2/v1/userinfo"
        user_info_parametars = {"access_token":access_token}
        user_info_r = requests.get(user_info_url,params=user_info_parametars)
        user_info  = user_info_r.json()

        user = CustomUser.objects.get(user_info["id"])

        if user :
            login(request,user)
            return redirect(Home)
        
        elif not user :
            try :
                CustomUser.objects.create(
                email= user_info["email"],
                # phone = user_info["phone"],
                first_name = user_info["given_name"],
                last_name = user_info["family_name"],
                                      )
                login(request,user)
                return redirect(Loged_in)
            except :
                (ValueError,TypeError,OverflowError)
                return messages.error(request,"we failed to log you in")
        else :
            return render(request,"something_blew_up.html")





        



            
        

        






        

