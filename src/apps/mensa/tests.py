from datetime import date, time
from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from apps.core.models import CustomUser, EconomicalLevel, University

from .models import (Allergen, City, Dish, Event, Hours, Includes, Ingredient,
                     Mensa, Menu, Review)


class MensaModelsTestCase(TestCase):

    def setUp(self):
        # Create related objects
        self.city = City.objects.create(name="Rome", landscape="landscape.jpg")
        self.university = University.objects.create(name="Sapienza")
        self.economical_level = EconomicalLevel.objects.create(
            name="Standard", cost=Decimal("2.50"))
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            university=self.university,
            economical_level=self.economical_level)

    def test_city_creation(self):
        self.assertEqual(self.city.name, "Rome")
        self.assertEqual(self.city.landscape, "landscape.jpg")

    def test_mensa_creation(self):
        mensa = Mensa.objects.create(name="Mensa Centrale",
                                     description="Central Mensa",
                                     position="Via Roma 1",
                                     banner="banner.jpg",
                                     capacity=100,
                                     phone_number="1234567890",
                                     city=self.city,
                                     email="mensa@example.com")
        self.assertEqual(mensa.name, "Mensa Centrale")
        self.assertEqual(mensa.city, self.city)

    def test_review_creation(self):
        mensa = Mensa.objects.create(name="Mensa Centrale",
                                     description="Central Mensa",
                                     position="Via Roma 1",
                                     banner="banner.jpg",
                                     capacity=100,
                                     phone_number="1234567890",
                                     city=self.city,
                                     email="mensa@example.com")
        review = Review.objects.create(mensa=mensa,
                                       user=self.user,
                                       stars=5,
                                       text="Great food!")
        self.assertEqual(review.mensa, mensa)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.stars, 5)
        self.assertEqual(review.text, "Great food!")

    def test_menu_creation(self):
        mensa = Mensa.objects.create(name="Mensa Centrale",
                                     description="Central Mensa",
                                     position="Via Roma 1",
                                     banner="banner.jpg",
                                     capacity=100,
                                     phone_number="1234567890",
                                     city=self.city,
                                     email="mensa@example.com")
        menu = Menu.objects.create(mensa=mensa, weekday=0, day_part=0)
        self.assertEqual(menu.mensa, mensa)
        self.assertEqual(menu.weekday, 0)
        self.assertEqual(menu.day_part, 0)

    def test_dish_creation(self):
        ingredient = Ingredient.objects.create(name="Tomato")
        allergen = Allergen.objects.create(name="Gluten")
        dish = Dish.objects.create(name="Pasta",
                                   description="Delicious pasta",
                                   img="pasta.jpg")
        dish.ingredients.add(ingredient)
        dish.allergens.add(allergen)
        self.assertEqual(dish.name, "Pasta")
        self.assertIn(ingredient, dish.ingredients.all())
        self.assertIn(allergen, dish.allergens.all())

    def test_hours_creation(self):
        mensa = Mensa.objects.create(name="Mensa Centrale",
                                     description="Central Mensa",
                                     position="Via Roma 1",
                                     banner="banner.jpg",
                                     capacity=100,
                                     phone_number="1234567890",
                                     city=self.city,
                                     email="mensa@example.com")
        hours = Hours.objects.create(mensa=mensa,
                                     weekday=0,
                                     daypart=0,
                                     open_time=time(12, 0),
                                     close_time=time(14, 0))
        self.assertEqual(hours.mensa, mensa)
        self.assertEqual(hours.weekday, 0)
        self.assertEqual(hours.daypart, 0)
        self.assertEqual(hours.open_time, time(12, 0))
        self.assertEqual(hours.close_time, time(14, 0))

    def test_event_creation(self):
        event = Event.objects.create(name="Open Day",
                                     date=date(2025, 4, 28),
                                     img="openday.jpg")
        self.assertEqual(event.name, "Open Day")
        self.assertEqual(event.date, date(2025, 4, 28))
        self.assertEqual(event.img, "openday.jpg")

    def test_duplicate_review(self):
        print("Testing duplicate review creation...")
        mensa = Mensa.objects.create(name="Mensa Centrale",
                                     description="Central Mensa",
                                     position="Via Roma 1",
                                     banner="banner.jpg",
                                     capacity=100,
                                     phone_number="1234567890",
                                     city=self.city,
                                     email="mensa@example.com")
        Review.objects.create(mensa=mensa,
                              user=self.user,
                              stars=5,
                              text="Great food!")
        print("First review created successfully.")
        with self.assertRaises(IntegrityError):
            Review.objects.create(mensa=mensa,
                                  user=self.user,
                                  stars=4,
                                  text="Good food!")
        print("Duplicate review creation blocked as expected.")

    def test_hours_creation_and_overlap(self):
        print("Testing hours creation and overlap prevention...")
        mensa = Mensa.objects.create(name="Mensa Centrale",
                                     description="Central Mensa",
                                     position="Via Roma 1",
                                     banner="banner.jpg",
                                     capacity=100,
                                     phone_number="1234567890",
                                     city=self.city,
                                     email="mensa@example.com")
        Hours.objects.create(mensa=mensa,
                             weekday=0,
                             daypart=0,
                             open_time=time(12, 0),
                             close_time=time(14, 0))
        print("First hours created successfully.")
        with self.assertRaises(IntegrityError):
            Hours.objects.create(mensa=mensa,
                                 weekday=0,
                                 daypart=0,
                                 open_time=time(13, 0),
                                 close_time=time(15, 0))
        print("Overlapping hours creation blocked as expected.")

    def test_event_unique_constraint(self):
        print("Testing event unique constraint...")
        Event.objects.create(name="Open Day",
                             date=date(2025, 4, 28),
                             img="openday.jpg")
        print("First event created successfully.")
        with self.assertRaises(IntegrityError):
            Event.objects.create(name="Open Day",
                                 date=date(2025, 4, 28),
                                 img="openday_duplicate.jpg")
        print("Duplicate event creation blocked as expected.")

    def test_create_complete_menu(self):
        print("Testing creation of a complete menu...")
        mensa = Mensa.objects.create(name="Mensa Centrale",
                                     description="Central Mensa",
                                     position="Via Roma 1",
                                     banner="banner.jpg",
                                     capacity=100,
                                     phone_number="1234567890",
                                     city=self.city,
                                     email="mensa@example.com")
        for weekday in range(7):
            for day_part in range(2):
                menu = Menu.objects.create(mensa=mensa,
                                           weekday=weekday,
                                           day_part=day_part)
                print(
                    f"Created menu for weekday {weekday}, day part {day_part}."
                )
                self.assertEqual(menu.mensa, mensa)
                self.assertEqual(menu.weekday, weekday)
                self.assertEqual(menu.day_part, day_part)
        print("Complete menu created successfully.")

    def test_create_complete_hours(self):
        print("Testing creation of complete hours...")
        mensa = Mensa.objects.create(name="Mensa Centrale",
                                     description="Central Mensa",
                                     position="Via Roma 1",
                                     banner="banner.jpg",
                                     capacity=100,
                                     phone_number="1234567890",
                                     city=self.city,
                                     email="mensa@example.com")
        for weekday in range(7):
            for day_part in range(2):
                open_time = time(12, 0) if day_part == 0 else time(19, 0)
                close_time = time(14, 0) if day_part == 0 else time(21, 0)
                hours = Hours.objects.create(mensa=mensa,
                                             weekday=weekday,
                                             daypart=day_part,
                                             open_time=open_time,
                                             close_time=close_time)
                print(
                    f"Created hours for weekday {weekday}, day part {day_part}."
                )
                self.assertEqual(hours.mensa, mensa)
                self.assertEqual(hours.weekday, weekday)
                self.assertEqual(hours.daypart, day_part)
                self.assertEqual(hours.open_time, open_time)
                self.assertEqual(hours.close_time, close_time)
        print("Complete hours created successfully.")

    def test_create_complete_menu_with_dishes_using_includes_v1(self):
        print(
            "Testing creation of a complete menu with dishes using Includes..."
        )
        mensa = Mensa.objects.create(name="Mensa Centrale",
                                     description="Central Mensa",
                                     position="Via Roma 1",
                                     banner="banner.jpg",
                                     capacity=100,
                                     phone_number="1234567890",
                                     city=self.city,
                                     email="mensa@example.com")

        # Create some ingredients and dishes
        ingredient1 = Ingredient.objects.create(name="Tomato")
        ingredient2 = Ingredient.objects.create(name="Cheese")
        dish1 = Dish.objects.create(name="Pasta",
                                    description="Delicious pasta",
                                    img="pasta.jpg")
        dish2 = Dish.objects.create(name="Pizza",
                                    description="Cheesy pizza",
                                    img="pizza.jpg")
        dish1.ingredients.add(ingredient1)
        dish2.ingredients.add(ingredient2)

        for weekday in range(7):
            for day_part in range(2):
                menu = Menu.objects.create(mensa=mensa,
                                           weekday=weekday,
                                           day_part=day_part)
                Includes.objects.create(menu=menu, dish=dish1, type=0)  # Primo
                Includes.objects.create(menu=menu, dish=dish2,
                                        type=1)  # Secondo

                print(
                    f"Created menu for weekday {weekday}, day part {day_part} with dishes using Includes."
                )
                self.assertEqual(menu.mensa, mensa)
                self.assertEqual(menu.weekday, weekday)
                self.assertEqual(menu.day_part, day_part)
                self.assertIn(dish1, menu.dishes.all())
                self.assertIn(dish2, menu.dishes.all())
        print("Complete menu with dishes using Includes created successfully.")

    def test_create_complete_menu_with_dishes_using_includes_v2(self):
        print(
            "Testing creation of a complete menu with dishes using Includes..."
        )
        mensa = Mensa.objects.create(name="Mensa Centrale",
                                     description="Central Mensa",
                                     position="Via Roma 1",
                                     banner="banner.jpg",
                                     capacity=100,
                                     phone_number="1234567890",
                                     city=self.city,
                                     email="mensa@example.com")
        # Create some ingredients and dishes
        ingredient1 = Ingredient.objects.create(name="Tomato")
        ingredient2 = Ingredient.objects.create(name="Cheese")
        dish1 = Dish.objects.create(name="Pasta",
                                    description="Delicious pasta",
                                    img="pasta.jpg")
        dish2 = Dish.objects.create(name="Pizza",
                                    description="Cheesy pizza",
                                    img="pizza.jpg")
        dish1.ingredients.add(ingredient1)
        dish2.ingredients.add(ingredient2)
        for weekday in range(7):
            for day_part in range(2):
                menu = Menu.objects.create(mensa=mensa,
                                           weekday=weekday,
                                           day_part=day_part)
                menu.dishes.add(dish1, through_defaults={'type': 0})
                menu.dishes.add(dish2, through_defaults={'type': 1})
                print(
                    f"Created menu for weekday {weekday}, day part {day_part} with dishes using Includes."
                )
                self.assertEqual(menu.mensa, mensa)
                self.assertEqual(menu.weekday, weekday)
                self.assertEqual(menu.day_part, day_part)
                self.assertIn(dish1, menu.dishes.all())
                self.assertIn(dish2, menu.dishes.all())
        print("Complete menu with dishes using Includes created successfully.")
