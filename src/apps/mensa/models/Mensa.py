from django.db import models


class Mensa(models.Model):
    """"
   Mensa(UUID,Name,Description,Position,Banner,Capacity,PhoneNumber*,City,Email*)
     F.k. Mensa[City](=City[Name]
     Chiave Mensa[Name]
    primary key UUID
    """

    uuid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    position = models.CharField(max_length=255)
    banner = models.ImageField(upload_to='banners/')
    capacity = models.IntegerField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    Gallery = models.ManyToManyField('PhotoMensa', blank=True)

    def __str__(self):
        return f'Mensa(uuid={self.uuid}, name={self.name}, description={self.description}, position={self.position}, banner={self.banner}, capacity={self.capacity}, phone_number={self.phone_number}, city={self.city}, email={self.email})'
    
    def __repr__(self) -> str:
        return self.__str__()

class PhotoMensa(models.Model):
    """"
    Photo(Img)
    """

    img = models.ImageField(upload_to='photos/')

    def __str__(self):
        return f"PhotoMensa(img={self.img})"

    def __repr__(self) -> str:
        return self.__str__()