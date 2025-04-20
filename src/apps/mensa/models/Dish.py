from django.db import models


class Dish(models.Model):
    """"
    Dish(Name, Desc, Img)
     incl. Dish[Name] (= Contains[Dish]
    """


    name = models.CharField(max_length=100, unique=True, primary_key=True)
    description = models.TextField()
    img = models.ImageField(upload_to='photos/', blank=True, null=True)
    ingredients = models.ManyToManyField('Ingredient', blank=True, related_name='dishes')

    def __str__(self):
        return self.name

    
    
