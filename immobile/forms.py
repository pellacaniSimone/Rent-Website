from django import forms
from dashboard.debug_utils import debug_info

from django.shortcuts import get_object_or_404
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from zone.models import    Zona
from utenti.models import User,Proprietario

from .models import (
    Immobile,
    )


#####################################################################################
#               guest : list and search houses
#####################################################################################





class SearchAppartamentiForm(forms.Form):

    helper = FormHelper()
    helper.form_id = "search_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Cerca"))
    search_string = forms.CharField(label="Cerca",max_length=100, min_length=3)



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


#####################################################################################
#               Registered user : select and search houses
#####################################################################################


class SelezionaImmobileForm(forms.Form):
    immobile = forms.ModelChoiceField(queryset=Immobile.objects.all(), empty_label="Seleziona un immobile")
    helper = FormHelper()
    helper.form_id = "select_immobil_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Prenota"))



#####################################################################################
#               Owner: new Host
#####################################################################################
class CreateImmobileForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addimmobile_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Immobile",))
    def __init__(self, *args, **kwargs):
        """Cattura user"""
        debug_info(self)
        self.username = kwargs.pop('username', None)  
        super().__init__(*args, **kwargs)
        self.fields['indirizzo'].queryset = Zona.objects.filter(tipo='Indirizzo')
    def save(self,commit=True):
        """Usa user e lo usa come id"""
        immobile = super().save(commit=False)  
        debug_info(self,self.username)
        if self.username:
            django_user_obj = get_object_or_404(User, username=self.username)
            proprietario = Proprietario.objects.filter(pk=django_user_obj.pk)
            
            debug_info(self,proprietario)
            immobile.proprietario = proprietario.first()  
        if commit:
            immobile.save()  
        return immobile 
    class Meta:
        """user appartiene al built-in di django, 
        menu a tendina con il nome dai model"""
        model = Immobile
        fields = ["nome","indirizzo","data_creazione","prezzo","foto"]
        widgets = { 'proprietario': forms.HiddenInput(), } 
