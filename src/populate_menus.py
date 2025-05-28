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

from apps.mensa.models import Mensa, Menu, Dish, Includes, Allergen
from PIL import Image
from io import BytesIO
import random


from apps.mensa.models import Mensa
from apps.mensa.models.Menu import Menu, Dish, Includes
from apps.mensa.models.Allergen import Allergen
import random



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
