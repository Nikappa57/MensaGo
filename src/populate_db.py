import os
import random
from datetime import time, timedelta
from decimal import Decimal
from pathlib import Path

import django
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import random
from io import BytesIO

from PIL import Image

from apps.core.models import CustomUser, EconomicalLevel, University
from apps.mensa.models import Allergen, Dish, Includes, Mensa, Menu
# Importazione dei modelli
from apps.mensa.models.City import City
from apps.mensa.models.Events import Event
from apps.mensa.models.Hours import Hours
from apps.mensa.models.Mensa import AmenitiesMensa, Mensa, PhotoMensa
from apps.mensa.models.Review import Review

# Nomi e cognomi italiani per generare utenti casuali
NOMI_ITALIANI = [
    "Marco", "Giuseppe", "Antonio", "Giovanni", "Andrea", "Luigi", "Roberto",
    "Stefano", "Paolo", "Francesco", "Luca", "Alessandro", "Davide", "Matteo",
    "Lorenzo", "Simone", "Riccardo", "Federico", "Daniele", "Massimo",
    "Alessio", "Nicola", "Sergio", "Pietro", "Enrico", "Carlo", "Alberto",
    "Leonardo", "Filippo", "Giacomo", "Michele", "Maria", "Anna", "Francesca",
    "Giulia", "Chiara", "Sara", "Laura", "Valentina", "Martina", "Elena",
    "Giovanna", "Alessandra", "Lucia", "Sofia", "Elisa", "Giorgia", "Paola",
    "Roberta", "Serena", "Silvia", "Federica", "Claudia", "Cristina", "Monica",
    "Michela", "Ilaria", "Caterina", "Camilla", "Irene", "Arianna"
]

COGNOMI_ITALIANI = [
    "Rossi", "Ferrari", "Russo", "Bianchi", "Romano", "Gallo", "Costa",
    "Fontana", "Conti", "Esposito", "Ricci", "Bruno", "De Luca", "Moretti",
    "Marino", "Greco", "Barbieri", "Lombardi", "Giordano", "Colombo",
    "Mancini", "Longo", "Leone", "Martinelli", "Marchetti", "Caruso",
    "Ferrara", "Santoro", "Marini", "Bianco", "Conte", "Serra", "Fabbri",
    "Ferri", "Valentini", "Bellini", "Benedetti", "Martino", "Rizzo",
    "De Santis", "Messina", "Gentile", "Carbone", "Morelli", "Giorgi",
    "Ferraro", "Ferrero", "Testa", "Costantini", "Grassi", "Pellegrini",
    "Palumbo", "Sanna", "Farina"
]


def create_admin_user():
    """Crea un utente admin se non esiste già"""
    User = get_user_model()
    if not User.objects.filter(email="admin@admin.com").exists():
        User.objects.create_superuser(email="admin@admin.com",
                                      password="admin",
                                      first_name="Admin",
                                      last_name="User")
        print("Creato utente admin (admin@admin.com / admin)")
    else:
        print("Utente admin già esistente.")


def create_sample_image(filename, width=800, height=600, color=None):
    """
	Crea un'immagine di esempio con dimensioni e colore specificati
	Salva l'immagine nella cartella appropriata e restituisce il percorso relativo
	Se il file esiste già, lo riusa senza sovrascrivere.
	"""
    # Se il file esiste già, non ricrearlo
    if os.path.exists(filename):
        print(f"Immagine già esistente: {filename}")
        return filename

    try:
        from PIL import Image

        # Crea un'immagine con colore casuale se non specificato
        if color is None:
            color = (random.randint(0, 255), random.randint(0, 255),
                     random.randint(0, 255))

        img = Image.new('RGB', (width, height), color)

        # Crea la directory se non esiste
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Salva l'immagine
        img.save(filename)
        print(f"Creata immagine di esempio: {filename}")
        return filename

    except ImportError:
        print("PIL non installato. Utilizzo placeholder.")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write('placeholder')
        return filename


def populate_reviews(min_reviews=5, max_reviews=10):
    """Aggiunge recensioni alle mense"""
    print("\nCreando recensioni...")

    User = get_user_model()
    users = list(CustomUser.objects.all())
    mense = list(Mensa.objects.all())

    if not users:
        print("Nessun utente trovato, creo nuovi utenti...")
        users = populate_users(30)  # Crea 30 utenti se non ce ne sono

    if not users or not mense:
        print("Nessun utente o mensa trovata, salto le reviews.")
        return

    # Recensioni varie di esempio per generare testi plausibili
    recensioni_positive = [
        "Ottimo servizio e cibo di qualità. Altamente consigliato per gli studenti che cercano un pasto veloce ma gustoso.",
        "Il rapporto qualità-prezzo è eccezionale. I piatti sono sempre freschi e il personale molto cordiale.",
        "Un ambiente pulito e ben organizzato. Code veloci anche nelle ore di punta.",
        "Varietà di scelta notevole, anche per vegani e vegetariani. Complimenti!",
        "Porzioni abbondanti e cibo sempre fresco. Il mio posto preferito per pranzo.",
        "Personale gentilissimo e servizio rapido. Perfetto per una pausa pranzo.",
        "Finalmente una mensa universitaria con opzioni salutari e gustose.",
        "Piatti ben preparati e presentati. Si vede la cura nella scelta degli ingredienti.",
        "Anche se affollata, l'organizzazione è efficiente. Non si aspetta mai troppo.",
        "Buona varietà di primi e secondi, sempre ben cucinati."
    ]

    recensioni_medie = [
        "Servizio nella media. Alcune volte il cibo è ottimo, altre meno.",
        "Qualità discreta ma a volte le code sono troppo lunghe.",
        "Ci sono giorni migliori e giorni peggiori. Nel complesso accettabile.",
        "Menu poco variato di settimana in settimana, ma comunque di qualità accettabile.",
        "Ambiente un po' rumoroso ma il cibo è discreto.",
        "Prezzi giusti per la qualità offerta, ma si potrebbe migliorare la varietà.",
        "Personale a volte un po' sbrigativo, ma il cibo è nella media.",
        "Luogo comodo per la posizione, ma niente di speciale quanto a qualità.",
        "Porzioni adeguate ma non abbondanti. Buono per un pasto veloce.",
        "Piatti base preparati bene, ma poche specialità o piatti particolari."
    ]

    recensioni_negative = [
        "Servizio lento e cibo spesso freddo. Potrebbe migliorare molto.",
        "Qualità scadente rispetto al prezzo. Non è all'altezza di una mensa universitaria.",
        "Poche opzioni per chi ha intolleranze alimentari. Molto deludente.",
        "Code interminabili e pochi posti a sedere. Organizzazione pessima.",
        "Personale poco attento e a volte scortese. Esperienza da dimenticare.",
        "Menu ripetitivo e poco fantasioso. Mancano alternative interessanti.",
        "Ambiente poco pulito e tavoli spesso sporchi. Da migliorare l'igiene.",
        "Porzioni troppo piccole per il prezzo che si paga.",
        "Qualità degli ingredienti discutibile. Si potrebbero fare scelte migliori.",
        "Troppo rumore e poca organizzazione. Difficile godersi il pasto."
    ]

    # Contatore per le recensioni create
    review_count = 0

    for mensa in mense:
        # Numero casuale di recensioni per questa mensa
        num_reviews = random.randint(min_reviews, max_reviews)
        print(f"Creando {num_reviews} recensioni per {mensa.name}...")

        # Utenti già utilizzati per questa mensa
        users_reviewed = set()

        for i in range(num_reviews):
            # Selezioniamo un utente casuale che non ha ancora recensito questa mensa
            available_users = [u for u in users if u.id not in users_reviewed]
            if not available_users:
                print(
                    f"  Nessun altro utente disponibile per recensire {mensa.name}"
                )
                break

            user = random.choice(available_users)
            users_reviewed.add(user.id)

            # Controlliamo se esiste già una recensione
            if Review.objects.filter(mensa=mensa, user=user).exists():
                continue

            # Generiamo un voto casuale con bias verso le recensioni positive
            stars = random.choices([1, 2, 3, 4, 5], weights=[1, 1, 3, 5, 3])[0]

            # Selezioniamo un testo di recensione appropriato
            if stars >= 4:
                text = random.choice(recensioni_positive)
            elif stars == 3:
                text = random.choice(recensioni_medie)
            else:
                text = random.choice(recensioni_negative)

            # Creiamo la recensione
            Review.objects.create(mensa=mensa,
                                  user=user,
                                  stars=stars,
                                  text=text)
            print(
                f"  ✓ Recensione {stars}★ per {mensa.name} da {user.first_name} {user.last_name}"
            )
            review_count += 1

    print(f"Totale recensioni create: {review_count}")


