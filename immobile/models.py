from django.db import models
from django.utils import timezone
from zone.models import Zona


from utenti.models import Proprietario
from zone.models import Zona

#####################################################################################
#               immobile
#####################################################################################

class Immobile(models.Model):
    proprietario = models.ForeignKey(Proprietario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    indirizzo = models.ForeignKey(Zona, on_delete=models.SET_NULL, null=True, blank=True)
    data_creazione = models.DateTimeField(default=timezone.now)
    confermato_da_admin = models.BooleanField(default=False)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='static/immobili/', blank=True, null=True)


    @property
    def zona_indirizzo(self):
        return self.indirizzo.is_indirizzo

    @property
    def disponibile(self):
        from prenotazione.models import Prenotazione
        list_prenot = Prenotazione.objects.all()
        prenotati=[x.immobile.pk for x in list_prenot if x.attiva ]
        if self.confermato_da_admin and self.pk not in prenotati:
            return True
        return False

    def __str__(self):
        return f"{self.nome} di {self.indirizzo} costo giornaliero € {self.prezzo}"

    class Meta:
        verbose_name_plural = "Immobili"
