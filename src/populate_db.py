import os
import random
from datetime import timedelta
from pathlib import Path

import django
from django.core.files.base import ContentFile
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importazione dei modelli
from apps.mensa.models.City import City
from apps.mensa.models.Events import Event
from apps.mensa.models.Mensa import Mensa, PhotoMensa


def create_sample_image(filename, width=800, height=600, color=None):
    """
    Crea un'immagine di esempio con dimensioni e colore specificati
    Salva l'immagine nella cartella appropriata e restituisce il percorso relativo
    """
    try:
        from PIL import Image

        # Crea un'immagine con colore casuale se non specificato
        if color is None:
            color = (random.randint(0, 255), random.randint(0, 255),
                     random.randint(0, 255))

        img = Image.new('RGB', (width, height), color)

        # Crea la directory se non esiste
        directory = os.path.dirname(filename)
        os.makedirs(directory, exist_ok=True)

        # Salva l'immagine
        img.save(filename)
        return filename
    except ImportError:
        print("PIL non installato. Utilizzo immagine di placeholder."
              )  # TODO: penso non serva!
        # Se PIL non è installato, crea solo un file vuoto come placeholder
        with open(filename, 'w') as f:
            f.write('placeholder')
        return filename


def populate_cities():
    """Aggiunge alcune città di esempio al database"""
    cities = [
        "Roma", "Milano", "Napoli", "Torino", "Bologna", "Firenze", "Venezia",
        "Padova"
    ]
    cities_pos = {
        "Roma": (41.9028, 12.4964),
        "Milano": (45.4642, 9.1900),
        "Napoli": (40.8518, 14.2681),
        "Torino": (45.0703, 7.6869),
        "Bologna": (44.4949, 11.3426),
        "Firenze": (43.7696, 11.2558),
        "Venezia": (45.4408, 12.3155),
        "Padova": (45.4064, 11.8768)
    }

    print("Aggiungo città...")
    for city_name in cities:
        # Controlla se la città esiste già
        if City.objects.filter(name=city_name).exists():
            city = City.objects.get(name=city_name)
        else:
            city = City(name=city_name)

        # Crea un'immagine di esempio per la città
        img_path = f"frontend/static/imgs/landscapes/{city_name.lower().replace(' ', '_')}.jpg"  # TODO: a che serve?
        create_sample_image(img_path)

        # Crea l'oggetto City
        landscape_file_path = f"landscapes/{city_name.lower().replace(' ', '_')}.jpg"
        city.landscape = landscape_file_path
        city.latitude = cities_pos[city_name][0]
        city.longitude = cities_pos[city_name][1]
        city.save()
        print(f"Aggiunta città: {city_name}")


def populate_events():
    """Aggiunge alcuni eventi di esempio al database"""
    # Eventi con date future (a partire da oggi)
    today = timezone.now().date()
    events = [{
        "name": "Festival Culinario Universitario",
        "days_from_now": 5
    }, {
        "name": "Serata Pizza e Birra",
        "days_from_now": 10
    }, {
        "name": "Incontro con Chef Stellato",
        "days_from_now": 15
    }, {
        "name": "Degustazione Vini Locali",
        "days_from_now": 20
    }, {
        "name": "Serata di Cucina Internazionale",
        "days_from_now": 25
    }, {
        "name": "Workshop: Cucina Sostenibile",
        "days_from_now": 30
    }]

    print("Aggiungo eventi...")
    for event in events:
        event_date = today + timedelta(days=event["days_from_now"])
        event_name = event["name"]

        # Controlla se l'evento esiste già
        if not Event.objects.filter(name=event_name, date=event_date).exists():
            # Crea un'immagine di esempio per l'evento
            img_path = f"frontend/static/imgs/events/{event_name.lower().replace(' ', '_')}.jpg"
            create_sample_image(img_path)

            # Crea l'oggetto Event
            event_obj = Event(
                name=event_name,
                date=event_date,
                img=f"events/{event_name.lower().replace(' ', '_')}.jpg")
            event_obj.save()
            print(f"Aggiunto evento: {event_name} in data {event_date}")
        else:
            print(f"L'evento {event_name} in data {event_date} esiste già")


