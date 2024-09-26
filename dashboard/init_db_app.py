
from django.contrib.auth.models import User
from faker import Faker
import random
from datetime import timedelta
from django.utils import timezone



from datetime import timedelta
from django.utils import timezone
from zone.models import Zona
from utenti.models import Proprietario ,UserProfile
from recensione.models import Recensione
from immobile.models import Immobile
from prenotazione.models import Prenotazione
from sopraluogo.models import Sopraluogo

import random
from django.contrib.auth.models import Group

fake = Faker()


def crea_zone():
    # Crea le regioni
    tipi=["Stato","Regione","Provincia","Comune","Indirizzo"]
    print("Crea zone")
    zone_list=[]
    # crea nuove zone
    for _,ty in enumerate(tipi):
        if ty in ["Stato" , "Provincia" , "Regione"]:
            n=3
        elif ty=="Comune":
            n=10
        else : # indirizzo
            n=100
        for _ in range(n):  # Crea 3 regioni
            if ty in ["Stato" , "Provincia" , "Regione"]:
                nome=fake.country(),
            elif ty=="Comune":
                nome=fake.city()
            else : # indirizzo
                nome=fake.street_address()
            zona = Zona.objects.create(
                nome=nome,
                latitudine=random.uniform(-90, 90),
                longitudine=random.uniform(-180, 180),
                tipo=ty
            )
            zone_list.append(zona)
    print("Imposta struttura soprazone-sottozone")
    # logica soprazone
    for _,zona in enumerate(zone_list):
        tipo_zona = zona.tipo
        j=tipi.index(tipo_zona) # recupera l'indice 
        if tipo_zona == "Stato":
            soprazone_disponibili = [z for z in zone_list if z.nome != zona.nome ]  # filtra gli altri stati
        else:
            soprazone_disponibili = [z for z in zone_list if z.tipo == tipi[j-1]]  # soprazone possibili
        soprazona = random.choice(soprazone_disponibili) if soprazone_disponibili else None
        zona.soprazona = soprazona
        zona.save()

    print("Stati confinanti")
    lista_stati=[z for z in zone_list if z.tipo == "Stato" ]
    lista_stati[0].aggiungi_confinanti(lista_stati[1])
    lista_stati[1].aggiungi_confinanti(lista_stati[2])

    print("Liste confinanti")
    lista_regioni=[z for z in zone_list if z.tipo == "Regione" ]
    lista_provincie=[z for z in zone_list if z.tipo == "Provincia" ]
    lista_comuni=[z for z in zone_list if z.tipo == "Comune" ]
    lista_indirizzi=[z for z in zone_list if z.tipo == "Indirizzo" ]
    matrice=[lista_regioni,lista_provincie,lista_comuni,lista_indirizzi]
    # logica confinanti non stati
    scz1=[]
    scz2=[]
    for i,zona1 in enumerate(matrice):
        for j,zona2 in enumerate(zona1):
            if i<j:
                scz1=zona1[i].soprazona.confinanti.all()
            else:
                scz1=[]
            scz2=zona2.soprazona.confinanti.all()
        union=list(set(scz1) & set(scz2))
        for j,zona2 in enumerate(zona1):
            if union: # se la  lista non è vuota allora le 2 zone possono confinare
                if len(scz2)<5: # tiene basso il numero dei confinanti
                    zona2.aggiungi_confinanti(zona1[i])
                    zona2.save()

def random_date():
    tz = timezone.now()
    return tz - timedelta(days=random.randint(1, 365))

def random_datetime_in_past():
    now = timezone.now()
    delta_days = random.randint(1, 5)
    return now - timedelta(days=delta_days)

def indirizzo_casuale():
    tutte_zone = Zona.objects.filter(tipo='Indirizzo')
    return random.choice(tutte_zone)

def crea_gruppo(nome):
    group, created = Group.objects.get_or_create(name=nome)
    if created:
        print(f"Gruppo '{nome}' creato con successo.")
    else:
        print(f"Il gruppo '{nome}' esiste già nel database.")

def crea_gruppi():
    # Codice per creare il gruppo se non esiste
    #gl=['Iscritti','Clienti','Proprietari']
    gl=['Confermato','Proprietario']
    for i in gl:
        crea_gruppo(i)

def utente_di_prova(n=0):
    password="123utente123"
    return f"utentecasuale{n}" , password

def utente_base_e_gruppo(user_tag=None):
    u,p = utente_di_prova(user_tag)
    username = fake.user_name() if user_tag==None else u
    email = fake.email()
    password = fake.password() if user_tag==None else p
    user = User.objects.create_user(username=username, email=email, password=password)
    confirmed=False
    if user_tag in ["02","03"]:
        g = Group.objects.get(name="Confermato") #cerco il gruppo che mi interessa
        g.user_set.add(user)
        confirmed=True
    if user_tag in ["03"]:
        print("Creazione Proprietario")
        g = Group.objects.get(name="Proprietario") #cerco il gruppo che mi interessa
        g.user_set.add(user)
        confirmed=True
    return user

