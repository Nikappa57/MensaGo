from django.shortcuts import get_object_or_404, render

from .models import City, Mensa


def mensa_city(request, city_name):
    city: City = get_object_or_404(City, name=city_name)
    mense = Mensa.objects.filter(city=city).all()
    context = {"city": city, "mense": mense}

    return render(request, "mensa/city.html", context)


def mensa_details(request, city_name, mensa_name):
    mensa: Mensa = get_object_or_404(Mensa,
                                     name=mensa_name,
                                     city__name=city_name)
    context = {"mensa": mensa, "current_user": request.user}

    return render(request, "mensa/details.html", context)
