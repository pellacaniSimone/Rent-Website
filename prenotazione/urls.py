
from django.urls import path

from .views import (

    PrenotazioneCreateView,
    PrenotazioniClienteListView,
    AffittiProprietarioListView,
)

app_name = "prenotazione"

urlpatterns = [
    # Client
    path("prenota/<int:pk>"                 ,   PrenotazioneCreateView.as_view(),           name="prenota"),
    path("storico/",                            PrenotazioniClienteListView.as_view(),      name="storico_cli"),

    # Owner
    path("storico_pro/",                            AffittiProprietarioListView.as_view(),      name="storico_pro"),

]
