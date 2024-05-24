from django.urls import path
from . import views
urlpatterns = [
    path("login",views.Login.as_view(),name="login"),
    path("signup",views.SignUp.as_view(),name="signup"),
    path("logout",views.Logout.as_view(),name="logout"),
    path("verifiy_email",views.VerifiyEmail.as_view(),name="verifiy_email"),
    path("pending_verification",views.PendingVerification.as_view(),name="pending_verification"),
    path("check_verification",views.CheckVerification.as_view(),name="check_verification"),
    path("verification_compelete",views.VerificationComplete.as_view(),name="verification_complete"),
]