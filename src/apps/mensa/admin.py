from django.contrib import admin

from .models import (Allergen, City, Dish, Event, Hours, Includes, Ingredient,
                     Mensa, Menu, PhotoMensa, Review)


class PhotoMensaInline(admin.TabularInline):
    model = PhotoMensa
    extra = 1


class MensaAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'position')
    list_filter = ('city', )
    search_fields = ('name', 'position', 'city__name')


class CityAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'latitude', 'longitude')


class AllergenAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', )


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', )


class DishAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', )


class EventAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'date')


class HoursAdmin(admin.ModelAdmin):
    list_display = ('mensa', 'weekday', 'daypart', 'open_time', 'close_time')
    list_filter = ('mensa', 'weekday', 'daypart')
    search_fields = ('mensa__name', )


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('mensa', 'user', 'stars')
    search_fields = ('mensa__name', 'user__email', 'user__first_name',
                     'user__last_name')
    list_filter = ('mensa', 'stars')


class IncludesInline(admin.TabularInline):
    model = Includes
    extra = 1


class MenuAdmin(admin.ModelAdmin):
    inlines = [IncludesInline]
    list_display = ('mensa', 'weekday', 'day_part')
    search_fields = ('mensa__name', )
    list_filter = ('mensa', 'weekday', 'day_part')


admin.site.register(Mensa, MensaAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Allergen, AllergenAdmin)
admin.site.register(Hours, HoursAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Event, EventAdmin)
