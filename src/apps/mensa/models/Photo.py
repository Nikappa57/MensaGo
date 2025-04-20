from django.db import models


class Photo(models.Model):
    """"
    Photo(Img)  
    """

    img = models.ImageField(upload_to='photos/', blank=True, null=True)
    
    def __str__(self):
        return self.img.name.split('/')[-1]  # Return the filename only

    
    
