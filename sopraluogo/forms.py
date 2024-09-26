from django import forms
from dashboard.debug_utils import debug_info
from django.shortcuts import get_object_or_404
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout
from utenti.models import UserProfile
from immobile.models import Immobile
from django.contrib.auth.models import User
from .models import (
    Sopraluogo,
    )

from django.forms import ModelForm, DateInput,NumberInput


#####################################################################################
#               Utente Cliente: Crea Sopraluoghi
#####################################################################################

class SopraluogoCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "usersopraluogotion_crispy_form"
    helper.form_method = 'POST'
    helper.add_input(Submit('Conferma', 'Save'))
    def __init__(self, *args, **kwargs):
        debug_info(self)
        super(SopraluogoCreateForm, self).__init__(*args, **kwargs)
        self.fields['utente'].required = False
        self.fields['immobile'].required = False
    class Meta:
        model = Sopraluogo
        fields = ['data_ora_sopraluogo',"utente","immobile"]
        widgets = {
            'data_ora_sopraluogo': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'utente': forms.HiddenInput(), 
            'immobile': forms.HiddenInput(), 
        }



#####################################################################################
#               Utente Proprietario: Edita Sopraluoghi
#####################################################################################






class EventForm(ModelForm):
  class Meta:
    model = Sopraluogo
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'data_ora_sopraluogo': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'durata_h': NumberInput(attrs={'min': '0', 'step': '1'}),  # Utilizza NumberInput per un input numerico
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)


