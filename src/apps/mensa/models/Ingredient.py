from django.db import models


class Ingredient(models.Model):
    """"
    Ingredient(Name)
    """


    name = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.name

    
    
