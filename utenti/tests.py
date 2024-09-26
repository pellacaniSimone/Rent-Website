from django.test import TestCase

# Create your tests here.

from dashboard.tests import DataCreation

#######################################################################
#--------------------------- Models Test -----------------------------#
#######################################################################


class ProprietarioModelTest(TestCase):
    dt=DataCreation()
    @classmethod
    def setUpTestData(cls):
        cls.dt.crea_proprietario()

    def test_proprietario_str(self):
        proprietario = self.dt.crea_proprietario()
        expected_str = f"{proprietario.user.user.username} - {proprietario.indirizzo.nome} - {proprietario.numero_telefono}"
        self.assertEqual(str(proprietario), expected_str)

