from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from .views import (
    ProprietarioConfermaView,
    UserSettingsView,
    #ConfermaUtenteClienteView,
    ConfirmAccountView,
    UserCreateView
)

app_name = "utenti"

urlpatterns = [

    # Staff 
    path("register_pro/",            ProprietarioConfermaView.as_view(),  name="register_pro"),

    # Reg users
    path('profilo_User/<int:pk>/',   UserSettingsView.as_view(),     name='userdetail'),
    path('confirm-account/',         ConfirmAccountView.as_view(), name='confirm_account'),
    
    # guest
    path("register/",                UserCreateView.as_view(),             name="register"),
    path("login/",                   LoginView.as_view(),                  name="login"),
    path("logout/",                  LogoutView.as_view(),                 name="logout"),

]