def populate_cities():
    """Aggiunge alcune città di esempio al database"""
    cities = [
        "Roma", "Milano", "Napoli", "Torino", "Bologna", "Firenze", "Venezia"
    ]
    coords = {
        "Roma": (41.9028, 12.4964),
        "Milano": (45.4642, 9.1900),
        "Napoli": (40.8518, 14.2681),
        "Torino": (45.0703, 7.6869),
        "Bologna": (44.4949, 11.3426),
        "Firenze": (43.7696, 11.2558),
        "Venezia": (45.4408, 12.3155),
    }

    for name in cities:
        city, created = City.objects.get_or_create(name=name)
        # Percorso immagine
        fname = name.lower().replace(' ', '_') + '.jpg'
        rel_path = f"landscapes/{fname}"
        img_path = f"frontend/static/imgs/landscapes/{fname}"

        # Crea immagine se non esiste
        create_sample_image(img_path)

        city.landscape = rel_path
        city.latitude, city.longitude = coords[name]
        city.save()
        print(f"{'Aggiunta' if created else 'Aggiornata'} città: {name}")


def populate_events():
    """Aggiunge alcuni eventi di esempio al database"""
    today = timezone.now().date()
    events = [{
        "name": "Festival Culinario Universitario",
        "desc":
        "Un festival dedicato alla cucina universitaria con stand gastronomici e showcooking.",
        "days_from_now": 5
    }, {
        "name": "Serata Pizza e Birra",
        "desc": "Una serata informale con pizza artigianale e birre locali.",
        "days_from_now": 10
    }, {
        "name": "Incontro con Chef Stellato",
        "desc":
        "Un incontro esclusivo con uno chef stellato che presenterà ricette innovative.",
        "days_from_now": 15
    }, {
        "name": "Degustazione Vini Locali",
        "desc":
        "Degustazione guidata di vini del territorio con sommelier professionisti.",
        "days_from_now": 20
    }, {
        "name": "Serata di Cucina Internazionale",
        "desc":
        "Un viaggio tra i sapori del mondo con piatti tipici di diversi paesi.",
        "days_from_now": 25
    }, {
        "name": "Workshop: Cucina Sostenibile",
        "desc":
        "Laboratorio pratico su tecniche di cucina sostenibile e a basso impatto ambientale.",
        "days_from_now": 30
    }]

    for ev in events:
        date = today + timedelta(days=ev['days_from_now'])
        name = ev['name']
        desc = ev['desc']
        if not Event.objects.filter(name=name, date=date).exists():
            img_fname = name.lower().replace(' ', '_') + '.jpg'
            rel_img = f"events/{img_fname}"
            img_path = f"frontend/static/imgs/events/{img_fname}"

            create_sample_image(img_path)
            Event.objects.create(name=name, desc=desc, date=date, img=rel_img)
            print(f"Aggiunto evento: {name} il {date}")
        else:
            print(f"Evento già esistente: {name} il {date}")