def crea_utente_iscritto(user_tag=None): # senza gruppi
    user = utente_base_e_gruppo(user_tag)
    iscritto = UserProfile.objects.create(
        user=user,
        is_confirmed=False
    ) 
    return iscritto

def crea_utente_confermato(user_tag=None):
    user = utente_base_e_gruppo(user_tag)
    registrato = UserProfile.objects.create(
        user=user,
        is_confirmed=True
    ) 
    return registrato

def crea_proprietario(user_tag=None):
    registrato = crea_utente_confermato(user_tag)
    prop = Proprietario.objects.create(
        user=registrato,
        indirizzo=indirizzo_casuale(),
        numero_telefono=fake.phone_number()
    )
    return  prop


def crea_proprietari_immobili_e_clienti():
    for _ in range(5):
        crea_proprietario()
    for _ in range(10):
        crea_utente_confermato()
    for _ in range(5):
        crea_utente_iscritto()


def sei_confermato(k):
    """Se è il primo immobile l'admin conferma, quindi è random"""
    if k ==1:
        return True
    else:
        return random.choice([True,True,True, False]) 

immobili = [
    {"nome": "Villa Ombrosa", "prezzo": 1200, "zona": "Centro"},
    {"nome": "Appartamento Mare", "prezzo": 1500, "zona": "Mare"},
    {"nome": "Villetta con Giardino", "prezzo": 1800, "zona": "Periferia"},
    {"nome": "Attico Panoramico", "prezzo": 2000, "zona": "Centro"},
    {"nome": "Chalet Montagna", "prezzo": 2500, "zona": "Montagna"},
    {"nome": "Casa Aurora", "prezzo":200 , "zona":"Random"   },
    {"nome": "Loft Serenità", "prezzo":200 , "zona":"Random"   },
    {"nome": "Residenza Verdi Colline", "prezzo":200 , "zona":"Random"   },
    {"nome": "Appartamento Vista Mare", "prezzo":200 , "zona":"Random"   },
    {"nome": "Dimora dei Fiori", "prezzo":200 , "zona":"Random"   },
    {"nome": "Loft Moderno", "prezzo":200 , "zona":"Random"   },
    {"nome": "Villa delle Palme", "prezzo":200 , "zona":"Random"   },
    {"nome": "Casa del Bosco", "prezzo":200 , "zona":"Random"   },
    {"nome": "Suite Eleganza", "prezzo":200 , "zona":"Random"   },
    {"nome": "Appartamento del Sole", "prezzo":200 , "zona":"Random"   },
]



def crea_immobili(tester=False):
    proprietari = Proprietario.objects.all()
    for proprietario in proprietari:
        r_inter=random.randint(3, 5)
        for _ in range(r_inter):
            r = random.randint(0, len(immobili) - 1)
            immobile_data = immobili[r]
            Immobile.objects.create(
                proprietario=proprietario,
                nome=immobile_data["nome"],
                prezzo=random.uniform(25, 300),
                indirizzo=indirizzo_casuale(),
                data_creazione=random_datetime_in_past(),
                confermato_da_admin=sei_confermato(r_inter)
            )


def crea_prenotazioni(tester=False):
    immobili = Immobile.objects.all()
    for immobile in immobili:
        for _ in range(random.randint(1, 8)):
            if immobile.confermato_da_admin:
                durata_prenotazione = random.randint(15, 30)
                Prenotazione.objects.create(
                    utente=crea_utente_confermato(),
                    immobile=immobile,
                    data_prenotazione=timezone.now() + timedelta(days=random.randint(1, 30)) - timedelta(days=random.randint(1, 15)),
                    durata=durata_prenotazione
                )


def crea_recensioni(tester=False):
    immobili = Immobile.objects.all()
    for immobile in immobili:
        for _ in range(random.randint(0, 3)):
            if immobile.confermato_da_admin:
                Recensione.objects.create(
                    utente=crea_utente_confermato(),
                    immobile=immobile,
                    testo=fake.text(),
                    stelline=random.randint(0, 4)
                )

def crea_sopraluoghi(tester=False):
    immobili = Immobile.objects.all()
    for immobile in immobili:
        for _ in range(random.randint(0, 3)):
            if immobile.confermato_da_admin:
                durata_sopraluogo = random.randint(1, 2)
                Sopraluogo.objects.create(
                    utente=crea_utente_confermato(),
                    immobile=immobile,
                    data_ora_sopraluogo=timezone.now() + timedelta(days=random.randint(1, 30)),
                    durata_h=durata_sopraluogo,
                    note_proprietario=fake.text(),
                )




def init_db_sql():
    # crea 3 utenti conosciuti
    crea_zone()
    crea_gruppi()
    crea_utente_iscritto("01") 
    crea_utente_confermato("02") # add is_confirmed
    crea_proprietario("03") 
    crea_proprietari_immobili_e_clienti() # casuali
    crea_immobili()
    crea_prenotazioni()
    crea_recensioni()
    crea_sopraluoghi()
    print("Fine creazione database\n")
