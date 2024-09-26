
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path,re_path

from .views import AggiungiRecensioneView

app_name = "recensione"

urlpatterns = [

    path('aggiungi/<int:pk>', AggiungiRecensioneView.as_view(), name='aggiungi'),

]
