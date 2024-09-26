from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

# Create your tests here.

from dashboard.tests import DataCreation

#######################################################################
#--------------------------- Models Test -----------------------------#
#######################################################################


class SopraluogoModelTest(TestCase):
    dt=DataCreation()
    @classmethod
    def setUpTestData(cls):
        cls.dt.crea_sopraluogo()


    def test_sopraluogo_str(self):
        sopraluogo = self.dt.crea_sopraluogo()
        expected_str = f"Sopraluogo di {sopraluogo.immobile.nome} di {sopraluogo.immobile.indirizzo} "
        self.assertEqual(str(sopraluogo), expected_str)