def populate_mense():
    """Aggiunge alcune mense di esempio al database"""
    mense_data = {
        'Milano': [
            {
                'name': 'Mensa Bicocca',
                'description':
                'Moderna mensa universitaria nel campus Bicocca',
                'position': 'Piazza della Scienza 1, Milano',
                'capacity': 300,
                'phone_number': '02123456',
                'email': 'mensa.bicocca@unimib.it'
            },
            {
                'name': 'Mensa Statale',
                'description':
                'Mensa centrale dell\'Università degli Studi di Milano',
                'position': 'Via Festa del Perdono 7, Milano',
                'capacity': 400,
                'phone_number': '02654321',
                'email': 'mensa.statale@unimi.it'
            },
            {
                'name': 'Mensa Politecnico',
                'description': 'Mensa del Politecnico di Milano',
                'position': 'Piazza Leonardo da Vinci 32, Milano',
                'capacity': 500,
                'phone_number': '02345678',
                'email': 'mensa.polimi@unimi.it'
            },
            {
                'name': 'Mensa Città Studi',
                'description': 'Mensa del quartiere universitario Città Studi',
                'position': 'Via Celoria 2, Milano',
                'capacity': 350,
                'phone_number': '02234567',
                'email': 'mensa.studi@unimi.it'
            },
            {
                'name': 'Mensa IULM',
                'description': 'Mensa dell\'Università IULM',
                'position': 'Via Carlo Bo 1, Milano',
                'capacity': 200,
                'phone_number': '02876543',
                'email': 'mensa.iulm@unimi.it'
            },
            {
                'name': 'Mensa Bocconi',
                'description': 'Mensa dell\'Università Bocconi',
                'position': 'Via Sarfatti 25, Milano',
                'capacity': 600,
                'phone_number': '02712345',
                'email': 'mensa.boc@unimi.it'
            },
            {
                'name': 'Mensa NABA',
                'description': 'Mensa della Nuova Accademia di Belle Arti',
                'position': 'Via C. Darwin 20, Milano',
                'capacity': 150,
                'phone_number': '02345678',
                'email': 'mensa.naba@unimi.it'
            },
        ],
        'Roma': [{
            'name': 'Mensa La Sapienza',
            'description': 'Mensa principale dell\'Università La Sapienza',
            'position': 'Piazzale Aldo Moro 5, Roma',
            'capacity': 500,
            'phone_number': '06123456',
            'email': 'mensa.sapienza@uniroma1.it'
        }, {
            'name': 'Mensa Roma Tre',
            'description': 'Mensa dell\'Università Roma Tre',
            'position': 'Via Ostiense 159, Roma',
            'capacity': 250,
            'phone_number': '06654321',
            'email': 'mensa.romatre@uniroma3.it'
        }],
        'Bologna': [{
            'name': 'Mensa Irnerio',
            'description': 'Mensa storica dell\'Università di Bologna',
            'position': 'Via Zamboni 33, Bologna',
            'capacity': 350,
            'phone_number': '051123456',
            'email': 'mensa.irnerio@unibo.it'
        }, {
            'name': 'Mensa Ingegneria',
            'description': 'Mensa della facoltà di Ingegneria',
            'position': 'Viale del Risorgimento 2, Bologna',
            'capacity': 200,
            'phone_number': '051654321',
            'email': 'mensa.ingegneria@unibo.it'
        }],
        'Firenze': [{
            'name': 'Mensa Calamandrei',
            'description': 'Mensa centrale dell\'Università di Firenze',
            'position': 'Viale Morgagni 51, Firenze',
            'capacity': 300,
            'phone_number': '055123456',
            'email': 'mensa.calamandrei@unifi.it'
        }],
        'Torino': [{
            'name': 'Mensa Politecnico',
            'description': 'Mensa del Politecnico di Torino',
            'position': 'Corso Duca degli Abruzzi 24, Torino',
            'capacity': 400,
            'phone_number': '011123456',
            'email': 'mensa.polito@polito.it'
        }],
        'Napoli': [{
            'name': 'Mensa Federico II',
            'description': 'Mensa dell\'Università Federico II',
            'position': 'Corso Umberto I 40, Napoli',
            'capacity': 350,
            'phone_number': '081123456',
            'email': 'mensa.federicoii@unina.it'
        }],
        'Venezia': [{
            'name': 'Mensa Rio Novo',
            'description': 'Mensa universitaria nel cuore di Venezia',
            'position': 'Dorsoduro 3861, Venezia',
            'capacity': 200,
            'phone_number': '041123456',
            'email': 'mensa.rionovo@unive.it'
        }],
        'Padova': [{
            'name': 'Mensa Piovego',
            'description': 'Mensa del polo scientifico',
            'position': 'Via Giuseppe Colombo 1, Padova',
            'capacity': 300,
            'phone_number': '049123456',
            'email': 'mensa.piovego@unipd.it'
        }, {
            'name': 'Mensa San Francesco',
            'description': 'Mensa nel centro storico di Padova',
            'position': 'Via San Francesco 122, Padova',
            'capacity': 250,
            'phone_number': '049654321',
            'email': 'mensa.sanfrancesco@unipd.it'
        }]
    }

    print("\nAggiungo mense...")
    for city_name, mense in mense_data.items():
        try:
            city = City.objects.get(name=city_name)
            print(f"\nProcessando {city_name}...")

            for mensa_data in mense:
                # Controlla se la mensa esiste già
                if not Mensa.objects.filter(name=mensa_data['name']).exists():
                    # Crea un'immagine di esempio per la mensa
                    img_name = mensa_data['name'].lower().replace(' ', '_')
                    img_path = f"uploads/banners/{img_name}.jpg"
                    create_sample_image(img_path)

                    # Crea la mensa con i dati base
                    mensa = Mensa(name=mensa_data['name'],
                                  description=mensa_data['description'],
                                  position=mensa_data['position'],
                                  capacity=mensa_data['capacity'],
                                  phone_number=mensa_data['phone_number'],
                                  email=mensa_data['email'],
                                  city=city,
                                  banner=f"banners/{img_name}.jpg")
                    mensa.save()
                    
                    # Crea e collega le immagini della galleria
                    # Crea 4 immagini di esempio per ogni mensa
                    for i in range(4):
                        img_name = f"{mensa_data['name'].lower().replace(' ', '-')}{i+1}.jpg"
                        img_path = f"uploads/photos/{img_name}"
                        # Crea un'immagine con un colore casuale per ogni foto della galleria
                        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        create_sample_image(img_path, color=color)
                        # Crea l'oggetto PhotoMensa e lo collega alla mensa
                        photo = PhotoMensa.objects.create(img=f"photos/{img_name}")
                        mensa.gallery.add(photo)
                    mensa.save()
                    
                    print(f"Aggiunta mensa: {mensa_data['name']} con 4 immagini")
                else:
                    print(f"La mensa {mensa_data['name']} esiste già")

        except City.DoesNotExist:
            print(f"Città {city_name} non trovata, salto...")


def create_mensa_gallery(mensa_name, num_images=4):
    """
    Crea una galleria di immagini per una mensa creando oggetti PhotoMensa
    """
    photos = []
    for i in range(num_images):
        img_name = f"{mensa_name.lower().replace(' ', '-')}{i+1}.jpg"
        img_path = f"uploads/photos/{img_name}"
        # Crea un'immagine con un colore casuale per ogni foto della galleria
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        create_sample_image(img_path)
        photo = PhotoMensa.objects.create(img=f"photos/{img_name}")
        photos.append(photo)
    return photos


def clear_mense():
    """Elimina tutte le mense e le foto esistenti nel database"""
    print("Eliminando tutte le mense esistenti...")
    Mensa.objects.all().delete()
    print("Eliminando tutte le foto delle mense esistenti...")
    PhotoMensa.objects.all().delete()
    print("Tutte le mense e le foto eliminate con successo!")


if __name__ == "__main__":
    print("Inizio popolazione del database...")
    populate_cities()
    populate_events()
    clear_mense()
    populate_mense()
    print("Popolazione del database completata con successo!")
