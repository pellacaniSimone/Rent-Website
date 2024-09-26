#####################################################################################
#               imports
#####################################################################################
from dashboard.debug_utils import debug_info
from django.urls import reverse

from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin


from utenti.models import UserProfile




#####################################################################################
#               Front page guest, vetrina
#####################################################################################

class RentHomeView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            return self.post(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)
        
    @method_decorator(login_required)
    def post(self, request):
        return render(request, template_name="dashboard.html")
    def get(self, request):
        return render(request, template_name="home.html")



#####################################################################################
#               Iscritti: conferma iscrizione, profilo, home users_dashboard
#####################################################################################
class DashboardHomeView(PermissionRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        debug_info(self)
        gperm=request.user.groups.filter(name="Confermato").exists()
        staff=request.user.is_staff
        user=request.user
        user_obj=False
        if str(user)!="AnonymousUser"  and not staff :
            user_obj = get_object_or_404( UserProfile ,user=request.user )
        debug_info(self)
        if staff or gperm or (user_obj and user_obj.is_confirmed): # normal use
            return self.normal(request, *args, **kwargs)
        elif str(user)=="AnonymousUser" :
            return self.red_login(request, *args, **kwargs)
        elif not gperm and not user_obj.is_confirmed :
            return self.confirm(request, *args, **kwargs)
        else : 
            return self.normal(request, *args, **kwargs)
        
    def red_login(self, request,*args, **kwargs):
        """ 
            Utente non autenticato
            compare il messaggio 
            Si è arrivati qui in quanto non si dispone 
            dei permessi necessari per il servizio scelto!
        """
        debug_info(self)
        url = reverse('utenti:login')
        url_with_params = f"{url}?auth=notok"
        return redirect(url_with_params, request=request, request_method='GET',*args, **kwargs)

    def confirm(self, request,*args, **kwargs): # confirm_account
        """ 
            Utente autenticato
            Conferma di autenticazione
        """
        debug_info(self)
        url = reverse('utenti:confirm_account')
        url_with_params = f"{url}?auth=confirm"
        return redirect(url_with_params, request=request, request_method='GET',*args, **kwargs)
    
    def normal(self, request,*args, **kwargs): # confirm_account
        debug_info(self)
        return render(request, template_name="dashboard.html") #POST