from dashboard.debug_utils import debug_info
from django.shortcuts import render

from django.views.generic import ListView, View,DetailView
from django.shortcuts import redirect, HttpResponse
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.db.models import Count
from django.db.models.functions import Random
from django.db.models import Prefetch, OuterRef, Subquery

# Create your views here.
from django.views.generic import FormView

from .forms import (
    CreateImmobileForm,
    SelezionaImmobileForm,
)
from zone.models import Zona
from .models import Immobile
from recensione.models import  Recensione
from recensione.forms import RecensioneForm
from prenotazione.models import  Prenotazione
from django.db.models import Q
from django.views.generic import TemplateView
#####################################################################################
#               Guest: visualizza lista e ricerca
#####################################################################################


class ImmobileListView(ListView):
    nome = "Le nostre offerte affitti contengono"
    context_object_name = 'Appartamenti list'
    model = Immobile
    template_name = "lista_immobili.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(num_prenotazioni=Count('prenotazioni'))
        queryset = queryset.annotate(num_sopraluoghi=Count('sopraluoghi'))
        queryset = queryset.order_by('-num_prenotazioni','num_sopraluoghi')
        return queryset


class AdvancedSearchImmobileView(TemplateView):
    template_name = 'ricerca_Avanzata.html'

    def get(self, request):
        debug_info(self)
        name_query =  request.GET.get('name_query', '') 
        add_query  =  request.GET.get('add_query',  '') # pk
        min_query  =  request.GET.get('min_query',  '') 
        min_query  =  float(min_query) if min_query else 0.0
        max_query  =  request.GET.get('max_query',  '')
        max_query  =  float(max_query) if max_query else 0.0

        immobili = Immobile.objects.all()
        filters = Q()  

        if name_query:
            filters &= Q(nome__icontains=name_query)
        if add_query:
            filters &= Q(indirizzo_id=add_query)
            indirizzo_selezionato = Zona.objects.get(pk=add_query,tipo="Indirizzo")
            distanze_immobili = {immobile.pk: indirizzo_selezionato.calcola_distanza(immobile.indirizzo) for immobile in immobili}
            immobili_dis = sorted(immobili, key=lambda x: distanze_immobili[x.pk])
            primi_tre_immobili = immobili_dis[:3]
            filters |= Q(pk__in=[immobile.pk for immobile in primi_tre_immobili])
            debug_info(self,filters,primi_tre_immobili)

        if min_query > 0 and min_query < 50000:
            filters &= Q(prezzo__gte=min_query)
        if max_query > 0 and max_query < 50000:
            filters &= Q(prezzo__lte=max_query)
        debug_info(self,filters)
        immobili = immobili.filter(filters) if filters else None
        # unifica
        immobili = list(set(immobili if immobili else []))
        addresses = Zona.objects.filter(tipo="Indirizzo")  
        context = { "immobili": immobili, "addresses":addresses }
        debug_info(self,context)
        return render(request, "ricerca_Avanzata.html", context=context)



#####################################################################################
#               registrato confermato: dettaglio immobile, ricerca avanzata
#####################################################################################




class ImmobileDetailView(DetailView):
    """Nessun form associato, ma per le recensioni, RecensioneForm"""
    nome = "Riepilogo "
    model = Immobile
    template_name = 'immobile_detail.html' 
    context_object_name = 'Appartamento detail' 
    def __init__(self,*args , **kwargs) -> None:
        debug_info(self)
        super().__init__(*args,**kwargs)
    def dispatch(self, *args,**kwargs):
        debug_info(self)
        gperm=self.request.user.groups.filter(name="Confermato").exists()
        staff=self.request.user.is_staff
        anon=True if str(self.request.user)=="AnonymousUser" else False
        debug_info(self,gperm,staff,anon,self.request.user)
        if anon :
            return self.red_login()
        elif gperm or staff:# normal use
            return self.get(self.request, *args, **kwargs)
        else:
            url = reverse('page_not_found') # 
            return redirect(url, request=self.request, request_method='GET',*args, **kwargs)
    def get_context_data(self, **kwargs):
        debug_info(self)
        context = super().get_context_data(**kwargs)
        # aggiungi recensione
        immobile = self.get_object()
        recensioni = Recensione.objects.filter(immobile=immobile)
        context['recensioni'] = recensioni
        context['form'] = RecensioneForm()
        return context
    def get_form_kwargs(self):
        """
            passare l'utente corrente al form quando lo istanzio
            Serve per non inserire l'utente corrente nella registrazione 
            di immobili
            (ogni utente si intesisce i suoi) 
        """
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            print("GET branch")
            kwargs['username_tmp'] = self.request.user.username  # Passa l'utente corrente al form
            kwargs['pk_tmp']=self.kwargs['pk']
            debug_info(self,kwargs)
            return kwargs
        if self.request.method == 'POST':
            print("POST branch")
            debug_info(self,kwargs)
            return kwargs

    def red_login(self):
        debug_info(self)
        url = reverse('utenti:login')
        url_with_params = f"{url}?auth=notok"
        return redirect(url_with_params, request_method='GET')




class SelezionaImmobileView(FormView):
    template_name = 'seleziona_immobile.html'
    form_class = SelezionaImmobileForm
    success_url = reverse_lazy('immobile_detail')

    def form_valid(self, form):
        debug_info(self)
        immobile_id = form.cleaned_data['immobile'].id
        self.success_url = reverse_lazy('immobile:immobile_detail', kwargs={'pk': immobile_id})
        return super().form_valid(form)


#####################################################################################
#               proprietario
#####################################################################################



class CreateImmobileView( CreateView,SuccessMessageMixin):
    """Crea immobili"""
    model = Immobile
    form_class = CreateImmobileForm
    title = "Aggiungi un immobile agli affitti"
    template_name = "create_immobile.html"
    success_url = reverse_lazy("immobile:crea_immobile")
    success_message = "Immobile creato con successo!"

    def get_form_kwargs(self):
        """
            passare l'utente corrente al form quando lo istanzio
            Serve per non inserire l'utente corrente nella registrazione 
            di immobili
            (ogni utente si inserisce i suoi) 
        """
        debug_info(self)
        kwargs = super().get_form_kwargs()
        kwargs['username'] = self.request.user.username  # Passa l'utente corrente al form
        return kwargs

