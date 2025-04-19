from django.db import models


class Gallery(models.Model):
    """"
    Gallery(Mensa, Photo)
    """
    mensa = models.ForeignKey('mensa.Mensa', on_delete=models.CASCADE, related_name='gallery')
    photo = models.ForeignKey('mensa.Photo',on_delete=models.SET_NULL, related_name='gallery')

    def __str__(self):
        return f"{self.mensa} - {self.photo}"

    
