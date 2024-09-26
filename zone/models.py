from django.db import models
from math import radians, sin, cos, sqrt, atan2


#####################################################################################
#               zona
#####################################################################################

class Zona(models.Model):
    TIPI_PERMESSI=["Stato","Regione","Provincia","Comune","Indirizzo"]
    confinanti = models.ManyToManyField('self', symmetrical=True, blank=True )
    soprazona = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='zona_confinanti') 
    nome = models.CharField(max_length=100,null=False) 
    latitudine = models.DecimalField(max_digits=9, decimal_places=6) 
    longitudine = models.DecimalField(max_digits=9, decimal_places=6) 
    tipo = models.CharField(max_length=20,null=False) 

    def __str__(self):
        return self.nome
    
    @property
    def is_indirizzo(self):
        return True if self.tipo=="Indirizzo" else False
    @property
    def is_comune(self):
        return True if self.tipo=="Comune" else False
    @property
    def is_provincia(self):
        return True if self.tipo=="Provincia" else False
    @property
    def is_regione(self):
        return True if self.tipo=="Regione" else False
    @property
    def is_stato(self):
        return True if self.tipo=="Stato" else False


    @classmethod
    def __new_zone(cls, nome=None, latitudine=None, longitudine=None, confinanti=None, soprazona=None, tipo=None):
        return cls.objects.create(nome=nome, latitudine=latitudine, longitudine=longitudine, confinanti=confinanti, soprazona=soprazona, tipo=tipo)

    def aggiungi_soprazona(self,nuova=None,nome=None, latitudine=None, longitudine=None, confinanti=None, soprazona=None, tipo=None):
        if not nuova:
            nuova = self.__new_zone(nome=nome, latitudine=latitudine, longitudine=longitudine, confinanti=confinanti, soprazona=soprazona, tipo=tipo)
        self.soprazona=nuova
        return nuova

    def aggiungi_confinanti(self,nuova=None,nome=None, latitudine=None, longitudine=None, confinanti=None, soprazona=None, tipo=None):
        if not nuova:
            nuova = self.__new_zone(nome=nome, latitudine=latitudine, longitudine=longitudine, confinanti=confinanti, soprazona=soprazona, tipo=tipo)
        self.confinanti.add(nuova)
        return nuova

    def calcola_distanza(self, altra_zona):
        diametro_terra= 12742.0
        raggio_terra_km = diametro_terra /2
        # radiant conversion
        lat1, lon1, lat2, lon2 = map(radians, [self.latitudine, self.longitudine, altra_zona.latitudine, altra_zona.longitudine])
        dlon = lon2 - lon1
        dlat = lat2 - lat1  # Haversine formula
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distanza_km = raggio_terra_km * c
        return distanza_km
    

