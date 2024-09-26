from django.test import TestCase
from .models import Zona


#######################################################################
#--------------------------- Models Test -----------------------------#
#######################################################################


class ZonaTestCase(TestCase):
    def setUp(self):
        self.zona1 = Zona.objects.create(nome="Zona 1", latitudine=45.0, longitudine=9.0, tipo="Stato")
        self.zona2 = Zona.objects.create(nome="Zona 2", latitudine=46.0, longitudine=10.0, tipo="Regione")
        self.zona3 = Zona.objects.create(nome="Zona 3", latitudine=44.0, longitudine=9.5, tipo="Regione")

    def test_str_method(self):
        self.assertEqual(str(self.zona1), "Zona 1")
        self.assertEqual(str(self.zona2), "Zona 2")
    
    def test_aggiungi_soprazona_method(self):
        self.zona2.aggiungi_soprazona(self.zona1)
        self.assertEqual(self.zona2.soprazona.nome, "Zona 1")
        self.assertEqual(self.zona2.soprazona.tipo, "Stato")
        self.assertEqual(self.zona2.soprazona.pk, 1)  
    
    def test_aggiungi_confinanti_method(self):
        self.zona3.aggiungi_confinanti(self.zona2)
        self.assertIn(self.zona3, self.zona2.confinanti.all())  

  
    def test_calcola_distanza_method(self):
        zona3 = Zona.objects.create(nome="Zona 3", latitudine=47.0, longitudine=11.0, tipo="Comune")
        distanza_km = self.zona1.calcola_distanza(zona3)
        self.assertAlmostEqual(distanza_km, 270.76, places=1)  # Aproximate distancee verification
        distanza_self = self.zona1.calcola_distanza(self.zona1)
        self.assertEqual(distanza_self, 0.0)
        distanza_uguale = self.zona1.calcola_distanza(self.zona1)
        self.assertEqual(distanza_uguale, 0.0)

#######################################################################
#--------------------------- URL Test -----------------------------#
#######################################################################

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from dashboard.tests import DataCreation
from .models import Zona

class ZonaCreateViewTest(TestCase):
    dt=DataCreation()
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.dt.crea_utente(username='testuser', password='12345')

    def test_access_allowed_for_authenticated_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('zone:nuova_zona'))
        self.assertEqual(response.status_code, 200)  # Status code 200 indica successo

    def test_zona_creation(self):
        self.client.login(username='testuser', password='12345')
        data={"nome":"via picchio pazzerello 56",
              "latitudine":44,
              "longitudine":15,
              "tipo":"Indirizzo"}
        response = self.client.post(reverse('zone:nuova_zona'), data)
        self.assertEqual(response.status_code, 302)  # Reindirizza dopo la creazione
        self.assertTrue(Zona.objects.filter(nome='via picchio pazzerello 56').exists())


class ZonaTestDistanza(TestCase):
    def setUp(self):
        self.zona1 = Zona.objects.create(nome="Zona1", latitudine=45.0, longitudine=10.0, tipo="Comune")
        self.zona2 = Zona.objects.create(nome="Zona2", latitudine=46.0, longitudine=11.0, tipo="Comune")
        self.zona3 = Zona.objects.create(nome="Zona3", latitudine=0.0, longitudine=0.0, tipo="Comune")
        self.zona4 = Zona.objects.create(nome="Zona4", latitudine=90.0, longitudine=180.0, tipo="Comune")
        self.zona5 = Zona.objects.create(nome="Zona5", latitudine=-90.0, longitudine=-180.0, tipo="Comune")

    def test_calcola_distanza(self):
        distanza_vicino = self.zona1.calcola_distanza(self.zona2)
        self.assertAlmostEqual(distanza_vicino, 135.786, places=3)
        distanza_stessa_zona = self.zona1.calcola_distanza(self.zona1)
        self.assertEqual(distanza_stessa_zona, 0)
        distanza_limite = self.zona1.calcola_distanza(self.zona3)
        self.assertAlmostEqual(distanza_limite, 5099.84, places=2)
        distanza_limite = self.zona1.calcola_distanza(self.zona4)
        self.assertAlmostEqual(distanza_limite, 5003.77, places=2)
        distanza_limite = self.zona1.calcola_distanza(self.zona5)
        self.assertAlmostEqual(distanza_limite, 15011.32, places=2)
        distanza_limite = self.zona4.calcola_distanza(self.zona5)
        self.assertAlmostEqual(distanza_limite, 20015.086, places=2)
        distanza_limite = self.zona3.calcola_distanza(self.zona5)
        self.assertAlmostEqual(distanza_limite, 10007.543, places=2)
        distanza_limite = self.zona3.calcola_distanza(self.zona4)
        self.assertAlmostEqual(distanza_limite, 10007.543, places=2)

