from django.db import models


class Ingredient(models.Model):
    """"
    Ingredient(Name)
    """

    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return f"Ingredient(name={self.name})"

    def __repr__(self) -> str:
        return self.__str__()
