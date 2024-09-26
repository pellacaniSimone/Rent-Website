from django.db import models
#from django.contrib.auth.models import User
# Create your models here.

from immobile.models import Immobile
from utenti.models import UserProfile,User

#####################################################################################
#               recensione
#####################################################################################


class Recensione(models.Model):
    utente = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    immobile = models.ForeignKey(Immobile, on_delete=models.CASCADE)
    testo = models.TextField()
    stelline = models.IntegerField(choices=[(i, str(i)) for i in range(0, 5)])

    def __str__(self):
        return f"Recensione di {self.immobile} di {self.utente}"
        
    class Meta:
        verbose_name_plural = "recensioni"