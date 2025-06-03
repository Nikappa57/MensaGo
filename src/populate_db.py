import os
import random
from datetime import timedelta, time
from pathlib import Path

import django
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importazione dei modelli
from apps.mensa.models.City import City
from apps.mensa.models.Events import Event
from apps.mensa.models.Mensa import Mensa, PhotoMensa, AmenitiesMensa
from apps.mensa.models.Review import Review
from apps.mensa.models.Hours import Hours

from apps.mensa.models import Mensa, Menu, Dish, Includes, Allergen
from PIL import Image
from io import BytesIO
import random


def create_admin_user():
	"""Crea un utente admin se non esiste già"""
	User = get_user_model()
	if not User.objects.filter(email="admin@admin.com").exists():
		User.objects.create_superuser(
			email="admin@admin.com",
			password="admin",
			first_name="Admin",
			last_name="User"
		)
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
			color = (
				random.randint(0, 255),
				random.randint(0, 255),
				random.randint(0, 255)
			)

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


def populate_reviews():
	"""Aggiunge alcune recensioni di esempio alle mense"""
	User = get_user_model()
	users = list(User.objects.all())
	mense = list(Mensa.objects.all())
	if not users or not mense:
		print("Nessun utente o mensa trovata, salto le reviews.")
		return

	for mensa in mense:
		for i in range(2):  # 2 recensioni per mensa
			user = users[i % len(users)]
			if not Review.objects.filter(mensa=mensa, user=user).exists():
				Review.objects.create(
					mensa=mensa,
					user=user,
					stars=random.randint(1, 5),
					text=f"Recensione di test {i+1} per {mensa.name} da {user.first_name}"
				)
				print(f"Aggiunta review per {mensa.name} da {user.email}")
			else:
				print(f"Review già esistente per {mensa.name} da {user.email}")


def populate_cities():
	"""Aggiunge alcune città di esempio al database"""
	cities = [
		"Roma", "Milano", "Napoli", "Torino", "Bologna", 
		"Firenze", "Venezia", "Padova"
	]
	coords = {
		"Roma": (41.9028, 12.4964),
		"Milano": (45.4642, 9.1900),
		"Napoli": (40.8518, 14.2681),
		"Torino": (45.0703, 7.6869),
		"Bologna": (44.4949, 11.3426),
		"Firenze": (43.7696, 11.2558),
		"Venezia": (45.4408, 12.3155),
		"Padova": (45.4064, 11.8768)
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
    events = [
        {
            "name": "Festival Culinario Universitario",
            "desc": "Un festival dedicato alla cucina universitaria con stand gastronomici e showcooking.",
            "days_from_now": 5
        },
        {
            "name": "Serata Pizza e Birra",
            "desc": "Una serata informale con pizza artigianale e birre locali.",
            "days_from_now": 10
        },
        {
            "name": "Incontro con Chef Stellato",
            "desc": "Un incontro esclusivo con uno chef stellato che presenterà ricette innovative.",
            "days_from_now": 15
        },
        {
            "name": "Degustazione Vini Locali",
            "desc": "Degustazione guidata di vini del territorio con sommelier professionisti.",
            "days_from_now": 20
        },
        {
            "name": "Serata di Cucina Internazionale",
            "desc": "Un viaggio tra i sapori del mondo con piatti tipici di diversi paesi.",
            "days_from_now": 25
        },
        {
            "name": "Workshop: Cucina Sostenibile",
            "desc": "Laboratorio pratico su tecniche di cucina sostenibile e a basso impatto ambientale.",
            "days_from_now": 30
        }
    ]

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
				}
			)

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

			print(f"{'Aggiunta' if created else 'Aggiornata'} mensa: {m_data['name']}")


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
				close_time=time(14, 30)
			)
		
		# Orari di cena dal lunedì al venerdì (giorni 0-4)
		for weekday in range(5):
			Hours.objects.create(
				mensa=mensa,
				weekday=weekday,
				daypart=1,  # Cena
				open_time=time(19, 0),
				close_time=time(22, 0)
			)
		
		# Alcune mense sono aperte anche il sabato a pranzo (giorno 5)
		if random.random() < 0.7:  # 70% delle mense aperte il sabato a pranzo
			Hours.objects.create(
				mensa=mensa,
				weekday=5,
				daypart=0,  # Pranzo
				open_time=time(11, 30),
				close_time=time(14, 0)
			)
			print(f"  ✓ {mensa.name} aperta il sabato a pranzo")
	
	print(f"Orari configurati per {mense.count()} mense")

