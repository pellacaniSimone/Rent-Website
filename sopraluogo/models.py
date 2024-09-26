from django.db import models
from immobile.models import Immobile
from utenti.models import UserProfile
from django.utils import timezone
from datetime import  timedelta
from calendar import HTMLCalendar

#####################################################################################
#               sopraluogo
#####################################################################################


class Sopraluogo(models.Model):
    
    utente = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name="sopraluoghi_utente")
    immobile = models.ForeignKey(Immobile,on_delete=models.CASCADE,related_name="sopraluoghi")
    data_ora_sopraluogo = models.DateTimeField(default=timezone.now)
    durata_h = models.PositiveIntegerField(default=1)
    note_proprietario = models.TextField(null=True)

    def __str__(self):
        return f"Sopraluogo di {self.immobile.nome} di {self.immobile.indirizzo} "
    class Meta:
        verbose_name_plural = "Sopraluoghi"

