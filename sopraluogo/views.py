#####################################################################################
#               imports
#####################################################################################
from dashboard.debug_utils import debug_info
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from django.urls import reverse_lazy
from .models import Sopraluogo
from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404,redirect
from .forms import (
    SopraluogoCreateForm,
    )
from datetime import datetime,date
from immobile.models import Immobile
from utenti.models import Proprietario,UserProfile
from .utils import Calendar
from .forms import EventForm
from django.utils.safestring import mark_safe

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta, date
import calendar
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#####################################################################################
#               Utente Cliente
#####################################################################################

class SopraluogoCreateView(CreateView):
    """Crea immobili"""
    model = Sopraluogo
    form_class = SopraluogoCreateForm
    title = "Aggiungi una sopraluogo"
    template_name = "sopraluogo_form.html"
    success_url = reverse_lazy("home")
    success_message = "Sopraluogo creata con successo!"
    def form_valid(self, form,*args,**kwargs):
        """gestisce salvataggio form"""
        debug_info(self)
        id_imm=self.kwargs.get('pk')
        username=self.request.user
        userobj=get_object_or_404(User, username=username)
        sopraluogo = form.save(commit=False)
        sopraluogo.utente=get_object_or_404(UserProfile, user=userobj)
        sopraluogo.immobile=get_object_or_404(Immobile, pk=id_imm)
        print(sopraluogo)
        sopraluogo.save()
        return super().form_valid(form)



class CalendarioSopraluoghiView(ListView):
    model = Sopraluogo
    template_name = 'calendario_sopraluoghi.html'

    def dispatch(self, *args,**kwargs):
        """Gestione Autorizzazione"""
        debug_info(self,self.request)
        gperm=self.request.user.groups.filter(name="Proprietario").exists()
        staff=self.request.user.is_staff
        anon=True if str(self.request.user)=="AnonymousUser" else False
        if anon :
            return self.red_login()
        elif gperm or staff:# normal use
            return self.get(self.request, *args, **kwargs) #normal
        else:
            url = reverse('page_not_found') # 
            return redirect(url, request=self.request, request_method='GET',*args, **kwargs)
    def get_context_data(self, **kwargs):
        debug_info(self)
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('day', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

    def red_login(self):
        debug_info(self)
        url = reverse('utenti:login')
        url_with_params = f"{url}?auth=notok"
        return redirect(url_with_params, request_method='GET')


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Sopraluogo()
    if event_id:
        instance = get_object_or_404(Sopraluogo, pk=event_id)
    else:
        instance = Sopraluogo()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'calendario_sopraluoghi.html', {'form': form})