def populate_mense():
    """Aggiunge mense di esempio al database"""
    mense_data = {
        'Milano': [
            {
                'name':
                'Mensa Bicocca',
                'description':
                'Moderna mensa universitaria nel campus Bicocca. Offre un\'ampia varietà di piatti freschi e nutrienti, '
                'con opzioni per diverse esigenze alimentari in un ambiente spazioso e luminoso.',
                'position':
                'Piazza della Scienza 1, Milano',
                'capacity':
                300,
                'phone_number':
                '02123456',
                'email':
                'mensa.bicocca@unimib.it',
                'latitude':
                45.5132,
                'longitude':
                9.2109
            },
            {
                'name':
                'Mensa Statale',
                'description':
                'Mensa centrale dell\'Università degli Studi di Milano. Situata nel cuore storico dell\'ateneo, '
                'offre piatti della tradizione italiana e internazionale in un ambiente ricco di storia e cultura.',
                'position':
                'Via Festa del Perdono 7, Milano',
                'capacity':
                400,
                'phone_number':
                '02654321',
                'email':
                'mensa.statale@unimi.it',
                'latitude':
                45.4598,
                'longitude':
                9.1938
            },
            {
                'name':
                'Mensa Politecnico',
                'description':
                'Mensa del Politecnico di Milano. Spazio moderno e tecnologico che serve centinaia di studenti di ingegneria '
                'e architettura ogni giorno, offrendo pasti bilanciati e opzioni vegetariane e vegane.',
                'position':
                'Piazza Leonardo da Vinci 32, Milano',
                'capacity':
                500,
                'phone_number':
                '02345678',
                'email':
                'mensa.polimi@unimi.it',
                'latitude':
                45.4784,
                'longitude':
                9.2258
            },
            {
                'name':
                'Mensa Città Studi',
                'description':
                'Mensa del quartiere universitario Città Studi. Centro di ritrovo per studenti di diverse facoltà, '
                'con un\'offerta gastronomica varia che spazia dalla cucina tradizionale a piatti innovativi.',
                'position':
                'Via Celoria 2, Milano',
                'capacity':
                350,
                'phone_number':
                '02234567',
                'email':
                'mensa.studi@unimi.it',
                'latitude':
                45.4762,
                'longitude':
                9.2309
            },
            {
                'name':
                'Mensa IULM',
                'description':
                'Mensa dell\'Università IULM. Ambiente contemporaneo e design curato per gli studenti di comunicazione e lingue, '
                'con un menu che riflette la diversità culturale dell\'ateneo e la creatività dei suoi corsi.',
                'position':
                'Via Carlo Bo 1, Milano',
                'capacity':
                200,
                'phone_number':
                '02876543',
                'email':
                'mensa.iulm@unimi.it',
                'latitude':
                45.4439,
                'longitude':
                9.1568
            },
            {
                'name':
                'Mensa Bocconi',
                'description':
                'Mensa dell\'Università Bocconi. Struttura all\'avanguardia con standard elevati di qualità e servizio, '
                'frequentata da studenti di economia e business da tutto il mondo, con un\'offerta gastronomica internazionale.',
                'position':
                'Via Sarfatti 25, Milano',
                'capacity':
                600,
                'phone_number':
                '02712345',
                'email':
                'mensa.boc@unimi.it',
                'latitude':
                45.4507,
                'longitude':
                9.1881
            },
            {
                'name':
                'Mensa NABA',
                'description':
                'Mensa della Nuova Accademia di Belle Arti. Spazio creativo e informale per gli studenti d\'arte e design, '
                'con un\'atmosfera vivace e stimolante, e piatti che combinano tradizione e innovazione culinaria.',
                'position':
                'Via Carlo Darwin 20, Milano',
                'capacity':
                150,
                'phone_number':
                '02345678',
                'email':
                'mensa.naba@unimi.it',
                'latitude':
                45.4647,
                'longitude':
                9.1812
            },
            {
                'name':
                'Mensa San Raffaele',
                'description':
                'Mensa universitaria dell\'Ospedale San Raffaele. Punto di ristoro per studenti di medicina e personale sanitario, '
                'con attenzione particolare alla nutrizione e al benessere, in un contesto di eccellenza medica.',
                'position':
                'Via Olgettina 60, Milano',
                'capacity':
                250,
                'phone_number':
                '02987654',
                'email':
                'mensa.sanraffaele@unimi.it',
                'latitude':
                45.5054,
                'longitude':
                9.2659
            },
            {
                'name':
                'Mensa Cattolica',
                'description':
                'Grande mensa dell\'Università Cattolica del Sacro Cuore. Ampio spazio di ristorazione che unisce tradizione e modernità, '
                'offrendo una vasta gamma di piatti in un ambiente accogliente, nel rispetto dei valori dell\'ateneo.',
                'position':
                'Largo Agostino Gemelli 1, Milano',
                'capacity':
                450,
                'phone_number':
                '02456789',
                'email':
                'mensa.cattolica@unicatt.it',
                'latitude':
                45.4635,
                'longitude':
                9.1756
            },
            {
                'name':
                'Mensa Conservatorio',
                'description':
                'Mensa del Conservatorio Giuseppe Verdi. Luogo di incontro per musicisti e artisti, '
                'caratterizzato da un\'atmosfera rilassante e culturale, con menu che celebrano la tradizione italiana e l\'armonia dei sapori.',
                'position':
                'Via Conservatorio 12, Milano',
                'capacity':
                180,
                'phone_number':
                '02321654',
                'email':
                'mensa.conservatorio@consmilano.it',
                'latitude':
                45.4671,
                'longitude':
                9.2008
            },
        ],
        'Roma': [
            {
                'name':
                'Mensa La Sapienza',
                'description':
                'Mensa principale dell\'Università La Sapienza. Punto di riferimento per migliaia di studenti nel più grande ateneo d\'Europa, '
                'con una vastissima offerta gastronomica che rappresenta la diversità della popolazione studentesca.',
                'position':
                'Piazzale Aldo Moro 5, Roma',
                'capacity':
                500,
                'phone_number':
                '06123456',
                'email':
                'mensa.sapienza@uniroma1.it',
                'latitude':
                41.9021,
                'longitude':
                12.5145
            },
            {
                'name':
                'Mensa Roma Tre',
                'description':
                'Mensa dell\'Università Roma Tre. Struttura moderna nel cuore di Ostiense, '
                'accoglie gli studenti in un ambiente giovane e dinamico con proposte culinarie che bilanciano tradizione romana e cucina internazionale.',
                'position':
                'Via Ostiense 159, Roma',
                'capacity':
                250,
                'phone_number':
                '06654321',
                'email':
                'mensa.romatre@uniroma3.it',
                'latitude':
                41.8578,
                'longitude':
                12.4845
            },
            {
                'name':
                'Mensa Tor Vergata',
                'description':
                'Mensa moderna dell\'Università di Tor Vergata. Situata nel grande campus nell\'area est di Roma, '
                'offre un servizio efficiente e di qualità in un contesto verde e sostenibile, con ampi spazi interni ed esterni.',
                'position':
                'Via Cambridge 115, Roma',
                'capacity':
                350,
                'phone_number':
                '06789123',
                'email':
                'mensa.torvergata@uniroma2.it',
                'latitude':
                41.8539,
                'longitude':
                12.6252
            },
            {
                'name':
                'Mensa LUISS',
                'description':
                'Elegante mensa dell\'Università LUISS. Ambiente raffinato e professionale per gli studenti di questa prestigiosa università privata, '
                'con un\'offerta gastronomica di alto livello che rispecchia lo standard dell\'ateneo.',
                'position':
                'Viale Pola 12, Roma',
                'capacity':
                280,
                'phone_number':
                '06456789',
                'email':
                'mensa.luiss@luiss.it',
                'latitude':
                41.9178,
                'longitude':
                12.5088
            },
            {
                'name':
                'Mensa San Pietro',
                'description':
                'Mensa vicino alla Città del Vaticano. Luogo strategico per studenti e turisti, '
                'offre una vista meravigliosa sulla Basilica e propone piatti della tradizione romana e internazionale in un contesto unico.',
                'position':
                'Via della Conciliazione 4, Roma',
                'capacity':
                200,
                'phone_number':
                '06987654',
                'email':
                'mensa.sanpietro@uniroma3.it',
                'latitude':
                41.9019,
                'longitude':
                12.4614
            },
            {
                'name':
                'Mensa Campus Bio-Medico',
                'description':
                'Mensa specializzata dell\'Università Campus Bio-Medico. Concentrata sulla nutrizione e il benessere, '
                'propone menu bilanciati con ingredienti selezionati, adatti alle esigenze degli studenti di medicina e scienze della salute.',
                'position':
                'Via Álvaro del Portillo 21, Roma',
                'capacity':
                220,
                'phone_number':
                '06654789',
                'email':
                'mensa.biomedico@unicampus.it',
                'latitude':
                41.8020,
                'longitude':
                12.4829
            },
        ],
        'Bologna': [
            {
                'name':
                'Mensa Irnerio',
                'description':
                'Mensa storica dell\'Università di Bologna. Situata nel cuore della zona universitaria, porta il nome del celebre giurista, '
                'offrendo piatti della tradizione emiliana e servizi di alta qualità per studenti dell\'ateneo più antico del mondo.',
                'position':
                'Via Zamboni 33, Bologna',
                'capacity':
                350,
                'phone_number':
                '051123456',
                'email':
                'mensa.irnerio@unibo.it',
                'latitude':
                44.4969,
                'longitude':
                11.3526
            },
            {
                'name':
                'Mensa Ingegneria',
                'description':
                'Mensa della facoltà di Ingegneria. Progettata con criteri funzionali e moderni, '
                'si distingue per l\'efficienza del servizio e i menu appositamente studiati per le lunghe giornate di studio degli studenti di ingegneria.',
                'position':
                'Viale del Risorgimento 2, Bologna',
                'capacity':
                200,
                'phone_number':
                '051654321',
                'email':
                'mensa.ingegneria@unibo.it',
                'latitude':
                44.4876,
                'longitude':
                11.3283
            },
            {
                'name':
                'Mensa Bononia',
                'description':
                'Mensa centrale nel cuore di Bologna. Un punto di ritrovo strategico per tutti gli studenti, '
                'con vista sulla magnifica Piazza Maggiore e un\'offerta gastronomica che celebra la ricca tradizione culinaria bolognese.',
                'position':
                'Piazza Maggiore 6, Bologna',
                'capacity':
                280,
                'phone_number':
                '051789456',
                'email':
                'mensa.bononia@unibo.it',
                'latitude':
                44.4938,
                'longitude':
                11.3426
            },
            {
                'name':
                'Mensa San Vitale',
                'description':
                'Mensa universitaria zona San Vitale. In un palazzo storico ristrutturato, '
                'crea un piacevole contrasto tra antico e moderno, offrendo piatti genuini e servizi attenti alle esigenze degli studenti.',
                'position':
                'Via San Vitale 59, Bologna',
                'capacity':
                190,
                'phone_number':
                '051456123',
                'email':
                'mensa.sanvitale@unibo.it',
                'latitude':
                44.4955,
                'longitude':
                11.3520
            },
            {
                'name':
                'Mensa Due Torri',
                'description':
                'Mensa universitaria vicino alle Due Torri. Con vista sul simbolo della città, '
                'è un ambiente vivace e cosmopolita, frequentato da studenti locali e internazionali che qui trovano un punto di incontro e socializzazione.',
                'position':
                'Strada Maggiore 34, Bologna',
                'capacity':
                230,
                'phone_number':
                '051789123',
                'email':
                'mensa.duetorri@unibo.it',
                'latitude':
                44.4942,
                'longitude':
                11.3469
            },
        ],
        'Firenze': [
            {
                'name':
                'Mensa Calamandrei',
                'description':
                'Mensa centrale dell\'Università di Firenze. Una delle strutture più grandi e moderne del sistema universitario fiorentino, '
                'situata nel polo scientifico e tecnologico, con un\'ampia offerta di piatti della tradizione toscana e nazionale.',
                'position':
                'Viale Morgagni 51, Firenze',
                'capacity':
                300,
                'phone_number':
                '055123456',
                'email':
                'mensa.calamandrei@unifi.it',
                'latitude':
                43.8004,
                'longitude':
                11.2419
            },
            {
                'name':
                'Mensa Santa Marta',
                'description':
                'Mensa universitaria nel complesso di Santa Marta. Incastonata in un edificio storico ristrutturato, '
                'coniuga fascino architettonico e servizi moderni, con un\'attenzione particolare alla qualità e alla varietà dell\'offerta gastronomica.',
                'position':
                'Via Santa Marta 3, Firenze',
                'capacity':
                240,
                'phone_number':
                '055789123',
                'email':
                'mensa.santamarta@unifi.it',
                'latitude':
                43.7975,
                'longitude':
                11.2499
            },
            {
                'name':
                'Mensa Caponnetto',
                'description':
                'Mensa del polo delle scienze sociali. Dedicata agli studenti di giurisprudenza, scienze politiche ed economia, '
                'offre un ambiente stimolante e funzionale con proposte culinarie che variano quotidianamente per soddisfare ogni palato.',
                'position':
                'Via delle Pandette 32, Firenze',
                'capacity':
                220,
                'phone_number':
                '055456789',
                'email':
                'mensa.caponnetto@unifi.it',
                'latitude':
                43.8174,
                'longitude':
                11.2277
            },
            {
                'name':
                'Mensa San Marco',
                'description':
                'Mensa storica nel centro città vicino al Museo di San Marco. Un angolo di tranquillità nel cuore turistico di Firenze, '
                'dove gli studenti possono godere di piatti genuini a prezzi accessibili circondati dalla bellezza del Rinascimento fiorentino.',
                'position':
                'Piazza San Marco 1, Firenze',
                'capacity':
                180,
                'phone_number':
                '055321654',
                'email':
                'mensa.sanmarco@unifi.it',
                'latitude':
                43.7786,
                'longitude':
                11.2593
            },
        ],
        'Torino': [
            {
                'name':
                'Mensa Politecnico',
                'description':
                'Mensa del Politecnico di Torino. Un ampio spazio di ristorazione per gli studenti di ingegneria e architettura, '
                'con servizi efficienti e menu studiati per supportare le lunghe giornate di studio in questo prestigioso ateneo tecnico.',
                'position':
                'Corso Duca degli Abruzzi 24, Torino',
                'capacity':
                400,
                'phone_number':
                '011123456',
                'email':
                'mensa.polito@polito.it',
                'latitude':
                45.0626,
                'longitude':
                7.6620
            },
            {
                'name':
                'Mensa Palazzo Nuovo',
                'description':
                'Mensa universitaria di Palazzo Nuovo. Punto di riferimento per gli studenti di facoltà umanistiche, '
                'offre un\'atmosfera vivace e multiculturale, con proposte culinarie che spaziano dalla tradizione piemontese a piatti internazionali.',
                'position':
                'Via Sant\'Ottavio 20, Torino',
                'capacity':
                280,
                'phone_number':
                '011789456',
                'email':
                'mensa.palazzonuovo@unito.it',
                'latitude':
                45.0678,
                'longitude':
                7.6930
            },
            {
                'name':
                'Mensa Campus Luigi Einaudi',
                'description':
                'Moderna mensa del Campus Luigi Einaudi. Struttura all\'avanguardia in uno dei complessi universitari più recenti della città, '
                'caratterizzata da ampie vetrate e spazi luminosi, con un\'offerta culinaria variata e attenta alla sostenibilità.',
                'position':
                'Lungo Dora Siena 100, Torino',
                'capacity':
                320,
                'phone_number':
                '011456789',
                'email':
                'mensa.cle@unito.it',
                'latitude':
                45.0746,
                'longitude':
                7.6925
            },
            {
                'name':
                'Mensa Valentino',
                'description':
                'Mensa nel complesso del Castello del Valentino. Un\'esperienza unica di ristorazione universitaria all\'interno di un sito UNESCO, '
                'dove gli studenti di architettura possono pranzare immersi nella storia e nell\'eleganza di uno dei simboli di Torino.',
                'position':
                'Viale Mattioli 39, Torino',
                'capacity':
                200,
                'phone_number':
                '011321654',
                'email':
                'mensa.valentino@unito.it',
                'latitude':
                45.0546,
                'longitude':
                7.6871
            },
        ],
        'Napoli': [
            {
                'name':
                'Mensa Federico II',
                'description':
                'Mensa dell\'Università Federico II. Situata nello storico Corso Umberto, serve quotidianamente centinaia di studenti '
                'di uno degli atenei più antichi del mondo, offrendo piatti della tradizione napoletana preparati con ingredienti locali di qualità.',
                'position':
                'Corso Umberto I 40, Napoli',
                'capacity':
                350,
                'phone_number':
                '081123456',
                'email':
                'mensa.federicoii@unina.it',
                'latitude':
                40.8467,
                'longitude':
                14.2596
            },
            {
                'name':
                'Mensa Monte Sant\'Angelo',
                'description':
                'Grande mensa del polo scientifico. Struttura moderna e spaziosa che serve il vasto complesso universitario di Monte Sant\'Angelo, '
                'con un\'organizzazione efficiente che riesce a gestire il grande afflusso di studenti nelle ore di punta.',
                'position':
                'Via Vicinale Cupa Cintia, 1',
                'capacity':
                380,
                'phone_number':
                '081789456',
                'email':
                'mensa.montesantangelo@unina.it',
                'latitude':
                40.8391,
                'longitude':
                14.1828
            },
            {
                'name':
                'Mensa Via Mezzocannone',
                'description':
                'Mensa storica nel centro città. Un punto di ritrovo tradizionale per generazioni di studenti napoletani, '
                'con un\'atmosfera vivace e autentica, dove si possono gustare i sapori della cucina partenopea a prezzi accessibili.',
                'position':
                'Via Mezzocannone 16, Napoli',
                'capacity':
                220,
                'phone_number':
                '081456789',
                'email':
                'mensa.mezzocannone@unina.it',
                'latitude':
                40.8470,
                'longitude':
                14.2525
            },
            {
                'name':
                'Mensa Parthenope',
                'description':
                'Mensa dell\'Università Parthenope. Con una vista spettacolare sul Golfo di Napoli, '
                'offre un\'esperienza unica tra mare e cultura, con un menu che valorizza i prodotti locali e la dieta mediterranea.',
                'position':
                'Via Acton 38, Napoli',
                'capacity':
                200,
                'phone_number':
                '081321654',
                'email':
                'mensa.parthenope@uniparthenope.it',
                'latitude':
                40.8365,
                'longitude':
                14.2520
            },
        ],
        'Venezia': [
            {
                'name':
                'Mensa Rio Novo',
                'description':
                'Mensa universitaria nel cuore di Venezia. Affacciata sul canale di Rio Novo, offre un\'esperienza di ristorazione unica, '
                'dove gli studenti possono mangiare ammirando le gondole che passano, in un perfetto connubio tra utilità e bellezza veneziana.',
                'position':
                'Dorsoduro 3861, Venezia',
                'capacity':
                200,
                'phone_number':
                '041123456',
                'email':
                'mensa.rionovo@unive.it',
                'latitude':
                45.4354,
                'longitude':
                12.3210
            },
            {
                'name':
                'Mensa San Giobbe',
                'description':
                'Mensa del polo economico di Ca\' Foscari. Situata in un edificio storico riqualificato nel sestiere di Cannaregio, '
                'serve principalmente gli studenti di economia con piatti che uniscono tradizione veneta e internazionalità.',
                'position':
                'Cannaregio 873, Venezia',
                'capacity':
                180,
                'phone_number':
                '041789456',
                'email':
                'mensa.sangiobbe@unive.it',
                'latitude':
                45.4442,
                'longitude':
                12.3200
            },
            {
                'name':
                'Mensa Santa Marta',
                'description':
                'Mensa nel complesso di Santa Marta. Un ambiente moderno in un contesto storico, '
                'questa mensa è frequentata soprattutto dagli studenti di scienze, offrendo un menu variato e un\'atmosfera rilassata lontana dal turismo.',
                'position':
                'Dorsoduro 2137, Venezia',
                'capacity':
                150,
                'phone_number':
                '041456789',
                'email':
                'mensa.santamarta@unive.it',
                'latitude':
                45.4326,
                'longitude':
                12.3174
            },
            {
                'name':
                'Mensa IUAV',
                'description':
                'Mensa dell\'Università IUAV. Progettata con un\'attenzione particolare al design e all\'architettura, come si addice a questa università, '
                'offre spazi funzionali e accoglienti dove gli studenti di architettura e design possono ritrovarsi e condividere idee.',
                'position':
                'Santa Croce 191, Venezia',
                'capacity':
                140,
                'phone_number':
                '041321654',
                'email':
                'mensa.iuav@iuav.it',
                'latitude':
                45.4390,
                'longitude':
                12.3241
            },
        ]
    }

    for city_name, mense_list in mense_data.items():
        try:
            city = City.objects.get(name=city_name)
        except City.DoesNotExist:
            print(f"Città {city_name} non trovata, salto...")
            continue

        for m_data in mense_list:
            mensa, created = Mensa.objects.get_or_create(
                name=m_data['name'],
                defaults={
                    'description': m_data['description'],
                    'position': m_data['position'],
                    'capacity': m_data['capacity'],
                    'phone_number': m_data['phone_number'],
                    'email': m_data['email'],
                    'city': city
                })

            # Banner image
            banner_fname = m_data['name'].lower().replace(' ', '_') + '.jpg'
            banner_rel = f"banners/{banner_fname}"
            banner_path = f"uploads/banners/{banner_fname}"

            create_sample_image(banner_path)
            mensa.banner = banner_rel
            mensa.save()

            # Galleria
            for i in range(4):
                img_name = f"{m_data['name'].lower().replace(' ', '-')}{i+1}.jpg"
                rel = f"photos/{img_name}"
                path = f"uploads/photos/{img_name}"
                create_sample_image(path)

                photo, p_created = PhotoMensa.objects.get_or_create(img=rel)
                if not mensa.gallery.filter(pk=photo.pk).exists():
                    mensa.gallery.add(photo)
            mensa.save()

            print(
                f"{'Aggiunta' if created else 'Aggiornata'} mensa: {m_data['name']}"
            )


