from django.urls import path

from .views import (
    ImmobileListView,
    CreateImmobileView,
    ImmobileDetailView,
    SelezionaImmobileView,
    AdvancedSearchImmobileView
)

app_name = "immobile"

urlpatterns = [
    # Proprietario 
    path("crea_immobile/",                      CreateImmobileView.as_view(),                  name="crea_immobile"),     

    # registrato
    path('immobile/<int:pk>/',                   ImmobileDetailView.as_view(),                  name='immobile_detail'),          
    path('seleziona-immobile/',                  SelezionaImmobileView.as_view(),               name='seleziona_immobile'),


    # guest
    path("lista_immobili/",                      ImmobileListView.as_view(),                   name="lista_immobili"),
    path('ricerca-avanzata/',                  AdvancedSearchImmobileView.as_view(),               name='ricerca_avanzata'),

]
