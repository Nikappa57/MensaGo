from django.db import models


class Dish(models.Model):
    """"
    Dish(Name, Desc, Img)
     p.k. Dish[Name]
    """

    name = models.CharField(max_length=100, unique=True, primary_key=True)
    description = models.TextField()
    img = models.ImageField(upload_to='dish-photos/')
    allergens = models.ManyToManyField('mensa.Allergen', blank=True)

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"Dish(name={self.name}, description={self.description}, img={self.img})"


class Menu(models.Model):
    """"
    Menu(Mensa,WeekDay,DayPart)
     f.k. Menu[Mensa] ⊆ Mensa[Name]
     incl. Menu[Mensa,WeekDay,DayPart] ⊆ Includes[Mensa,WeekDay,DayPart]
    """

    WEEKDAY = [
        (0, 'Lunedi'),
        (1, 'Martedi'),
        (2, 'Mercoledi'),
        (3, 'Giovedi'),
        (4, 'Venerdi'),
        (5, 'Sabato'),
        (6, 'Domenica'),
    ]

    DAY_PART = [
        (0, 'Pranzo'),
        (1, 'Cena'),
    ]

    mensa = models.ForeignKey('mensa.Mensa', on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAY)
    day_part = models.IntegerField(choices=DAY_PART)
    dishes = models.ManyToManyField('mensa.Dish', through='Includes', blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mensa', 'weekday', 'day_part'],
                                    name='menu_unique_mensa_weekday_daypart')
        ]
        ordering = ['weekday', 'day_part']

    def __str__(self):
        return f"{self.mensa} {self.weekday} {self.day_part}"

    def __repr__(self) -> str:
        return f"Menu(mensa={self.mensa}, weekday={self.weekday}, day_part={self.day_part})"


class Includes(models.Model):
    """
    Include(Menu,Dish,type)
    """

    TYPE = [
        (0, 'Primo'),
        (1, 'Secondo'),
        (2, 'Contorno'),
        (3, 'Dessert/Frutta'),
    ]

    menu = models.ForeignKey('mensa.Menu', on_delete=models.CASCADE)
    dish = models.ForeignKey('mensa.Dish', on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['menu', 'dish'],
                                    name='unique_menu_dish')
        ]

    def __str__(self):
        return f"{self.menu} - {self.dish} ({self.type})"

    def __repr__(self) -> str:
        return f"Includes(menu={self.menu}, dish={self.dish}, type={self.type})"