def create_mensa_gallery(mensa_name, num_images=4):
    photos = []
    for i in range(num_images):
        img_name = f"{mensa_name.lower().replace(' ', '-')}{i+1}.jpg"
        rel = f"photos/{img_name}"
        path = f"uploads/photos/{img_name}"
        create_sample_image(path)
        photo, _ = PhotoMensa.objects.get_or_create(img=rel)
        photos.append(photo)
    return photos


def populate_hours():
    """Aggiunge orari di apertura per tutte le mense"""
    print("\nAggiungendo orari di apertura delle mense...")

    # Elimino eventuali orari esistenti
    Hours.objects.all().delete()

    # Configurazione degli orari per tutte le mense
    mense = Mensa.objects.all()

    for mensa in mense:
        print(f"Configurando orari per: {mensa.name}")

        # Orari di pranzo dal lunedì al venerdì (giorni 0-4)
        for weekday in range(5):
            Hours.objects.create(
                mensa=mensa,
                weekday=weekday,
                daypart=0,  # Pranzo
                open_time=time(11, 30),
                close_time=time(14, 30))

        # Orari di cena dal lunedì al venerdì (giorni 0-4)
        for weekday in range(5):
            Hours.objects.create(
                mensa=mensa,
                weekday=weekday,
                daypart=1,  # Cena
                open_time=time(19, 0),
                close_time=time(22, 0))

        # Alcune mense sono aperte anche il sabato a pranzo (giorno 5)
        if random.random() < 0.7:  # 70% delle mense aperte il sabato a pranzo
            Hours.objects.create(
                mensa=mensa,
                weekday=5,
                daypart=0,  # Pranzo
                open_time=time(11, 30),
                close_time=time(14, 0))
            print(f"  ✓ {mensa.name} aperta il sabato a pranzo")

    print(f"Orari configurati per {mense.count()} mense")


