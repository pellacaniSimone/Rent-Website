from faker import Faker
from django.utils import timezone
import random
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from immobile.models import Immobile
from utenti.models import Proprietario,UserProfile #,Cliente
from prenotazione.models import Prenotazione
from sopraluogo.models import Sopraluogo
from zone.models import Zona
#######################################################################
#--------------------------- Models Dati -----------------------------#
#######################################################################


class DataCreation:
    fake = Faker()
    def random_datetime_in_past(self):
        now = timezone.now()
        delta_days = random.randint(1, 5)
        return now - timedelta(days=delta_days)
    def crea_indirizzo(self):
        ls=[]
        ls=Zona.objects.all()
        ls = [x for x in ls if x.tipo=="Indirizzo"]
        if not ls:
            ls.append (Zona.objects.create(
                nome=self.fake.street_address(),
                latitudine=random.uniform(-90, 90),
                longitudine=random.uniform(-180, 180),
                tipo="Indirizzo"
            ))
        return random.choice(ls)
    def crea_utente(self,username=None,password=None):
        user=User.objects.create_user(
            username=self.fake.user_name() if username ==None else username, 
            email=self.fake.email(), 
            password=self.fake.password() if password ==None else password,
        )
        return UserProfile.objects.create(
            user=user,
            is_confirmed=True
        ) 

    def crea_proprietario(self, username=None,password=None):
        return  Proprietario.objects.create (
            user=self.crea_utente(username,password),
            indirizzo=self.crea_indirizzo(),
            numero_telefono=self.fake.phone_number()
        )
    def crea_immobile(self, name=None):
        return Immobile.objects.create(
                    proprietario=self.crea_proprietario(name),
                    nome="Casa di Test",
                    prezzo=random.uniform(10000, 500000),
                    indirizzo=self.crea_indirizzo(),
                    data_creazione=self.random_datetime_in_past(),
                    confermato_da_admin=True
                )
    def crea_prenotazione(self, cliente=None,proprietario=None, 
                          data_prenotazione=None,durata=None):
        du_p= timezone.now() - timedelta(days=300) if data_prenotazione is None else data_prenotazione
        dur= random.randint(15, 30) if durata is None else durata
        return  Prenotazione.objects.create(
                utente=self.crea_utente(cliente),
                immobile=self.crea_immobile(proprietario),
                data_prenotazione= du_p, # for demo pourpose
                durata=dur
            )
    def crea_zona(self,data):
        nome=self.fake.street_address()
        latitudine=random.uniform(-90, 90)
        longitudine=random.uniform(-180, 180)
        tipo="Indirizzo"
        if data==None:
            data={"nome":nome,
              "latitudine":latitudine,
              "longitudine":longitudine,
              "tipo":tipo}
        return Zona.objects.create(data )

    def crea_utente_confermato(self,user_tag=None):
        user = self.utente_base_e_gruppo(user_tag)
        registrato = UserProfile.objects.create(
            user=user,
            is_confirmed=True
        ) 
        return registrato


    def crea_sopraluogo(self):
        return Sopraluogo.objects.create(
            utente=self.crea_utente_confermato(),
            immobile=self.crea_immobile(),
            data_ora_sopraluogo=timezone.now() + timedelta(days=random.randint(1, 30)),
            durata_h=random.randint(1, 2),
            note_proprietario=self.fake.text(),
        )
    
    def crea_gruppo(self,nome):
        group, created = Group.objects.get_or_create(name=nome)
        if created:
            print(f"Gruppo '{nome}' creato con successo.")
        else:
            print(f"Il gruppo '{nome}' esiste già nel database.")

    def crea_gruppi(self,):

        gl=['Confermato','Proprietario']
        for i in gl:
            self.crea_gruppo(i)

    def utente_base_e_gruppo(self,user_tag=None):
        username = self.fake.user_name() 
        email = self.fake.email()
        password = self.fake.password() 
        user = User.objects.create_user(username=username, email=email, password=password)
        confirmed=False
        if user_tag in ["02","03"]:
            g = Group.objects.get(name="Confermato") 
            g.user_set.add(user)
            confirmed=True
        if user_tag in ["03"]:
            print("Creazione Proprietario")
            g = Group.objects.get(name="Proprietario")
            g.user_set.add(user)
            confirmed=True
        return user