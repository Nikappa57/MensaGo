from django.db import models


class Mensa(models.Model):
    """"
    Mensa(Name,Description,Position,Banner,Capacity,PhoneNumber*,City,Email*)
    f.k. Mensa[City] ⊆ City[Name]
    p.k  Mensa[Name]
    """

    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField()
    position = models.CharField(
        max_length=255)  # TODO: vedere come funzia per maps
    banner = models.ImageField(upload_to='banners/')
    capacity = models.IntegerField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    city = models.ForeignKey('City', on_delete=models.PROTECT)
    email = models.EmailField(blank=True, null=True)
    gallery = models.ManyToManyField('PhotoMensa')

    def __str__(self):
        return f'Mensa(name={self.name}, description={self.description}, position={self.position}, banner={self.banner}, capacity={self.capacity}, phone_number={self.phone_number}, city={self.city}, email={self.email})'

    def __repr__(self) -> str:
        return self.__str__()


class PhotoMensa(models.Model):
    """"
    PhotoMensa(Img)
    """

    img = models.ImageField(upload_to='photos/', unique=True)

    def __str__(self):
        return f"PhotoMensa(img={self.img})"

    def __repr__(self) -> str:
        return self.__str__()
