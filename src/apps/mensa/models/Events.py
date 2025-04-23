from django.db import models


class Event(models.Model):
    """"
    Event(Name, Date, Img)
    p.k. Event[name, date]
    """

    name = models.CharField(max_length=100)
    date = models.DateField()
    img = models.ImageField(upload_to='events/')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "date"],
                                    name="unique_name_date")
        ]
        ordering = ['date']

    def __str__(self):
        return f"Event(name={self.name}, date={self.date}, img={self.img})"

    def __repr__(self) -> str:
        return self.__str__()
