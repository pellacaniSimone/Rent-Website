from django.test import TestCase

# Create your tests here.

from dashboard.tests import DataCreation

#######################################################################
#--------------------------- Models Test -----------------------------#
#######################################################################



class ImmobileModelTest(TestCase):
    dt=DataCreation()
    @classmethod
    def setUpTestData(cls):
        cls.dt.crea_immobile()

    def test_disponibile_method(self):
        immobile = self.dt.crea_immobile()
        self.assertTrue(immobile.disponibile)

    def test_immobile_str(self):
        immobile = self.dt.crea_immobile()
        expected_str = f"{immobile.nome} di {immobile.indirizzo} costo giornaliero € {immobile.prezzo}"
        self.assertEqual(str(immobile), expected_str)

