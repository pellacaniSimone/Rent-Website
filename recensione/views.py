#####################################################################################
#               imports
#####################################################################################
from dashboard.debug_utils import debug_info
from django.shortcuts import redirect,render
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RecensioneForm
from django.views.generic.edit import FormView
from django.urls import reverse
from recensione.models import Recensione
#####################################################################################
#               Utente Cliente
#####################################################################################


class AggiungiRecensioneView(FormView):

    template_name = 'aggiungi_recensione.html'
    form_class = RecensioneForm
    def dispatch(self, *args,**kwargs):
        """Gestione Autorizzazione"""
        debug_info(self,self.request)
        gperm=self.request.user.groups.filter(name="Confermato").exists()
        staff=self.request.user.is_staff
        anon=True if str(self.request.user)=="AnonymousUser" else False
        if anon :
            return self.red_login()
        elif gperm or staff:# normal use
            if self.request.method == 'POST':
                print("POST branch")
                return self.get(self.request, *args, **kwargs) #normal
        else:
            url = reverse('page_not_found') # 
            return redirect(url, request=self.request, request_method='POST',*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            print("POST branch")
            prop=self.request.user.groups.filter(name="Proprietario").exists()
            print("HERE")
            if prop:
                kwargs["proprietario"]="proprietario"
            print(kwargs["proprietario"])
            kwargs['username_tmp'] = self.request.user.username  # Passa l'utente corrente al form
            kwargs['pk_tmp']=self.kwargs['pk']
            debug_info(self,kwargs)
            self.template_name = 'aggiungi_recensione.html'
            return kwargs

    def red_login(self):
        debug_info(self)
        url = reverse('utenti:login')
        url_with_params = f"{url}?auth=notok"
        return redirect(url_with_params, request_method='POST')






