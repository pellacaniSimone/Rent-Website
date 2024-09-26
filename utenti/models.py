from django.db import models
from django.contrib.auth.models import User
from zone.models import Zona


# Create your models here.


#####################################################################################
#               registered built in User
#####################################################################################

#####################################################################################
#               client
#####################################################################################


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    @property
    def stampa(self):
        return f"{self.user.username}"
    
    def __str__(self):
        v = "Confermato" if self.is_confirmed else "Da confermare"
        return f"{self.user.username} - {self.user.email} - {v}"
    class Meta:
        verbose_name_plural = "confermati"


#####################################################################################
#               owner user
#####################################################################################

class Proprietario(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    indirizzo = models.ForeignKey(Zona, on_delete=models.CASCADE, null=False)
    numero_telefono = models.CharField(max_length=20, null=False)
    @property
    def zona_indirizzo(self):
        return self.indirizzo.is_indirizzo
    @property
    def stampa(self):
        return f"{self.user.user.username}"
    def __str__(self):
        return f"{self.user.user.username} - {self.indirizzo.nome} - {self.numero_telefono}"
    class Meta:
        verbose_name_plural = "proprietari"