
from django.urls import path

from .views import (

    CalendarioSopraluoghiView,
    SopraluogoCreateView,
    event,

)

app_name = "sopraluogo"

urlpatterns = [
    # Utente Cliente
    path("sopraluogo/<int:pk>"                 ,   SopraluogoCreateView.as_view(),   name="sopraluogo"),


    # Utente Proprietario
    path("calendario/"                     ,   CalendarioSopraluoghiView.as_view(),   name="calendar"),
    path("calendario/new/"                 ,   event,   name="event_new"),
    path("calendario/<int:event_id>/"      ,   event,   name="event_edit"),
]
