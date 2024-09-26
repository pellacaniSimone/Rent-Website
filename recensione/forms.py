from django import forms
from dashboard.debug_utils import debug_info
from django.shortcuts import get_object_or_404
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout
from .models import Recensione
from utenti.models import Proprietario,UserProfile,User
from immobile.models import Immobile

#####################################################################################
#               Iscritti: Crea recensione
#####################################################################################




class RecensioneForm(forms.ModelForm):
    class Meta:
        model = Recensione
        fields = ['testo', 'stelline', 'immobile' , 'utente']
        widgets = { 'immobile': forms.HiddenInput(),
                   'utente': forms.HiddenInput(),
                    } # Nascondi il campo nel form


    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.username_tmp = kwargs.pop('username_tmp', None)
        self.pk_tmp_immobile = kwargs.pop('pk_tmp', None)
        self.proprietario = kwargs.pop('proprietario', None)
        print("USER")
        print(self.proprietario)
        super().__init__(*args, **kwargs)
        debug_info(self,*args, **kwargs)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'testo',
            'stelline',
            Submit('submit', 'Invia Recensione')
            )
        debug_info(self.data)
        print(self.is_bound,self.is_valid())
        if self.is_bound:
            testo = self.cleaned_data.get('testo')
            stelline = self.cleaned_data.get('stelline')
            userobj=get_object_or_404(User, username=self.username_tmp)
            userobj=get_object_or_404(UserProfile, user=userobj)
            immobile=get_object_or_404(Immobile, pk=self.pk_tmp_immobile)
            if immobile and userobj and testo and stelline:
                self.recensione = Recensione.objects.create(
                            immobile=immobile,
                            utente=userobj,
                            testo=testo,
                            stelline=stelline
                        )
                self.recensione.save()
            debug_info(self,"END recensione")
