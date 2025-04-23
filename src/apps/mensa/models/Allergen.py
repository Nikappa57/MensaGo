from django.db import models


class Allergen(models.Model):
    """"
    Allergen(Name)
    p.k. Allergen[Name]
    """

    name = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return f"Allergen(name={self.name})"

    def __repr__(self) -> str:
        return self.__str__()
