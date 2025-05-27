#!/usr/bin/env python
"""
Script per popolare il database con menu giornalieri e piatti
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.mensa.models import Mensa, Menu, Dish, Includes, Ingredient, Allergen
from PIL import Image
from io import BytesIO
import random


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
    
    ingredients_data = [
        'Pomodoro', 'Mozzarella', 'Basilico', 'Aglio', 'Olio extravergine',
        'Pasta', 'Riso', 'Carne bovina', 'Pollo', 'Pesce',
        'Zucchine', 'Melanzane', 'Peperoni', 'Spinaci', 'Insalata',
        'Parmigiano', 'Ricotta', 'Prosciutto', 'Salame', 'Funghi',
        'Carote', 'Patate', 'Cipolle', 'Prezzemolo', 'Rosmarino'
    ]
    
    for ingredient_name in ingredients_data:
        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
        if created:
            print(f"Creato ingrediente: {ingredient_name}")
    
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
    """Popola piatti tipici italiani"""
    print("\nCreando piatti...")
    
    dishes_data = [
        # Primi piatti
        {
            'name': 'Spaghetti alla Carbonara',
            'description': 'Pasta con uova, guanciale, pecorino romano e pepe nero',
            'ingredients': ['Pasta', 'Uova', 'Parmigiano', 'Prosciutto'],
            'allergens': ['Glutine', 'Uova', 'Lattosio']
        },
        {
            'name': 'Risotto ai Funghi',
            'description': 'Cremoso risotto con funghi porcini e parmigiano',
            'ingredients': ['Riso', 'Funghi', 'Parmigiano', 'Cipolle'],
            'allergens': ['Lattosio']
        },
        {
            'name': 'Pasta al Pomodoro',
            'description': 'Pasta con sugo di pomodoro fresco e basilico',
            'ingredients': ['Pasta', 'Pomodoro', 'Basilico', 'Aglio'],
            'allergens': ['Glutine']
        },
        {
            'name': 'Lasagne della Casa',
            'description': 'Lasagne con ragù di carne, besciamella e mozzarella',
            'ingredients': ['Pasta', 'Carne bovina', 'Mozzarella', 'Pomodoro'],
            'allergens': ['Glutine', 'Lattosio', 'Uova']
        },
        
        # Secondi piatti
        {
            'name': 'Pollo alla Griglia',
            'description': 'Petto di pollo grigliato con erbe aromatiche',
            'ingredients': ['Pollo', 'Rosmarino', 'Olio extravergine'],
            'allergens': []
        },
        {
            'name': 'Scaloppine al Limone',
            'description': 'Fettine di vitello in salsa al limone',
            'ingredients': ['Carne bovina', 'Olio extravergine'],
            'allergens': []
        },
        {
            'name': 'Pesce al Forno',
            'description': 'Filetto di pesce con patate e olive',
            'ingredients': ['Pesce', 'Patate', 'Olio extravergine'],
            'allergens': ['Pesce']
        },
        {
            'name': 'Cotoletta alla Milanese',
            'description': 'Cotoletta impanata e fritta',
            'ingredients': ['Carne bovina', 'Uova'],
            'allergens': ['Glutine', 'Uova']
        },
        
        # Contorni
        {
            'name': 'Insalata Mista',
            'description': 'Insalata fresca con pomodori e carote',
            'ingredients': ['Insalata', 'Pomodoro', 'Carote'],
            'allergens': []
        },
        {
            'name': 'Patate Arrosto',
            'description': 'Patate cotte al forno con rosmarino',
            'ingredients': ['Patate', 'Rosmarino', 'Olio extravergine'],
            'allergens': []
        },
        {
            'name': 'Spinaci Saltati',
            'description': 'Spinaci freschi saltati in padella',
            'ingredients': ['Spinaci', 'Aglio', 'Olio extravergine'],
            'allergens': []
        },
        {
            'name': 'Zucchine Grigliate',
            'description': 'Zucchine fresche grigliate',
            'ingredients': ['Zucchine', 'Olio extravergine'],
            'allergens': []
        },
        
        # Dolci/Frutta
        {
            'name': 'Tiramisù',
            'description': 'Il classico dolce italiano con mascarpone e caffè',
            'ingredients': ['Uova', 'Mascarpone'],
            'allergens': ['Glutine', 'Uova', 'Lattosio']
        },
        {
            'name': 'Panna Cotta',
            'description': 'Dolce al cucchiaio con frutti di bosco',
            'ingredients': ['Latte', 'Panna'],
            'allergens': ['Lattosio']
        },
        {
            'name': 'Frutta di Stagione',
            'description': 'Selezione di frutta fresca di stagione',
            'ingredients': [],
            'allergens': []
        },
        {
            'name': 'Gelato Artigianale',
            'description': 'Gelato prodotto artigianalmente',
            'ingredients': ['Latte'],
            'allergens': ['Lattosio']
        }
    ]
    
    for dish_data in dishes_data:
        dish, created = Dish.objects.get_or_create(
            name=dish_data['name'],
            defaults={
                'description': dish_data['description'],
                'img': f"dish-photos/{dish_data['name'].lower().replace(' ', '_')}.jpg"
            }
        )
        
        if created:
            # Crea immagine del piatto
            img_path = f"uploads/dish-photos/{dish_data['name'].lower().replace(' ', '_')}.jpg"
            create_sample_dish_image(img_path)
            
            # Aggiungi ingredienti
            for ingredient_name in dish_data['ingredients']:
                try:
                    ingredient = Ingredient.objects.get(name=ingredient_name)
                    dish.ingredients.add(ingredient)
                except Ingredient.DoesNotExist:
                    print(f"Ingrediente non trovato: {ingredient_name}")
            
            # Aggiungi allergeni
            for allergen_name in dish_data['allergens']:
                try:
                    allergen = Allergen.objects.get(name=allergen_name)
                    dish.allergens.add(allergen)
                except Allergen.DoesNotExist:
                    print(f"Allergene non trovato: {allergen_name}")
            
            print(f"Creato piatto: {dish_data['name']}")


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


def main():
    """Funzione principale"""
    print("Inizio popolamento menu e piatti...")
    
    # Popola ingredienti e allergeni
    populate_ingredients_and_allergens()
    
    # Popola piatti
    populate_dishes()
    
    # Popola menu
    populate_menus()
    
    print("\n✅ Popolamento completato!")
    print("Ora puoi visualizzare i menu giornalieri nelle pagine delle mense.")


if __name__ == "__main__":
    main()