def create_sample_dish_image(path, size=(300, 300)):
    """Crea un'immagine di esempio per un piatto"""
    # Colori appetitosi per i piatti
    colors = [
        (255, 165, 0),  # Arancione (pasta)
        (34, 139, 34),  # Verde (verdure)
        (210, 180, 140),  # Marrone (carne)
        (255, 99, 71),  # Rosso pomodoro
        (255, 255, 0),  # Giallo (formaggi)
        (139, 69, 19),  # Marrone scuro (dolci)
    ]

    # Crea directory se non esiste
    os.makedirs(os.path.dirname(path), exist_ok=True)

    color = random.choice(colors)
    img = Image.new('RGB', size, color=color)
    img.save(path, 'JPEG')
    print(f"Creata immagine: {path}")


def populate_ingredients_and_allergens():
    """Popola ingredienti e allergeni comuni"""
    print("\nCreando ingredienti...")

    print("\nCreando allergeni...")

    allergens_data = [
        'Glutine', 'Lattosio', 'Uova', 'Frutta a guscio', 'Soia', 'Pesce',
        'Crostacei', 'Sedano', 'Senape', 'Sesamo'
    ]

    for allergen_name in allergens_data:
        allergen, created = Allergen.objects.get_or_create(name=allergen_name)
        if created:
            print(f"Creato allergene: {allergen_name}")


