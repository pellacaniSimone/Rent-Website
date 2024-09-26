from django import forms


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Zona


#####################################################################################
#               Staff: add new zones
#####################################################################################

class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ['nome', 'latitudine', 'longitudine', 'tipo', 'confinanti', 'soprazona']
    
    def __init__(self, *args, **kwargs):
        super(ZonaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Salva'))