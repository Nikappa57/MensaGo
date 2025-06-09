from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..manager import CustomUserManager


class EconomicalLevel(models.Model):
    """
    EconomicalLevel(Name,cost)
    p.k EconomicalLevel[Name]
    """

    name = models.CharField(max_length=100, primary_key=True)
    cost = models.DecimalField(max_digits=5,
                               decimal_places=2,
                               default=Decimal('0.00'))

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"EconomicalLevel(name={self.name}, cost={self.cost})"


class CustomUser(AbstractUser):
    """"
    User(
        Email,
        first_name,
        last_name,
        propic,
        credit,
        university,
        economical level)
    f.k User[University] ⊆ University[Name]
    """

    username = None
    email = models.EmailField(_("email address"), unique=True)
    propic = models.ImageField(upload_to='profile_pics/',
                               default='profile_pics/default.jpg')
    credit = models.DecimalField(max_digits=10,
                                 decimal_places=2,
                                 default=Decimal('0.00'))
    economical_level = models.ForeignKey('EconomicalLevel',
                                         on_delete=models.PROTECT,
                                         null=True,
                                         blank=True)
    university = models.ForeignKey('University',
                                   on_delete=models.PROTECT,
                                   null=True,
                                   blank=True)
    suffers_from = models.ManyToManyField('mensa.Allergen', blank=True)
    likes = models.ManyToManyField('mensa.Dish', blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects: CustomUserManager = CustomUserManager()

    def __str__(self):
        return self.email

    def __repr__(self) -> str:
        return (
            f"User(email={self.email}, first_name={self.first_name}, "
            f"last_name={self.last_name}, propic={self.propic}, credit={self.credit}, "
            f"economical_level={self.economical_level}, university={self.university})"
        )