def populate_dishes():
    """Popola piatti tipici italiani utilizzando immagini esistenti"""
    print("\nCreando piatti...")

    # Ottengo la lista delle immagini di piatti esistenti
    dish_photos_dir = "uploads/dish-photos/"
    existing_photos = []

    if os.path.exists(dish_photos_dir):
        for file in os.listdir(dish_photos_dir):
            if file.endswith(".jpg") or file.endswith(".jpeg"):
                existing_photos.append(file)

    print(f"  Trovate {len(existing_photos)} immagini di piatti esistenti")

    dishes_data = [
        # Primi piatti
        {
            'name': 'Spaghetti alla Carbonara',
            'description':
            'Pasta con uova, guanciale, pecorino romano e pepe nero',
            'ingredients': ['Pasta', 'Uova', 'Parmigiano', 'Prosciutto'],
            'allergens': ['Glutine', 'Uova', 'Lattosio'],
            'img_keyword': 'spaghetti'
        },
        {
            'name': 'Risotto ai Funghi',
            'description': 'Cremoso risotto con funghi porcini e parmigiano',
            'ingredients': ['Riso', 'Funghi', 'Parmigiano', 'Cipolle'],
            'allergens': ['Lattosio'],
            'img_keyword': 'risotto'
        },
        {
            'name': 'Pasta al Pomodoro',
            'description': 'Pasta con sugo di pomodoro fresco e basilico',
            'ingredients': ['Pasta', 'Pomodoro', 'Basilico', 'Aglio'],
            'allergens': ['Glutine'],
            'img_keyword': 'pasta'
        },
        {
            'name': 'Lasagne della Casa',
            'description':
            'Lasagne con ragù di carne, besciamella e mozzarella',
            'ingredients': ['Pasta', 'Carne bovina', 'Mozzarella', 'Pomodoro'],
            'allergens': ['Glutine', 'Lattosio', 'Uova'],
            'img_keyword': 'lasagn'
        },
        {
            'name': 'Gnocchi al Gorgonzola',
            'description': 'Gnocchi di patate con crema di gorgonzola e noci',
            'ingredients': ['Patate', 'Farina', 'Gorgonzola', 'Noci'],
            'allergens': ['Glutine', 'Lattosio', 'Frutta a guscio'],
            'img_keyword': 'gnocchi'
        },
        {
            'name':
            'Tagliatelle al Ragù',
            'description':
            'Tagliatelle all\'uovo con ragù bolognese tradizionale',
            'ingredients': [
                'Pasta all\'uovo', 'Carne bovina', 'Pomodoro', 'Sedano',
                'Carote'
            ],
            'allergens': ['Glutine', 'Uova', 'Sedano'],
            'img_keyword':
            'tagliatelle'
        },
        {
            'name': 'Ravioli di Ricotta e Spinaci',
            'description':
            'Ravioli ripieni di ricotta e spinaci con burro e salvia',
            'ingredients': ['Pasta all\'uovo', 'Ricotta', 'Spinaci', 'Burro'],
            'allergens': ['Glutine', 'Uova', 'Lattosio'],
            'img_keyword': 'ravioli'
        },
        {
            'name': 'Risotto allo Zafferano',
            'description': 'Risotto cremoso allo zafferano in stile milanese',
            'ingredients': ['Riso', 'Zafferano', 'Parmigiano', 'Burro'],
            'allergens': ['Lattosio'],
            'img_keyword': 'risotto'
        },

        # Secondi piatti
        {
            'name': 'Pollo alla Griglia',
            'description': 'Petto di pollo grigliato con erbe aromatiche',
            'ingredients': ['Pollo', 'Rosmarino', 'Olio extravergine'],
            'allergens': [],
            'img_keyword': 'pollo'
        },
        {
            'name': 'Scaloppine al Limone',
            'description': 'Fettine di vitello in salsa al limone',
            'ingredients': ['Carne bovina', 'Olio extravergine'],
            'allergens': [],
            'img_keyword': 'scalopp'
        },
        {
            'name': 'Pesce al Forno',
            'description': 'Filetto di pesce con patate e olive',
            'ingredients': ['Pesce', 'Patate', 'Olio extravergine'],
            'allergens': ['Pesce'],
            'img_keyword': 'pesce'
        },
        {
            'name': 'Cotoletta alla Milanese',
            'description': 'Cotoletta impanata e fritta',
            'ingredients': ['Carne bovina', 'Uova'],
            'allergens': ['Glutine', 'Uova'],
            'img_keyword': 'cotoletta'
        },
        {
            'name': 'Melanzane alla Parmigiana',
            'description':
            'Strati di melanzane con pomodoro, mozzarella e parmigiano',
            'ingredients':
            ['Melanzane', 'Pomodoro', 'Mozzarella', 'Parmigiano'],
            'allergens': ['Lattosio'],
            'img_keyword': 'melanzane'
        },
        {
            'name': 'Polpette al Sugo',
            'description': 'Polpette di carne in salsa di pomodoro',
            'ingredients':
            ['Carne macinata', 'Uova', 'Pan grattato', 'Pomodoro'],
            'allergens': ['Glutine', 'Uova'],
            'img_keyword': 'polpette'
        },
        {
            'name': 'Frittata di Verdure',
            'description': 'Frittata con verdure miste di stagione',
            'ingredients': ['Uova', 'Zucchine', 'Peperoni', 'Cipolle'],
            'allergens': ['Uova'],
            'img_keyword': 'frittata'
        },
        {
            'name': 'Salmone alla Griglia',
            'description': 'Filetto di salmone grigliato con erbe e limone',
            'ingredients': ['Salmone', 'Limone', 'Erbe aromatiche'],
            'allergens': ['Pesce'],
            'img_keyword': 'salmone'
        },

        # Contorni
        {
            'name': 'Insalata Mista',
            'description': 'Insalata fresca con pomodori e carote',
            'ingredients': ['Insalata', 'Pomodoro', 'Carote'],
            'allergens': [],
            'img_keyword': 'insalata'
        },
        {
            'name': 'Patate Arrosto',
            'description': 'Patate cotte al forno con rosmarino',
            'ingredients': ['Patate', 'Rosmarino', 'Olio extravergine'],
            'allergens': [],
            'img_keyword': 'patate'
        },
        {
            'name': 'Spinaci Saltati',
            'description': 'Spinaci freschi saltati in padella',
            'ingredients': ['Spinaci', 'Aglio', 'Olio extravergine'],
            'allergens': [],
            'img_keyword': 'spinaci'
        },
        {
            'name': 'Zucchine Grigliate',
            'description': 'Zucchine fresche grigliate',
            'ingredients': ['Zucchine', 'Olio extravergine'],
            'allergens': [],
            'img_keyword': 'zucchine'
        },
        {
            'name': 'Funghi Trifolati',
            'description':
            'Funghi saltati con aglio, prezzemolo e vino bianco',
            'ingredients': ['Funghi', 'Aglio', 'Prezzemolo', 'Vino bianco'],
            'allergens': [],
            'img_keyword': 'funghi'
        },
        {
            'name': 'Peperonata',
            'description': 'Peperoni stufati con cipolla e pomodoro',
            'ingredients':
            ['Peperoni', 'Cipolla', 'Pomodoro', 'Olio extravergine'],
            'allergens': [],
            'img_keyword': 'peperonata'
        },
        {
            'name':
            'Verdure Grigliate Miste',
            'description':
            'Selezione di verdure alla griglia con olio e aromi',
            'ingredients':
            ['Zucchine', 'Peperoni', 'Melanzane', 'Olio extravergine'],
            'allergens': [],
            'img_keyword':
            'verdure'
        },
        {
            'name': 'Caponata Siciliana',
            'description':
            'Melanzane in agrodolce con sedano, capperi e olive',
            'ingredients': ['Melanzane', 'Sedano', 'Capperi', 'Olive'],
            'allergens': ['Sedano'],
            'img_keyword': 'caponata'
        },

        # Dolci/Frutta
        {
            'name': 'Tiramisù',
            'description': 'Il classico dolce italiano con mascarpone e caffè',
            'ingredients': ['Uova', 'Mascarpone'],
            'allergens': ['Glutine', 'Uova', 'Lattosio'],
            'img_keyword': 'tiramisu'
        },
        {
            'name': 'Panna Cotta',
            'description': 'Dolce al cucchiaio con frutti di bosco',
            'ingredients': ['Latte', 'Panna'],
            'allergens': ['Lattosio'],
            'img_keyword': 'panna'
        },
        {
            'name': 'Frutta di Stagione',
            'description': 'Selezione di frutta fresca di stagione',
            'ingredients': [],
            'allergens': [],
            'img_keyword': 'frutta'
        },
        {
            'name': 'Gelato Artigianale',
            'description': 'Gelato prodotto artigianalmente',
            'ingredients': ['Latte'],
            'allergens': ['Lattosio'],
            'img_keyword': 'gelato'
        },
        {
            'name': 'Crostata di Frutta',
            'description': 'Pasta frolla con crema pasticcera e frutta fresca',
            'ingredients': ['Farina', 'Uova', 'Latte', 'Frutta'],
            'allergens': ['Glutine', 'Uova', 'Lattosio'],
            'img_keyword': 'crostata'
        },
        {
            'name': 'Cannolo Siciliano',
            'description':
            'Cannolo ripieno di ricotta dolce e scaglie di cioccolato',
            'ingredients': ['Farina', 'Ricotta', 'Zucchero', 'Cioccolato'],
            'allergens': ['Glutine', 'Lattosio'],
            'img_keyword': 'cannolo'
        },
        {
            'name': 'Macedonia di Frutta',
            'description':
            'Mix di frutta fresca tagliata a pezzi con succo di limone',
            'ingredients': ['Mela', 'Pera', 'Kiwi', 'Arancia', 'Banana'],
            'allergens': [],
            'img_keyword': 'macedonia'
        },
        {
            'name': 'Torta al Cioccolato',
            'description': 'Soffice torta al cioccolato fondente',
            'ingredients': ['Farina', 'Uova', 'Burro', 'Cioccolato fondente'],
            'allergens': ['Glutine', 'Uova', 'Lattosio'],
            'img_keyword': 'torta'
        }
    ]

    for dish_data in dishes_data:
        # Cerca un'immagine corrispondente nella directory
        matching_photos = [
            p for p in existing_photos
            if dish_data['img_keyword'] in p.lower()
        ]

        if matching_photos:
            # Usa la prima immagine corrispondente trovata
            img_path = f"dish-photos/{matching_photos[0]}"
            print(
                f"  Trovata immagine esistente per {dish_data['name']}: {matching_photos[0]}"
            )
        else:
            # Se non trova un'immagine corrispondente, usa il nome formattato predefinito
            img_path = f"dish-photos/{dish_data['name'].lower().replace(' ', '_')}.jpg"
            print(
                f"  Nessuna immagine trovata per {dish_data['name']}, usando percorso predefinito"
            )

        dish, created = Dish.objects.get_or_create(
            name=dish_data['name'],
            defaults={
                'description': dish_data['description'],
                'img': img_path
            })

        if created:
            # Aggiungi allergeni
            for allergen_name in dish_data['allergens']:
                try:
                    allergen = Allergen.objects.get(name=allergen_name)
                    dish.allergens.add(allergen)
                except Allergen.DoesNotExist:
                    print(f"  Allergene non trovato: {allergen_name}")

            print(f"  Creato piatto: {dish_data['name']}")


