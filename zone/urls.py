from django.urls import path

from .views import (
    ZonaCreateView,
)

app_name = "zone"

urlpatterns = [
    # Staff 
    path('nuova-zona/',                         ZonaCreateView.as_view(),           name='nuova_zona'),
]
