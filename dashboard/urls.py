from dashboard.debug_utils  import  page_not_found_fbv_view,InitDBView
from django.urls import path, re_path, include
from django.contrib import admin
from .views import (

    RentHomeView, # dashboard oppure home
    DashboardHomeView,
  )

urlpatterns = [
     # Utente Iscritto
    path("dashboard/",                          DashboardHomeView.as_view(),    name="dashboard"), 
    re_path(r"^$|^\/$|^home\/$",                RentHomeView.as_view(),         name="home"),
    # admin
    path('admin/',                              admin.site.urls,                name="admin" ),
    # path                                      # class view                  # html url name ES action="{% url 'cerca_immobile' %}"
    re_path(r"^init_db/$",                      InitDBView.as_view(),         name="init_db"), # dev mode
    path("prenotazione/",                       include("prenotazione.urls"), name="prenotazione"), # app
    path("sopraluogo/",                         include("sopraluogo.urls"), name="sopraluogo"), # app
    path("recensione/",                         include("recensione.urls"), name="recensione"), # app
    path("immobile/",                           include("immobile.urls"), name="immobile"), # app
    path("utenti/",                             include("utenti.urls"), name="utenti"), # app
    path("zone/",                               include("zone.urls"), name="zone"), # app
    path('404/',                                page_not_found_fbv_view, name='page_not_found'), # app

]



