from urllib import request

from django.db import models


class Mensa(models.Model):
    """
    Mensa(Name,Description,Position,Banner,Capacity,PhoneNumber*,City,Email*,Latitude*,Longitude*)
    f.k. Mensa[City] ⊆ City[Name]
    p.k  Mensa[Name]
    """
    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField()
    position = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    banner = models.ImageField(upload_to='banners/')
    capacity = models.IntegerField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    city = models.ForeignKey('City', on_delete=models.PROTECT)
    email = models.EmailField(blank=True, null=True)
    gallery = models.ManyToManyField('PhotoMensa')
    amenities = models.ManyToManyField('AmenitiesMensa', blank=True)

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return (
            f"Mensa(name={self.name}, description={self.description}, position={self.position}, "
            f"banner={self.banner}, capacity={self.capacity}, phone_number={self.phone_number}, "
            f"city={self.city}, email={self.email})")

    def save(self, *args, **kwargs):
        # If position changed or coordinates are missing, update coordinates
        if not self.pk or not self.latitude or not self.longitude:
            self.geocode_address()
        super().save(*args, **kwargs)

    @property
    def stars(self):
        """media delle stelle di Reviews"""
        reviews = self.review_set.all()
        if not reviews:
            return 0
        return sum(review.stars for review in reviews) // len(reviews)

    def geocode_address(self):
        """
        Use Nominatim to convert the address to coordinates
        """
        import json
        import time
        from urllib import parse

        from django.conf import settings

        # Construct the full address including city
        full_address = f"{self.position}, {self.city.name}, Italy"

        # Nominatim API endpoint
        url = "https://nominatim.openstreetmap.org/search"

        # Request headers with a valid user agent (required by Nominatim)
        headers = {'User-Agent': 'MensaGO/1.0 (smartcanteen@example.com)'}

        # Query parameters
        params = {'q': full_address, 'format': 'json', 'limit': 1}

        try:
            # Make the request with a 1-second delay (Nominatim usage policy)
            time.sleep(1)
            query_string = parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            print(full_url)
            req = request.Request(full_url, headers=headers)
            with request.urlopen(req) as response:
                if response.status != 200:
                    raise Exception(f"Error: {response.status}")
                data = response.read()
                results = json.loads(data)
                if results:
                    self.latitude = float(results[0]['lat'])
                    self.longitude = float(results[0]['lon'])
                    return True

        except Exception as e:
            if settings.DEBUG:
                print(f"Geocoding error for {self.name}: {str(e)}")
        return False


class PhotoMensa(models.Model):
    """"
    PhotoMensa(Img)
    """

    img = models.ImageField(upload_to='photos/', unique=True)

    def __str__(self):
        return str(self.img)

    def __repr__(self) -> str:
        return f"PhotoMensa(img={self.img})"

class AmenitiesMensa(models.Model):
    """"
    Amenities(text, icon)
    """

    text = models.CharField(max_length=255, unique=True)
    icon = models.CharField(max_length=255)

    def __str__(self):
        return self.text

    def __repr__(self) -> str:
        return f"AmenitiesMensa(text={self.text}, icon={self.icon})"
