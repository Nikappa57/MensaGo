from django.db import models


class Dish(models.Model):
    """"
    Dish(Name, Desc, Img)
     incl. Dish[Name] (= Contains[Dish]
     p.k. Dish[Name]
    """

    name = models.CharField(max_length=100, unique=True, primary_key=True)
    description = models.TextField()
    img = models.ImageField(upload_to='dish-photos/')
    ingredients = models.ManyToManyField('mensa.Ingredient',
                                         related_name='dishes')
    allergens = models.ManyToManyField('mensa.Allergen', related_name='dishes')

    def save(self, *args, **kwargs) -> None:
        """
        Save the dish instance to the database.
        """

        if len(self.ingredients.all()) == 0: # TODO: controlla se si può fare con if not self.ingredients
            raise ValueError("Dish must contain at least one ingredient.")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Dish(name={self.name}, description={self.description}, img={self.img})"

    def __repr__(self) -> str:
        return self.__str__()


class Menu(models.Model):
    """"
    Menu(Mensa,WeekDay,DayPart)
     f.k. Menu[Mensa] (= Mensa[UUID]
     Inclusione Menu[Mensa,WeekDay,DayPart] (= Includes[Mensa,WeekDay,DayPart]
     vincolo esterno Menu[Mensa] partecipa a menu al massimo 14 volte
    Includes dish with attribute type (ManyToMany)
    """

    WEEKDAY = {
        (0, 'Lunedi'),
        (1, 'Martedi'),
        (2, 'Mercoledi'),
        (3, 'Giovedi'),
        (4, 'Venerdi'),
        (5, 'Sabato'),
        (6, 'Domenica'),
    }

    DAY_PART = {
        (0, 'Pranzo'),
        (1, 'Cena'),
    }

    mensa = models.ForeignKey('mensa.Mensa', on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAY)
    day_part = models.IntegerField(choices=DAY_PART)
    dishes = models.ManyToManyField('mensa.Dish',
                                    through='Include',
                                    related_name='menus')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mensa', 'weekday', 'day_part'],
                                    name='unique_mensa_weekday_daypart')
        ]
        ordering = ['weekday', 'day_part']

    def __str__(self):
        return f"Menu(mensa={self.mensa}, weekday={self.weekday}, day_part={self.day_part})"
    def __repr__(self) -> str:
        return self.__str__()


class Include(models.Model):
    """
    Include(Mensa,WeekDay,DayPart,Dish,type)
    """

    TYPE = {
        (0, 'Primo'),
        (1, 'Secondo'),
        (2, 'Contorno'),
        (3, 'Dessert/Frutta'),
    }

    menu = models.ForeignKey('mensa.Menu', on_delete=models.CASCADE)
    dish = models.ForeignKey('mensa.Dish', on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['menu', 'dish'],
                                    name='unique_menu_dish')
        ]

    def __str__(self) -> str:
        return f"menu: {self.menu}, dish: {self.dish}, type: {self.type}"

    def __repr__(self) -> str:
        return self.__str__()