def populate_menus():
    """Popola i menu per ogni mensa per tutti i giorni della settimana"""
    print("\nCreando menu...")

    # Prendi tutti i piatti disponibili
    primi = list(
        Dish.objects.filter(name__in=[
            'Spaghetti alla Carbonara', 'Risotto ai Funghi',
            'Pasta al Pomodoro', 'Lasagne della Casa', 'Gnocchi al Gorgonzola',
            'Tagliatelle al Ragù', 'Ravioli di Ricotta e Spinaci',
            'Risotto allo Zafferano'
        ]))

    secondi = list(
        Dish.objects.filter(name__in=[
            'Pollo alla Griglia', 'Scaloppine al Limone', 'Pesce al Forno',
            'Cotoletta alla Milanese', 'Melanzane alla Parmigiana',
            'Polpette al Sugo', 'Frittata di Verdure', 'Salmone alla Griglia'
        ]))

    contorni = list(
        Dish.objects.filter(name__in=[
            'Insalata Mista', 'Patate Arrosto', 'Spinaci Saltati',
            'Zucchine Grigliate', 'Funghi Trifolati', 'Peperonata',
            'Verdure Grigliate Miste', 'Caponata Siciliana'
        ]))

    dolci = list(
        Dish.objects.filter(name__in=[
            'Tiramisù', 'Panna Cotta', 'Frutta di Stagione',
            'Gelato Artigianale', 'Crostata di Frutta', 'Cannolo Siciliano',
            'Macedonia di Frutta', 'Torta al Cioccolato'
        ]))

    # Per ogni mensa
    mense = Mensa.objects.all()

    for mensa in mense:
        print(f"\nCreando menu per: {mensa.name}")

        # Per ogni giorno della settimana (0=Lunedì, 6=Domenica)
        for weekday in range(7):
            # Per pranzo e cena (0=Pranzo, 1=Cena)
            for day_part in range(2):
                # Controlla se il menu esiste già
                menu, created = Menu.objects.get_or_create(mensa=mensa,
                                                           weekday=weekday,
                                                           day_part=day_part)

                if created:
                    # Seleziona 2 piatti casuali per ogni categoria
                    # Selezioniamo 2 piatti per categoria senza ripetizioni
                    primi_scelti = random.sample(primi, min(
                        2, len(primi))) if primi else []
                    secondi_scelti = random.sample(secondi, min(
                        2, len(secondi))) if secondi else []
                    contorni_scelti = random.sample(
                        contorni, min(2, len(contorni))) if contorni else []
                    dolci_scelti = random.sample(dolci, min(
                        2, len(dolci))) if dolci else []

                    # Aggiungi i piatti al menu
                    for primo in primi_scelti:
                        Includes.objects.create(menu=menu, dish=primo,
                                                type=0)  # Primo

                    for secondo in secondi_scelti:
                        Includes.objects.create(menu=menu,
                                                dish=secondo,
                                                type=1)  # Secondo

                    for contorno in contorni_scelti:
                        Includes.objects.create(menu=menu,
                                                dish=contorno,
                                                type=2)  # Contorno

                    for dolce in dolci_scelti:
                        Includes.objects.create(menu=menu, dish=dolce,
                                                type=3)  # Dessert/Frutta

                    day_names = [
                        'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì',
                        'Sabato', 'Domenica'
                    ]
                    part_names = ['Pranzo', 'Cena']

                    print(
                        f"  Creato menu per {day_names[weekday]} - {part_names[day_part]} con {len(primi_scelti)} primi, {len(secondi_scelti)} secondi, {len(contorni_scelti)} contorni e {len(dolci_scelti)} dolci/frutta"
                    )


