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
        return render(request, "users/Loged_in.html")

class Logout(View):
    html_template = "users/logedout.html"
    def get(self, request):
        logout(request)
        return render(request,self.html_template)
    

class Login(View):
    html_template = "users/login.html"
    def get(self, request):
        if request.user.is_authenticated :
            return redirect('main:home')
        form = LoginForm()
        context = {"form": form}
        return render(request,self.html_template, context)
    
    def post(self,request):
        form = LoginForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            e_u_p = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            print(e_u_p,password)
            try :
                user = authenticate(u_e_p = e_u_p, password = password)
                print(user)
            except : 
                user = None
                print(user)
                messages.error(request,"We couldn't log you in with these creds")
                return redirect('users:login')
            if user :
                login(request, user)
                if not user.is_verified :
                    return redirect('users:verifiy_email')
                return redirect('users:logged_in')
            else :
                print(user)
                messages.error(request,"tbd")
                return redirect('users:login') 
        return render(request, self.html_template, context)
    


class SignUp(View):
    html_template = "users/signup.html"
    def get(self, request):
        form = SignUpForm()
        context = {"form":form}
        return render(request, self.html_template,context)
    
    def post(self, request):
        form = SignUpForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            password=form.cleaned_data['password']
            user = form.save()
            user.set_password(password)
            user.save()
            return redirect('main:home')
        return render(request, self.html_template,context)
    

# @login_required


class VerifiyEmail(View):
    html_template = "user/verifiy_email.html"
    def post(self,request):
        if request.user.is_authenticated:
            if request.user.is_verified != True :
                domain = get_current_site(request)
                user = request.user
                email = request.user.email
                name = request.user.first_name
                subject = "Please verifiy your email"
                html_content = "users/verifiymsg.html"
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

                email = EmailMessage(
                    subject,message,to=[email] 
                )
                email.content_subtype = "html"        
                email.send()
                return redirect('users:pending_verification')
            else : return redirect("users:already_verified")
        else : 
            messages.error(request,"You need to login first!")
            return redirect('users:login')
    def get(self,request):
       return render(request,"users/verifiy_email.html")

        
class AlreadyVerified(View):
    html_template= "users/already_verified.html"
    def get(self,request):
        return render(request,self.html_template)
    
class CheckVerification(View):
    def get(self,request, uidb64, token):
        try :
            uid = urlsafe_base64_decode(force_str(uidb64))
            user = CustomUser.objects.get(pk = uid)
        except :
            (TypeError,ValueError,CustomUser.DoesNotExist,OverflowError)
            user = None
        if user is not None and account_activation_token.check_token(user,token):
            user.is_verified = True
            user.save()
            return redirect('users:verification_complete')
        else :
            messages.warning(request,"link is invalid")
            return redirect('users:smth_blew_up')
        # return render(request, "checkverification.html") 


class VerificationComplete(View):
    html_template = "users/verification_complete.html"
    def get(self,request):
        return render(request,self.html_template)

class PendingVerification(View):
    html_template = "users/pending_verification.html"
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
            return redirect('users:change_password')
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
            return render(request,"users/pending_password_change.html")
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
                return redirect('users:change_password')
            else :
                return redirect('users:change_password')
        else :
            messages.error(request,"Invalid link plase try again")
            return redirect('users:something_went_wrong') 

class SomethingWentWrong(View):
    html_template= 'users/something_went_wrong.html'
    def get(self, request):
        return render(request,self.html_template)

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
            return redirect('main:home')
        
        elif not user :
            try :
                CustomUser.objects.create(
                email= user_info["email"],
                # phone = user_info["phone"],
                first_name = user_info["given_name"],
                last_name = user_info["family_name"],
                                      )
                login(request,user)
                return redirect('users:logged_in')
            except :
                (ValueError,TypeError,OverflowError)
                messages.error(request,"we failed to log you in")
                return redirect('users:something_went_wrong')
        else :
            return render(request,"something_blew_up.html")





        



            
        

        






        

