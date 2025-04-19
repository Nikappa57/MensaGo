from django.db import models


class Event(models.Model):
    """"
    Event(Name, Date, Img) primary key = name,date
    """

    name = models.CharField(max_length=100)
    date = models.DateField()
    unique_together = ('name', 'date') # Todo: check if it works(Django does not support composite primary keys)
    img = models.ImageField(upload_to='events/,blank=True, null=True')
    


    def __str__(self):
        return self.name
    
