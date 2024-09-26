#####################################################################################
#               imports
#####################################################################################
from dashboard.debug_utils import debug_info
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .forms import (
    PrenotazioneCreateForm,
    )

from utenti.models import UserProfile,Proprietario
from immobile.models import Immobile
from .models import Prenotazione
#####################################################################################
#               Utente Cliente
#####################################################################################

class PrenotazioneCreateView(CreateView):
    model = Prenotazione
    form_class = PrenotazioneCreateForm
    title = "Aggiungi una prenotazione"
    template_name = "prenotazione_form.html"
    success_url = reverse_lazy("home")
    success_message = "Prenotazione creata con successo!"
    
    def form_valid(self, form,*args,**kwargs):
        """gestisce salvataggio form"""
        debug_info(self)
        id_imm=self.kwargs.get('pk')
        username=self.request.user
        userobj=get_object_or_404(User, username=username)
        prenotazione = form.save(commit=False)
        prenotazione.utente=get_object_or_404(UserProfile, user=userobj)
        prenotazione.immobile=get_object_or_404(Immobile, pk=id_imm)
        print(prenotazione)
        prenotazione.save()
        return super().form_valid(form)


class PrenotazioniClienteListView(ListView):
    model = Prenotazione
    template_name = 'cliente_prenotazioni_list.html'  
    def get_context_data(self, **kwargs):
        debug_info(self)
        context = super().get_context_data(**kwargs)
        prenotazioni = Prenotazione.objects.filter(utente=self.request.user)
        context['prenotazione'] = prenotazioni
        return context
    def post(self, request):
        debug_info(self)
        user_profile = UserProfile.objects.get(user=self.request.user)  # Ottieni il profilo utente
        prenotazioni = Prenotazione.objects.filter(utente=user_profile)
        for i in prenotazioni:
            debug_info(self, i.attiva)
        ctx = {"prenots": prenotazioni}
        #debug_info(self,user_profile,prenotazioni)
        return render(request, self.template_name, ctx)


#####################################################################################
#               Utente Proprietario
#####################################################################################

import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np


class AffittiProprietarioListView(ListView):
    template_name = 'affitti_proprietario_list.html'  # Nome del template da utilizzare
    def get_queryset(self):
        debug_info(self,self.request.user)
        user_profile = UserProfile.objects.get(user=self.request.user)
        proprietario = Proprietario.objects.get(user=user_profile)
        queryset = Immobile.objects.filter(proprietario=proprietario)
        return queryset

    def get_context_data(self, **kwargs):
        debug_info(self)
        context = super().get_context_data(**kwargs)
        immobili = self.get_queryset()
        situazione_affitti = []
        for immobile in immobili:
            prenotazioni = Prenotazione.objects.filter(immobile=immobile)
            situazione_affitti.append({
                'immobile': immobile,
                'prenotazioni': prenotazioni,
            })
        context['situazione_affitti'] = situazione_affitti
        context['grafico_conteggi_prenot_totali'] , context['grafico_distinta_prenotazioni'] = self.crea_grafico(situazione_affitti)
        return context

    def crea_grafico(self, situazione_affitti):
        debug_info(self)
        labels = []
        attive_counts = []
        passate_counts = []
        future_counts = []

        conteggi_prenot_totali=[]
        prenot=[]
        for item in situazione_affitti:
            debug_info(self,item) 
            labels.append(item['immobile'].nome[:5])
            conteggi_prenot_totali.append(item['prenotazioni'].count())
            prenot+=item['prenotazioni'] 

            pr_attive = []
            pr_passate = []
            pr_future = []

            for pos, iter in enumerate(item['prenotazioni']):
                debug_info(self,iter)
                if iter.attiva:
                    pr_attive.append(iter)
                elif iter.passata:
                    pr_passate.append(iter)
                elif iter.futura:
                    pr_future.append(iter)
                else:
                    Exception("Not supported feature")

            attive_counts.append(len(pr_attive))
            passate_counts.append(len(pr_passate))
            future_counts.append(len(pr_future))

        # plot
        fig, ax = plt.subplots()
        ax.bar(labels, conteggi_prenot_totali)
        ax.set_ylabel('Numero di Prenotazioni')
        ax.set_title('Situazione Affitti totali')
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        grafico_conteggi_prenot_totali = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()

        fig, ax = plt.subplots()
        width = 0.15
        num_classi = len(labels)
        posizioni = range(num_classi)
        larghezza_barre = 0.29
        sx=[p - larghezza_barre/2 for p in posizioni]
        cent=[p + larghezza_barre/2 for p in posizioni]
        dx=[p + 3 * larghezza_barre/2 for p in posizioni]
        ax.bar(sx, passate_counts, width=width, label='Passate')
        ax.bar(cent, attive_counts, width=width, label='Attive')
        ax.bar(dx, future_counts, width=width,  label='Future')
        ax.set_xticks([p for p in posizioni])
        ax.set_xticklabels(labels)
        ax.set_ylabel('Numero di Prenotazioni')
        ax.set_title('Situazione Affitti per tipologia')
        ax.legend()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        grafico_distinta_prenotazioni = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()

        return grafico_conteggi_prenot_totali, grafico_distinta_prenotazioni
