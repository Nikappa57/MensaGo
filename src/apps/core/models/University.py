from django.db import models


class University(models.Model):
    """"
    University(Name)
    """

    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"University(name={self.name})"