def create_sample_dish_image(path, size=(300, 300)):
	"""Crea un'immagine di esempio per un piatto"""
	# Colori appetitosi per i piatti
	colors = [
		(255, 165, 0),    # Arancione (pasta)
		(34, 139, 34),    # Verde (verdure)
		(210, 180, 140),  # Marrone (carne)
		(255, 99, 71),    # Rosso pomodoro
		(255, 255, 0),    # Giallo (formaggi)
		(139, 69, 19),    # Marrone scuro (dolci)
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
		'Glutine', 'Lattosio', 'Uova', 'Frutta a guscio', 'Soia',
		'Pesce', 'Crostacei', 'Sedano', 'Senape', 'Sesamo'
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
			'description': 'Pasta con uova, guanciale, pecorino romano e pepe nero',
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
			'description': 'Lasagne con ragù di carne, besciamella e mozzarella',
			'ingredients': ['Pasta', 'Carne bovina', 'Mozzarella', 'Pomodoro'],
			'allergens': ['Glutine', 'Lattosio', 'Uova'],
			'img_keyword': 'lasagn'
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
		}
	]
	
	for dish_data in dishes_data:
		# Cerca un'immagine corrispondente nella directory
		matching_photos = [p for p in existing_photos if dish_data['img_keyword'] in p.lower()]
		
		if matching_photos:
			# Usa la prima immagine corrispondente trovata
			img_path = f"dish-photos/{matching_photos[0]}"
			print(f"  Trovata immagine esistente per {dish_data['name']}: {matching_photos[0]}")
		else:
			# Se non trova un'immagine corrispondente, usa il nome formattato predefinito
			img_path = f"dish-photos/{dish_data['name'].lower().replace(' ', '_')}.jpg"
			print(f"  Nessuna immagine trovata per {dish_data['name']}, usando percorso predefinito")
		
		dish, created = Dish.objects.get_or_create(
			name=dish_data['name'],
			defaults={
				'description': dish_data['description'],
				'img': img_path
			}
		)
		
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
	primi = list(Dish.objects.filter(name__in=[
		'Spaghetti alla Carbonara', 'Risotto ai Funghi', 'Pasta al Pomodoro', 'Lasagne della Casa'
	]))
	
	secondi = list(Dish.objects.filter(name__in=[
		'Pollo alla Griglia', 'Scaloppine al Limone', 'Pesce al Forno', 'Cotoletta alla Milanese'
	]))
	
	contorni = list(Dish.objects.filter(name__in=[
		'Insalata Mista', 'Patate Arrosto', 'Spinaci Saltati', 'Zucchine Grigliate'
	]))
	
	dolci = list(Dish.objects.filter(name__in=[
		'Tiramisù', 'Panna Cotta', 'Frutta di Stagione', 'Gelato Artigianale'
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
				menu, created = Menu.objects.get_or_create(
					mensa=mensa,
					weekday=weekday,
					day_part=day_part
				)
				
				if created:
					# Seleziona piatti casuali per ogni categoria
					primo_scelto = random.choice(primi) if primi else None
					secondo_scelto = random.choice(secondi) if secondi else None
					contorno_scelto = random.choice(contorni) if contorni else None
					dolce_scelto = random.choice(dolci) if dolci else None
					
					# Aggiungi i piatti al menu
					if primo_scelto:
						Includes.objects.create(menu=menu, dish=primo_scelto, type=0)  # Primo
					
					if secondo_scelto:
						Includes.objects.create(menu=menu, dish=secondo_scelto, type=1)  # Secondo
					
					if contorno_scelto:
						Includes.objects.create(menu=menu, dish=contorno_scelto, type=2)  # Contorno
					
					if dolce_scelto:
						Includes.objects.create(menu=menu, dish=dolce_scelto, type=3)  # Dessert/Frutta
					
					day_names = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']
					part_names = ['Pranzo', 'Cena']
					
					print(f"  Creato menu per {day_names[weekday]} - {part_names[day_part]}")
def populate_amenities():
	"""Crea e popola gli amenities per le mense"""
	print("\nCreando amenities...")
	
	amenities_data = [
		{"text": "WiFi gratuito", "icon": "fas fa-wifi"},
		{"text": "Parcheggio", "icon": "fas fa-parking"},
		{"text": "Accessibile ai disabili", "icon": "fas fa-wheelchair"},
		{"text": "Posti all'aperto", "icon": "fas fa-tree"},
		{"text": "Pagamento elettronico", "icon": "far fa-credit-card"},
		{"text": "Distributori automatici", "icon": "fas fa-coffee"},
		{"text": "Area relax", "icon": "fas fa-couch"},
		{"text": "Scaldavivande", "icon": "fas fa-fire-alt"},
		{"text": "Microonde disponibili", "icon": "fas fa-radiation-alt"},
		{"text": "Menù vegetariani", "icon": "fas fa-leaf"},
		{"text": "Menù senza glutine", "icon": "fas fa-seedling"}
	]
	
	# Crea gli amenities se non esistono già
	created_amenities = []
	for amenity_data in amenities_data:
		amenity, created = AmenitiesMensa.objects.get_or_create(
			text=amenity_data["text"],
			defaults={"icon": amenity_data["icon"]}
		)
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
	
def main():
	create_admin_user()
	populate_cities()
	populate_events()
	populate_mense()
	populate_reviews()
	populate_hours()
	populate_ingredients_and_allergens()
	populate_dishes()
	populate_menus()
	populate_amenities()
	print("Database popolato con successo!")

if __name__ == "__main__":
	main()
	print("Inizio popolamento del database...")
