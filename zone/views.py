from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
from .forms import ZonaForm

#####################################################################################
#               Staff: Zona setting, owner confirmation
#####################################################################################


class ZonaCreateView(CreateView,SuccessMessageMixin):
    form_class = ZonaForm
    template_name = 'zone/inserimento_zona.html'
    success_url = 'zone/inserimento_zona.html'  # redirect after save
    success_message = "Successo!"
    permission_required = "is_staff"