def populate_amenities():
    """Crea e popola gli amenities per le mense"""
    print("\nCreando amenities...")

    amenities_data = [{
        "text": "WiFi gratuito",
        "icon": "fas fa-wifi"
    }, {
        "text": "Parcheggio",
        "icon": "fas fa-parking"
    }, {
        "text": "Accessibile ai disabili",
        "icon": "fas fa-wheelchair"
    }, {
        "text": "Posti all'aperto",
        "icon": "fas fa-tree"
    }, {
        "text": "Pagamento elettronico",
        "icon": "far fa-credit-card"
    }, {
        "text": "Distributori automatici",
        "icon": "fas fa-coffee"
    }, {
        "text": "Area relax",
        "icon": "fas fa-couch"
    }, {
        "text": "Scaldavivande",
        "icon": "fas fa-fire-alt"
    }, {
        "text": "Microonde disponibili",
        "icon": "fas fa-radiation-alt"
    }, {
        "text": "Menù vegetariani",
        "icon": "fas fa-leaf"
    }, {
        "text": "Menù senza glutine",
        "icon": "fas fa-seedling"
    }]

    # Crea gli amenities se non esistono già
    created_amenities = []
    for amenity_data in amenities_data:
        amenity, created = AmenitiesMensa.objects.get_or_create(
            text=amenity_data["text"], defaults={"icon": amenity_data["icon"]})
        created_amenities.append(amenity)
        if created:
            print(f"  Creato amenity: {amenity_data['text']}")
        else:
            print(f"  Amenity già esistente: {amenity_data['text']}")

    # Assegna amenities alle mense
    mense = Mensa.objects.all()
    for mensa in mense:
        # Seleziona un numero casuale di amenities (da 3 a 8)
        num_amenities = random.randint(3, 8)
        selected_amenities = random.sample(created_amenities, num_amenities)

        # Aggiungi gli amenities alla mensa
        for amenity in selected_amenities:
            mensa.amenities.add(amenity)

        print(f"  Aggiunti {num_amenities} amenities a {mensa.name}")

    print("Amenities popolati con successo.")


def populate_universities():
    """Aggiunge le principali università italiane al database"""
    print("\nCreando università...")

    universities = [
        # Roma
        "Sapienza - Università di Roma",
        "Università di Roma Tor Vergata",
        "Università Roma Tre",
        "LUISS Guido Carli",
        "Università Campus Bio-Medico di Roma",
        "Link Campus University",
        # Milano
        "Università degli Studi di Milano",
        "Politecnico di Milano",
        "Università Commerciale Luigi Bocconi",
        "Università Cattolica del Sacro Cuore",
        "Università degli Studi di Milano-Bicocca",
        "Università IULM",
        "Università Vita-Salute San Raffaele",
        # Napoli
        "Università degli Studi di Napoli Federico II",
        "Università degli Studi di Napoli L'Orientale",
        "Università degli Studi di Napoli Parthenope",
        "Università degli Studi Suor Orsola Benincasa",
        # Torino
        "Università degli Studi di Torino",
        "Politecnico di Torino",
        "Università degli Studi del Piemonte Orientale",
        # Bologna
        "Università di Bologna",
        "Johns Hopkins University SAIS Bologna",
        # Firenze
        "Università degli Studi di Firenze",
        "Università Europea di Design",
        "Istituto Lorenzo de' Medici",
        # Venezia
        "Università Ca' Foscari Venezia",
        "IUAV - Università Iuav di Venezia",
    ]

    for uni_name in universities:
        uni, created = University.objects.get_or_create(name=uni_name)
        if created:
            print(f"  Creata università: {uni_name}")
        else:
            print(f"  Università già esistente: {uni_name}")

    print(f"Totale università: {University.objects.count()}")
    return University.objects.all()


def populate_economical_levels():
    """Aggiunge livelli economici basati su fasce ISEE al database"""
    print("\nCreando livelli economici (ISEE)...")

    levels = [
        {
            "name": "Fascia 1 - ISEE fino a € 10.000",
            "cost": 3.00
        },
        {
            "name": "Fascia 2 - ISEE da € 10.001 a € 20.000",
            "cost": 4.00
        },
        {
            "name": "Fascia 3 - ISEE da € 20.001 a € 30.000",
            "cost": 5.00
        },
        {
            "name": "Fascia 4 - ISEE da € 30.001 a € 40.000",
            "cost": 6.00
        },
        {
            "name": "Fascia 5 - ISEE da € 40.001 a € 50.000",
            "cost": 7.00
        },
        {
            "name": "Fascia 6 - ISEE superiore a € 50.000",
            "cost": 8.00
        },
        {
            "name": "Fascia speciale - Borsisti",
            "cost": 1.50
        },
        {
            "name": "Fascia docenti - Staff universitario",
            "cost": 5.50
        },
    ]

    for level in levels:
        eco_level, created = EconomicalLevel.objects.get_or_create(
            name=level["name"], defaults={"cost": Decimal(str(level["cost"]))})
        if created:
            print(
                f"  Creato livello economico: {level['name']} (costo: €{level['cost']:.2f})"
            )
        else:
            print(f"  Livello economico già esistente: {level['name']}")

    print(f"Totale livelli economici: {EconomicalLevel.objects.count()}")
    return EconomicalLevel.objects.all()


def populate_users(num_users=50):
    """Crea utenti casuali con nomi e cognomi italiani, università e livelli economici assegnati"""
    print("\nCreando utenti...")

    # Assicura che ci siano università e livelli economici
    universities = list(University.objects.all())
    if not universities:
        universities = populate_universities()

    economical_levels = list(EconomicalLevel.objects.all())
    if not economical_levels:
        economical_levels = populate_economical_levels()

    User = get_user_model()
    existing_count = User.objects.count()

    # Tieni traccia degli utenti creati
    created_users = []

    for i in range(num_users):
        # Genera nome e cognome casuali
        first_name = random.choice(NOMI_ITALIANI)
        last_name = random.choice(COGNOMI_ITALIANI)

        # Crea email basata sul nome
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@studente.it"

        # Verifica se esiste già
        if User.objects.filter(email=email).exists():
            continue

        # Assegna università e livello economico casuali
        university = random.choice(universities)
        eco_level = random.choice(economical_levels)

        # Crea l'utente
        try:
            user = User.objects.create_user(
                email=email,
                password=
                "password123",  # password generica per tutti gli utenti di test
                first_name=first_name,
                last_name=last_name,
                university=university,
                economical_level=eco_level,
                credit=Decimal(str(random.randint(0, 100) + random.random())))
            created_users.append(user)
            print(f"  Creato utente: {first_name} {last_name} ({email})")
        except Exception as e:
            print(f"  Errore nella creazione dell'utente {email}: {str(e)}")

    new_count = User.objects.count() - existing_count
    print(f"Totale nuovi utenti creati: {new_count}")
    print(f"Totale utenti nel database: {User.objects.count()}")

    return created_users


def reset_database():
    """Resetta il database cancellando tutti i dati esistenti"""
    print("Reset del database in corso...")

    # Elimina tutti i dati nelle tabelle
    CustomUser.objects.all().delete()
    EconomicalLevel.objects.all().delete()
    University.objects.all().delete()

    Mensa.objects.all().delete()
    City.objects.all().delete()
    PhotoMensa.objects.all().delete()
    AmenitiesMensa.objects.all().delete()
    Dish.objects.all().delete()
    Allergen.objects.all().delete()
    Includes.objects.all().delete()
    Menu.objects.all().delete()
    Hours.objects.all().delete()

    print("Database resettato con successo!")


def main():
    reset_database()  # Resetta il database prima di popolarlo
    create_admin_user()
    populate_cities()
    populate_events()

    # Creare università e livelli economici
    populate_universities()
    populate_economical_levels()

    # Creare utenti (oltre all'admin)
    populate_users(50)  # 50 utenti studenti

    # Popolamento mense e funzionalità correlate
    populate_mense()
    populate_hours()
    populate_ingredients_and_allergens()
    populate_dishes()
    populate_menus()
    populate_amenities()

    # Creazione recensioni (con più recensioni per mensa)
    populate_reviews(min_reviews=7, max_reviews=15)

    print("Database popolato con successo!")


if __name__ == "__main__":
    main()
    print("Inizio popolamento del database...")
