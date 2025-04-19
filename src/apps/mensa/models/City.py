from django.db import models


class City(models.Model):
    """"
    City(Name, Landscape)
    """

    name = models.CharField(max_length=100, unique=True)
    landscape = models.ImageField(upload_to='landscapes/', blank=True, null=True)

    def __str__(self):
        return self.name

    
    
