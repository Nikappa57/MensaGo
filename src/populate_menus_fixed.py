#!/usr/bin/env python
"""
Script migliorato per popolare il database con menu giornalieri e piatti
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.mensa.models import Mensa
from apps.mensa.models.Menu import Menu, Dish, Includes
from apps.mensa.models.Ingredient import Ingredient
from apps.mensa.models.Allergen import Allergen
import random


def clear_existing_data():
    """Pulisce i dati esistenti per ripartire da zero"""
    print("Cancellando dati esistenti...")
    Includes.objects.all().delete()
    Menu.objects.all().delete()
    Dish.objects.all().delete()
    Ingredient.objects.all().delete()
    Allergen.objects.all().delete()
    print("Dati cancellati!")


def create_ingredients():
    """Crea ingredienti base"""
    print("Creando ingredienti...")
    
    ingredients = [
        'Pasta', 'Riso', 'Pomodoro', 'Mozzarella', 'Parmigiano',
        'Basilico', 'Aglio', 'Olio extravergine', 'Carne bovina', 'Pollo',
        'Pesce', 'Uova', 'Spinaci', 'Zucchine', 'Patate',
        'Carote', 'Insalata', 'Funghi', 'Prosciutto', 'Ricotta'
    ]
    
    for name in ingredients:
        ingredient, created = Ingredient.objects.get_or_create(name=name)
        if created:
            print(f"  ✓ {name}")


def create_allergens():
    """Crea allergeni comuni"""
    print("Creando allergeni...")
    
    allergens = [
        'Glutine', 'Lattosio', 'Uova', 'Pesce', 'Frutta a guscio',
        'Soia', 'Sedano', 'Senape', 'Sesamo', 'Crostacei'
    ]
    
    for name in allergens:
        allergen, created = Allergen.objects.get_or_create(
            name=name,
            defaults={'icon': 'allergen-icons/default.png'}
        )
        if created:
            print(f"  ✓ {name}")


def create_dishes():
    """Crea piatti per il menu"""
    print("Creando piatti...")
    
    # Lista di piatti con ingredienti e allergeni
    dishes_data = [
        # PRIMI PIATTI
        {
            'name': 'Spaghetti alla Carbonara',
            'description': 'Pasta cremosa con guanciale, uova e pecorino romano',
            'ingredients': ['Pasta', 'Uova', 'Parmigiano', 'Prosciutto'],
            'allergens': ['Glutine', 'Uova', 'Lattosio']
        },
        {
            'name': 'Risotto ai Funghi Porcini',
            'description': 'Cremoso risotto mantecato con funghi porcini freschi',
            'ingredients': ['Riso', 'Funghi', 'Parmigiano'],
            'allergens': ['Lattosio']
        },
        {
            'name': 'Pasta al Pomodoro e Basilico',
            'description': 'Pasta con sugo di pomodoro fresco e basilico profumato',
            'ingredients': ['Pasta', 'Pomodoro', 'Basilico', 'Aglio'],
            'allergens': ['Glutine']
        },
        {
            'name': 'Lasagne della Nonna',
            'description': 'Lasagne tradizionali con ragù di carne e besciamella',
            'ingredients': ['Pasta', 'Carne bovina', 'Mozzarella', 'Pomodoro'],
            'allergens': ['Glutine', 'Lattosio', 'Uova']
        },
        {
            'name': 'Risotto alla Milanese',
            'description': 'Risotto allo zafferano, cremoso e dorato',
            'ingredients': ['Riso', 'Parmigiano'],
            'allergens': ['Lattosio']
        },
        
        # SECONDI PIATTI
        {
            'name': 'Pollo alle Erbe Aromatiche',
            'description': 'Petto di pollo grigliato con rosmarino e salvia',
            'ingredients': ['Pollo', 'Olio extravergine'],
            'allergens': []
        },
        {
            'name': 'Scaloppine al Limone',
            'description': 'Tenere fettine di vitello in salsa al limone',
            'ingredients': ['Carne bovina', 'Olio extravergine'],
            'allergens': []
        },
        {
            'name': 'Branzino al Sale',
            'description': 'Pesce fresco cotto in crosta di sale grosso',
            'ingredients': ['Pesce', 'Olio extravergine'],
            'allergens': ['Pesce']
        },
        {
            'name': 'Cotoletta alla Milanese',
            'description': 'Cotoletta impanata e dorata, croccante fuori e morbida dentro',
            'ingredients': ['Carne bovina', 'Uova'],
            'allergens': ['Glutine', 'Uova']
        },
        {
            'name': 'Salmone Grigliato',
            'description': 'Filetto di salmone grigliato con erbe mediterranee',
            'ingredients': ['Pesce', 'Olio extravergine'],
            'allergens': ['Pesce']
        },
        
        # CONTORNI
        {
            'name': 'Insalata Verde Mista',
            'description': 'Mix di insalate fresche con pomodorini e carote',
            'ingredients': ['Insalata', 'Pomodoro', 'Carote'],
            'allergens': []
        },
        {
            'name': 'Patate Arrosto al Rosmarino',
            'description': 'Patate dorate al forno con rosmarino fresco',
            'ingredients': ['Patate', 'Olio extravergine'],
            'allergens': []
        },
        {
            'name': 'Spinaci Saltati in Padella',
            'description': 'Spinaci freschi saltati con aglio e olio',
            'ingredients': ['Spinaci', 'Aglio', 'Olio extravergine'],
            'allergens': []
        },
        {
            'name': 'Zucchine alla Griglia',
            'description': 'Zucchine fresche grigliate con un filo d\'olio',
            'ingredients': ['Zucchine', 'Olio extravergine'],
            'allergens': []
        },
        {
            'name': 'Caponata Siciliana',
            'description': 'Mix di verdure mediterranee stufate',
            'ingredients': ['Zucchine', 'Pomodoro', 'Olio extravergine'],
            'allergens': []
        },
        
        # DOLCI E FRUTTA
        {
            'name': 'Tiramisù della Casa',
            'description': 'Il classico dolce italiano con mascarpone e caffè',
            'ingredients': ['Uova', 'Ricotta'],
            'allergens': ['Glutine', 'Uova', 'Lattosio']
        },
        {
            'name': 'Panna Cotta ai Frutti di Bosco',
            'description': 'Dolce cremoso con coulis di frutti rossi',
            'ingredients': ['Ricotta'],
            'allergens': ['Lattosio']
        },
        {
            'name': 'Frutta Fresca di Stagione',
            'description': 'Selezione di frutta fresca del giorno',
            'ingredients': [],
            'allergens': []
        },
        {
            'name': 'Gelato Artigianale',
            'description': 'Gelato prodotto con ingredienti naturali',
            'ingredients': ['Ricotta'],
            'allergens': ['Lattosio']
        },
        {
            'name': 'Crostata della Nonna',
            'description': 'Crostata di frutta con pasta frolla fatta in casa',
            'ingredients': ['Uova'],
            'allergens': ['Glutine', 'Uova', 'Lattosio']
        }
    ]
    
    created_dishes = []
    
    # Mapping diretto tra nomi piatti e file immagini
    dish_image_mapping = {
        'Spaghetti alla Carbonara': 'dish-photos/spaghetti_alla_carbonara.jpg',
        'Risotto ai Funghi Porcini': 'dish-photos/risotto_ai_funghi_porcini.jpg',
        'Pasta al Pomodoro e Basilico': 'dish-photos/pasta_al_pomodoro_e_basilico.jpg',
        'Lasagne della Nonna': 'dish-photos/lasagna_della_nonna.jpg',
        'Risotto alla Milanese': 'dish-photos/risotto_alla_milanese.jpg',
        'Pollo alle Erbe Aromatiche': 'dish-photos/pollo_alle_erbe_aromatiche.jpg',
        'Scaloppine al Limone': 'dish-photos/scaloppine_al_limone.jpg',
        'Branzino al Sale': 'dish-photos/branzino_al_sale.jpg',
        'Cotoletta alla Milanese': 'dish-photos/cotoletta_alla-milanese.jpg',
        'Salmone Grigliato': 'dish-photos/salmone_grigliato.jpg',
        'Insalata Verde Mista': 'dish-photos/insalata_verde_mista.jpg',
        'Patate Arrosto al Rosmarino': 'dish-photos/patate_arrosto_al_rosmarino.jpg',
        'Spinaci Saltati in Padella': 'dish-photos/spinaci_saltati_in_padella.jpg',
        'Zucchine alla Griglia': 'dish-photos/zucchine_alla_griglia.jpg',
        'Caponata Siciliana': 'dish-photos/caponata_alla_siciliana.jpg',
        'Tiramisù della Casa': 'dish-photos/tiramisu_della_casa.jpeg',
        'Panna Cotta ai Frutti di Bosco': 'dish-photos/pannacotta_ai_frutti_di_bosco.jpg',
        'Frutta Fresca di Stagione': 'dish-photos/frutta_fresca_di_stagione.jpg',
        'Gelato Artigianale': 'dish-photos/gelato_artigianale.jpg',
        'Crostata della Nonna': 'dish-photos/crostata_della_nonna.jpg'
    }
    
    print(f"Preparati {len(dish_image_mapping)} associazioni di immagini ai piatti")
    
    for dish_data in dishes_data:
        # Determina l'immagine da utilizzare
        img_path = dish_image_mapping.get(
            dish_data['name'], 'dish-photos/default.jpg'
        )
        
        # Crea il piatto
        dish, created = Dish.objects.get_or_create(
            name=dish_data['name'],
            defaults={
                'description': dish_data['description'],
                'img': img_path
            }
        )
        
        # Aggiorna l'immagine anche se il piatto esiste già
        if not created:
            dish.img = img_path
            dish.save()
            print(f"Aggiornata immagine per piatto esistente: {dish_data['name']}")
        
        if created:
            # Aggiungi ingredienti se esistono
            for ingredient_name in dish_data['ingredients']:
                try:
                    ingredient = Ingredient.objects.get(name=ingredient_name)
                    dish.ingredients.add(ingredient)
                except Ingredient.DoesNotExist:
                    pass
            
            # Aggiungi allergeni se esistono
            for allergen_name in dish_data['allergens']:
                try:
                    allergen = Allergen.objects.get(name=allergen_name)
                    dish.allergens.add(allergen)
                except Allergen.DoesNotExist:
                    pass
            
            print(f"  ✓ {dish_data['name']}")
            created_dishes.append(dish)
    
    return created_dishes


def create_menus():
    """Crea menu per tutte le mense per tutti i giorni della settimana"""
    print("Creando menu settimanali...")
    
    # Ottieni tutti i piatti per categoria
    primi = list(Dish.objects.filter(name__in=[
        'Spaghetti alla Carbonara', 'Risotto ai Funghi Porcini', 
        'Pasta al Pomodoro e Basilico', 'Lasagne della Nonna', 'Risotto alla Milanese'
    ]))
    
    secondi = list(Dish.objects.filter(name__in=[
        'Pollo alle Erbe Aromatiche', 'Scaloppine al Limone', 
        'Branzino al Sale', 'Cotoletta alla Milanese', 'Salmone Grigliato'
    ]))
    
    contorni = list(Dish.objects.filter(name__in=[
        'Insalata Verde Mista', 'Patate Arrosto al Rosmarino', 
        'Spinaci Saltati in Padella', 'Zucchine alla Griglia', 'Caponata Siciliana'
    ]))
    
    dolci = list(Dish.objects.filter(name__in=[
        'Tiramisù della Casa', 'Panna Cotta ai Frutti di Bosco', 
        'Frutta Fresca di Stagione', 'Gelato Artigianale', 'Crostata della Nonna'
    ]))
    
    print(f"Piatti disponibili: {len(primi)} primi, {len(secondi)} secondi, {len(contorni)} contorni, {len(dolci)} dolci")
    
    # Ottieni tutte le mense
    mense = list(Mensa.objects.all())
    print(f"Mense trovate: {len(mense)}")
    
    if not mense:
        print("⚠️  Nessuna mensa trovata! Assicurati di aver popolato le mense prima.")
        return
    
    day_names = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']
    part_names = ['Pranzo', 'Cena']
    
    menus_created = 0
    
    for mensa in mense:
        print(f"  Creando menu per: {mensa.name}")
        
        for weekday in range(7):  # 0=Lunedì, 6=Domenica
            for day_part in range(2):  # 0=Pranzo, 1=Cena
                
                # Crea il menu
                menu, created = Menu.objects.get_or_create(
                    mensa=mensa,
                    weekday=weekday,
                    day_part=day_part
                )
                
                if created:
                    # Seleziona piatti casuali per ogni categoria
                    if primi:
                        primo = random.choice(primi)
                        Includes.objects.create(menu=menu, dish=primo, type=0)
                    
                    if secondi:
                        secondo = random.choice(secondi)
                        Includes.objects.create(menu=menu, dish=secondo, type=1)
                    
                    if contorni:
                        contorno = random.choice(contorni)
                        Includes.objects.create(menu=menu, dish=contorno, type=2)
                    
                    if dolci:
                        dolce = random.choice(dolci)
                        Includes.objects.create(menu=menu, dish=dolce, type=3)
                    
                    menus_created += 1
                    print(f"    ✓ {day_names[weekday]} - {part_names[day_part]}")
    
    print(f"Menu creati: {menus_created}")


def main():
    """Funzione principale"""
    print("🍽️  POPOLAMENTO MENU MENSE")
    print("=" * 50)
    
    # Step 1: Pulisci dati esistenti
    clear_existing_data()
    
    # Step 2: Crea ingredienti
    create_ingredients()
    
    # Step 3: Crea allergeni  
    create_allergens()
    
    # Step 4: Crea piatti
    create_dishes()
    
    # Step 5: Crea menu
    create_menus()
    
    print("\n" + "=" * 50)
    print("✅ POPOLAMENTO COMPLETATO!")
    
    # Statistiche finali
    print(f"📊 Statistiche:")
    print(f"   • Ingredienti: {Ingredient.objects.count()}")
    print(f"   • Allergeni: {Allergen.objects.count()}")  
    print(f"   • Piatti: {Dish.objects.count()}")
    print(f"   • Menu: {Menu.objects.count()}")
    print(f"   • Relazioni menu-piatti: {Includes.objects.count()}")


if __name__ == "__main__":
    main()
