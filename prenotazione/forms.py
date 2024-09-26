from django import forms
from dashboard.debug_utils import debug_info
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import (
    Prenotazione,
    )


#####################################################################################
#               Client rent
#####################################################################################

class PrenotazioneCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "userprenotation_crispy_form"
    helper.form_method = 'POST'
    helper.add_input(Submit('Conferma', 'Save'))

    def __init__(self, *args, **kwargs):
        debug_info(self)
        super(PrenotazioneCreateForm, self).__init__(*args, **kwargs)
        self.fields['utente'].required = False
        self.fields['immobile'].required = False

    class Meta:
        model = Prenotazione
        fields = ['data_prenotazione', 'durata',"utente","immobile"]
        widgets = {
            'data_prenotazione': forms.DateInput(attrs={'type': 'date'}),
            'durata': forms.NumberInput(attrs={'min': '15', 'max': '365', 'step': '1'}),
            'utente': forms.HiddenInput(), 
            'immobile': forms.HiddenInput(), 
        }

