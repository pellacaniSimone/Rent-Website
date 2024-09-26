from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

# Create your tests here.

from dashboard.tests import DataCreation

#######################################################################
#--------------------------- Models Test -----------------------------#
#######################################################################


class PrenotazioneModelTest(TestCase):
    dt=DataCreation()
    @classmethod
    def setUpTestData(cls):
        cls.dt.crea_prenotazione()

    def test_attiva_method(self):
        prenotazione = self.dt.crea_prenotazione()
        near_past = timezone.now() - timedelta(days=1)
        prenotazione.data_prenotazione = near_past
        prenotazione.save()



    def test_prenotazione_str(self):
        prenotazione = self.dt.crea_prenotazione()
        expected_str = f"Prenotazione di {prenotazione.immobile.nome} di {prenotazione.immobile.indirizzo} affittato dal {str(prenotazione.data_prenotazione)} per {prenotazione.durata} giorni"
        self.assertEqual(str(prenotazione), expected_str)







from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from faker import Faker
from immobile.models import  Immobile
from utenti.models import UserProfile, Proprietario
from prenotazione.models import Prenotazione
from .views import AffittiProprietarioListView
from dashboard.tests import DataCreation

fake = Faker()

class AffittiProprietarioListViewTest(TestCase):
    dt=DataCreation()
    @classmethod
    def setUpTestData(cls):
        cls.dt.crea_gruppi()
        cls.user = cls.dt.crea_utente_confermato("02")
        cls.proprietario = cls.dt.crea_proprietario("03")
        cls.dt.crea_immobile()
        cls.dt.crea_prenotazione()

    def setUp(self):
        self.user = self.dt.crea_proprietario(username='testuser', password='password')
        self.client.force_login(self.proprietario.user.user)

    def test_get_queryset(self):
        response = self.client.get(reverse('prenotazione:storico_pro'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)
        queryset = response.context['object_list']
        for immobile in queryset:
            self.assertEqual(immobile.proprietario, self.proprietario)

    def test_get_context_data(self):
        response = self.client.get(reverse('prenotazione:storico_pro'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('situazione_affitti' in response.context)
        situazione_affitti = response.context['situazione_affitti']
        self.assertTrue(isinstance(situazione_affitti, list))
        from django.db.models.query import QuerySet
        for item in situazione_affitti:
            self.assertTrue('immobile' in item)
            self.assertTrue('prenotazioni' in item)
            self.assertTrue(isinstance(item['prenotazioni'], QuerySet))
            for prenotazione in item['prenotazioni']:
                self.assertTrue(isinstance(prenotazione, Prenotazione))
        self.assertTrue('grafico_conteggi_prenot_totali' in response.context)
        self.assertTrue('grafico_distinta_prenotazioni' in response.context)
        self.assertTrue(response.context['grafico_conteggi_prenot_totali'])
        self.assertTrue(response.context['grafico_distinta_prenotazioni'])


class PrenotazioneTestCase(TestCase):
    dt=DataCreation()
    @classmethod
    def setUp(cls):
        cls.data_prenotazione = timezone.now().date()
        cls.durata = 10  # in giorni
        cls.prenotazione_attiva = cls.dt.crea_prenotazione(data_prenotazione=cls.data_prenotazione, durata=cls.durata)
        cls.prenotazione_passata = cls.dt.crea_prenotazione(data_prenotazione=cls.data_prenotazione - timedelta(days=20), durata=cls.durata)
        cls.prenotazione_futura = cls.dt.crea_prenotazione(data_prenotazione=cls.data_prenotazione + timedelta(days=20), durata=cls.durata)

    def test_attiva_property(self):
        self.assertTrue(self.prenotazione_attiva.attiva)
        self.assertFalse(self.prenotazione_passata.attiva)
        self.assertFalse(self.prenotazione_futura.attiva)

    def test_passata_property(self):
        self.assertFalse(self.prenotazione_attiva.passata)
        self.assertTrue(self.prenotazione_passata.passata)
        self.assertFalse(self.prenotazione_futura.passata)

    def test_futura_property(self):
        self.assertFalse(self.prenotazione_attiva.futura)
        self.assertFalse(self.prenotazione_passata.futura)
        self.assertTrue(self.prenotazione_futura.futura)



