from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    path("login",views.Login.as_view(),name="login"),
    path("signup",views.SignUp.as_view(),name="signup"),
    path("logout",views.Logout.as_view(),name="logout"),
    path("loged_in",views.Loged_in.as_view(),name = "logged_in"),
    path("verifiy_email",views.VerifiyEmail.as_view(),name="verifiy_email"),
    path("pending_verification",views.PendingVerification.as_view(),name="pending_verification"),
    path("already_verified",views.AlreadyVerified.as_view(),name="already_verified"),
    path("check_verification/<uidb64>/<token>",views.CheckVerification.as_view(),name="check_verification"),
    path("verification_compelete",views.VerificationComplete.as_view(),name="verification_complete"),
    path("callback",views.CallBack.as_view(),name="callback"),
    path("change_password",views.ChangePassword.as_view(),name="change_password"),
    path("forgot_password",views.ForgotPassword.as_view(),name="forgot_password"),
    path("valide_password_change",views.ValidatePasswordChange.as_view(),name="validate_change_password"),
    path('smth_blew_up',views.SomethingWentWrong.as_view(),name="smth_blew_up"),

]