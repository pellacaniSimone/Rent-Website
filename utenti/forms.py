#####################################################################################
#               imports
#####################################################################################
from dashboard.debug_utils import debug_info


from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib.auth.models import Group

from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Field
from crispy_forms.bootstrap import FormActions
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse

from utenti.models import Proprietario #, Cliente
from zone.models import Zona



#####################################################################################
#               Guest: website registration
#####################################################################################

class CreaUtenteForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        user = super().save(commit) #ottengo un riferimento all'utente
        #g = Group.objects.get(name="Iscritti") #cerco il gruppo che mi interessa, dei soli iscritti
        #g.user_set.add(user) # aggiungo l'utente al gruppo
        return user #restituisco quello che il metodo padre di questo metodo avrebbe restituito.




#####################################################################################
#               Registered User: setting User, User Confirmation
#####################################################################################


from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import UserProfile

class ConfirmAccountForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "userconfirm_crispy_form"
    helper.form_method = 'POST'
    helper.add_input(Submit('Conferma', 'Save'))

    def __init__(self, *args, **kwargs):
        debug_info(self)
        self.username = kwargs.pop('username')
        super(ConfirmAccountForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        debug_info(self)
        django_user_obj = get_object_or_404(User, username=self.username)
        custom_user, __created = UserProfile.objects.get_or_create(user=django_user_obj)
        g = Group.objects.get(name="Confermato")
        g.user_set.add(django_user_obj)
        custom_user.is_confirmed = True
        custom_user.user = django_user_obj
        if commit:
            custom_user.save()
        return custom_user

    def get_success_url(self):
        debug_info(self)
        return reverse_lazy("dashboard")

    class Meta:
        model = UserProfile
        fields = ["is_confirmed"]
        widgets = {'is_confirmed': forms.HiddenInput()}




class UserSettingsForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "usersettings_crispy_form"
    helper.form_method = "POST"
    helper.layout = Layout( # substittution# helper.add_input(Submit("submit","modifica settings"))
        Field("username", readonly=True),
        Field("first_name"),
        Field("last_name"),
        Field("email"),
        FormActions(Submit("submit", "Modifica settings") )
    )
    def save(self,commit=True):
        debug_info(self)
        """Usa user e lo usa come id"""
        user = super().save(commit=False)  # get immobile instance without saving
        user.pk = user.pk
        if commit:
            user.save()  # if successful commit then user will be saved
        return user # else return as father method 
    class Meta:
        model = User
        fields = ["username",'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.HiddenInput(),  # hide user field
        }



#####################################################################################
#               Staff: Zona, conferma proprietario
#####################################################################################


class ConfermaUtenteProprietarioForm(forms.ModelForm):
    """Conferma
        TESTATO
    """
    helper = FormHelper()
    helper.form_id = "addproprietario_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Convalida Proprietario"))
    def __init__(self, *args, **kwargs):
        debug_info(self)
        super().__init__(*args, **kwargs)
        self.fields['indirizzo'].queryset = Zona.objects.filter(tipo='Indirizzo')
    def save(self,commit=True):
        debug_info(self)
        proprietario = super().save(commit=False)  # get  owner instance without saving
        user = proprietario.user
        if commit:
            proprietario.save()  # if successful commit then owner will be saved
        g = Group.objects.get(name="Proprietario") # get interested group
        g.user_set.add(user) # add user tp group
        return user # else return as father method.
    class Meta:
        """user appartiene al built-in di django, 
        menu a tendina con il nome dai model"""
        model = Proprietario
        fields = [ 'user','indirizzo']