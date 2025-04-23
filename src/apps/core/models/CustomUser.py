from decimal import Decimal
from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class EconomicalLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class CustomUser(AbstractUser):
    """"
    User(
        Email, 
        first_name, 
        last_name,
        propic, 
        credit, 
        university,
        economical level*)
    f.k User[University] (= University[Name]
    """

    propic = models.ImageField(upload_to='profile_pics/',
                               blank=True,
                               null=True)
    credit = models.DecimalField(max_digits=10,
                                 decimal_places=2,
                                 default=Decimal('0.00'))
    economical_level = models.CharField(max_length=10,
                                        choices=[(tag.name, tag.value)
                                                 for tag in EconomicalLevel],
                                        default=EconomicalLevel.LOW.name)
    university = models.ForeignKey('University', on_delete=models.PROTECT)

    suffers_from = models.ManyToManyField('mensa.Allergen',blank=True,related_name='suffers_from')

    likes = models.ManyToManyField('mensa.Dish', blank=True, related_name='likes')
    
    def __str__(self):
        return self.email
