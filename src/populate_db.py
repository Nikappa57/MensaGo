from django.utils import timezone
from datetime import timedelta
from django.core.files.base import ContentFile
import os
import base64
import random
from pathlib import Path

# Impostazione per l'ambiente Django
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importazione dei modelli
from apps.mensa.models.City import City
from apps.mensa.models.Events import Event

def create_sample_image(filename, width=800, height=600, color=None):
    """
    Crea un'immagine di esempio con dimensioni e colore specificati
    Salva l'immagine nella cartella appropriata e restituisce il percorso relativo
    """
    try:
        from PIL import Image
        # Crea un'immagine con colore casuale se non specificato
        if color is None:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        img = Image.new('RGB', (width, height), color)
        
        # Crea la directory se non esiste
        directory = os.path.dirname(filename)
        os.makedirs(directory, exist_ok=True)
        
        # Salva l'immagine
        img.save(filename)
        return filename
    except ImportError:
        print("PIL non installato. Utilizzo immagine di placeholder.")
        # Se PIL non è installato, crea solo un file vuoto come placeholder
        with open(filename, 'w') as f:
            f.write('placeholder')
        return filename

def populate_cities():
    """Aggiunge alcune città di esempio al database"""
    cities = [
        "Roma",
        "Milano",
        "Napoli",
        "Torino",
        "Bologna",
        "Firenze",
        "Venezia",
        "Padova"
    ]
    
    print("Aggiungo città...")
    for city_name in cities:
        # Controlla se la città esiste già
        if not City.objects.filter(name=city_name).exists():
            # Crea un'immagine di esempio per la città
            img_path = f"frontend/static/imgs/landscapes/{city_name.lower().replace(' ', '_')}.jpg"
            create_sample_image(img_path)
            
            # Crea l'oggetto City
            city = City(name=city_name, landscape=f"landscapes/{city_name.lower().replace(' ', '_')}.jpg")
            city.save()
            print(f"Aggiunta città: {city_name}")
        else:
            print(f"La città {city_name} esiste già")

def populate_events():
    """Aggiunge alcuni eventi di esempio al database"""
    # Eventi con date future (a partire da oggi)
    today = timezone.now().date()
    events = [
        {"name": "Festival Culinario Universitario", "days_from_now": 5},
        {"name": "Serata Pizza e Birra", "days_from_now": 10},
        {"name": "Incontro con Chef Stellato", "days_from_now": 15},
        {"name": "Degustazione Vini Locali", "days_from_now": 20},
        {"name": "Serata di Cucina Internazionale", "days_from_now": 25},
        {"name": "Workshop: Cucina Sostenibile", "days_from_now": 30}
    ]
    
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
                img=f"events/{event_name.lower().replace(' ', '_')}.jpg"
            )
            event_obj.save()
            print(f"Aggiunto evento: {event_name} in data {event_date}")
        else:
            print(f"L'evento {event_name} in data {event_date} esiste già")

if __name__ == "__main__":
    print("Inizio popolazione del database...")
    populate_cities()
    populate_events()
    print("Popolazione del database completata con successo!")