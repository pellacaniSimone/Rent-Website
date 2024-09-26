from django.db import models

# Create your models here.
#from django.contrib.auth.models import User

from immobile.models import Immobile
from utenti.models import UserProfile


from django.utils import timezone
from datetime import datetime, timedelta


#####################################################################################
#               prenotazione
#####################################################################################


class Prenotazione(models.Model):
    utente = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name="prenotazioni_utente")
    immobile = models.ForeignKey(Immobile,on_delete=models.CASCADE,related_name="prenotazioni")
    data_prenotazione = models.DateField(default=timezone.now)
    durata = models.PositiveIntegerField(default=15)
    # timing fix
    @property
    def termine(self):
        return datetime.combine(self.data_prenotazione, datetime.min.time()) + timedelta(days=self.durata)

    @property
    def adesso(self):
        return timezone.now().date()

    @property
    def attiva(self):
        """Adesso() è nella durata di tempo della prenotazione"""
        if self.data_prenotazione  <= timezone.now().date() and timezone.now().date() < self.termine.date():
            return True
        return False

    @property
    def passata(self):
        """Adesso() è nel futuro rispetto alla durata di tempo della prenotazione
        Si è già conclusa
        """
        if self.adesso > self.termine.date():
            return True
        return False 
    
    @property
    def futura(self):
        """Adesso() è nel passato rispetto alla durata di tempo della prenotazione
        deve ancora iniziare
        """
        if self.adesso < self.data_prenotazione:
            return True
        return False

    def __str__(self):
        return f"Prenotazione di {self.immobile.nome} di {self.immobile.indirizzo} affittato dal {str(self.data_prenotazione)} per {self.durata} giorni"

    class Meta:
        verbose_name_plural = "Prenotazioni"

