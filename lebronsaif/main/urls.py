from django.urls import path
from . import views
urlpatterns = [
    path("",views.Home.as_view(),name="home"),
    path("profile",views.Profile.as_view(),name="profile"),
]
