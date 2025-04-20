from django.db import models


class Suffers(models.Model):
    """"
    Suffers(User,Allergen)
        F.k. Suffers[User] (= User[Email]
        F.k Suffers[Allergen](=Allergen[Name]
    """


    user = models.ForeignKey('apps.core.CustomUser', on_delete=models.CASCADE, related_name='suffers')
    allergen = models.ForeignKey('mensa.Allergen', on_delete=models.CASCADE, related_name='suffers')

    unique_together = ('user', 'allergen')  # Todo: check if it works(Django does not support composite primary keys)
    
    def __str__(self):
        return self.user.email + " - " + self.allergen.name

    
    
