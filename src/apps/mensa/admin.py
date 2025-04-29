from django.contrib import admin
from .models import (
    Allergen,
    City,
    Event,
    Hours,
    Ingredient,
    Mensa,
    PhotoMensa,
    Dish,
    Includes,
    Menu,
    Review
)

# Registrazione dei modelli base
admin.site.register(Allergen)
admin.site.register(City)
admin.site.register(Event)
admin.site.register(Hours)
admin.site.register(Ingredient)

# Admin personalizzato per Mensa con inline per le foto
class PhotoMensaInline(admin.TabularInline):
    model = PhotoMensa
    extra = 1

class MensaAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)
    search_fields = ('name', 'address')

admin.site.register(Mensa, MensaAdmin)

# Admin personalizzato per Menu con inline per i piatti
class IncludesInline(admin.TabularInline):
    model = Includes
    extra = 1

class MenuAdmin(admin.ModelAdmin):
    inlines = [IncludesInline]
    

admin.site.register(Menu, MenuAdmin)
admin.site.register(Dish)
admin.site.register(Review)
