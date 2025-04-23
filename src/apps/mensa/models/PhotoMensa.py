from django.db import models


class PhotoMensa(models.Model):
    """"
    Photo(Img)
    """

    img = models.ImageField(upload_to='photos/')

    def __str__(self):
        return f"Photo(img={self.img})"

    def __repr__(self) -> str:
        return self.__str__()
