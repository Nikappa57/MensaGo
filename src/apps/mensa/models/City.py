from django.db import models


class City(models.Model):
    """"
    City(Name, Landscape, Latitude, Longitude)
    p.k. City[Name]
    """

    name = models.CharField(max_length=100, primary_key=True)
    landscape = models.ImageField(upload_to='landscapes/')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __str__(self):
        return f"City(name={self.name}, landscape={self.landscape})"

    def __repr__(self) -> str:
        return self.__str__()
