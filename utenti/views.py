#####################################################################################
#               imports
#####################################################################################
from dashboard.debug_utils import debug_info
import inspect
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms import BaseForm
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse_lazy,reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import ConfirmAccountForm

from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView


from django.http import HttpRequest, HttpResponseRedirect

from .models import (
    UserProfile
)


from .forms import (
    ConfermaUtenteProprietarioForm,
    UserSettingsForm,
    CreaUtenteForm,
    )



#####################################################################################
#               Guest registration
#####################################################################################


class UserCreateView(SuccessMessageMixin,CreateView):
    form_class = CreaUtenteForm
    template_name = "utenti/user_create.html"
    success_url = reverse_lazy("login")
    success_message = "Utente creato con successo! Effettua il login per accedere."



#####################################################################################
#               Instription: registration confirm
#####################################################################################


class ConfirmAccountView(LoginRequiredMixin,CreateView,SuccessMessageMixin):
    template_name = 'confirm_account.html'
    form_class = ConfirmAccountForm
    success_message = "Conferma registrazione avvenuta con successo!"
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        """Intercatta username da request"""
        debug_info(self)
        form_kwargs = super().get_form_kwargs()
        form_kwargs['username'] = self.request.user.username
        return form_kwargs

    def form_valid(self, form):
        """gestisce salvataggio form"""
        debug_info(self)
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        debug_info(self)
        return super().form_invalid(form)
    

#####################################################################################
#               Staff: Zona setting, confirm owner
#####################################################################################



class ProprietarioConfermaView(PermissionRequiredMixin, UserCreateView,SuccessMessageMixin,):
    """Attivazione utente Proprietario (da root)"""
    form_class = ConfermaUtenteProprietarioForm
    title = "Aggiungi un Proprietario di immobili"
    template_name = "utenti/user_Proprietario_create.html"
    success_url = reverse_lazy("utenti:register_pro")
    permission_required = "is_staff" 
    success_message = "Proprietario creato con successo!"


#####################################################################################
#               Iscritti: conferma iscrizione, profilo, home users_dashboard
#####################################################################################

class UserSettingsView(DetailView):
    model = User
    form_class = UserSettingsForm  # Add form Class
    title = "User settings"
    template_name = 'utenti/user_detail.html'  # Here your template name for html detail rendering
    context_object_name = 'user' # call from the template

    def get_object(self, queryset=None):
        debug_info(self)
        """Restituisce l'oggetto utente corrente"""
        return self.request.user

    @method_decorator(login_required)
    def get_form_kwargs(self):
        """
            passare l'utente corrente al form quando lo istanzio
            Serve per non inserire l'utente corrente nella registrazione 
            di immobili
            (ogni utente si intesisce i suoi) 
        """
        debug_info(self)
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_object()  # send current user ad form class
        return kwargs

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        debug_info(self)
        if request.method == "POST":
            return self.post(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        debug_info(self)
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context

    def get(self, request, *args, **kwargs):
        debug_info(self)
        return  render(request, '404.html', status=404)
    
    def post(self, request, *args, **kwargs):
        debug_info(self)
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        debug_info(self)
        return reverse('utenti:userdetail', args=[self.object.pk])


