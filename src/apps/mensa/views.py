from django.shortcuts import get_object_or_404, redirect, render

from apps.world.utils import haversine

from .models import City, Mensa


def mensa_city(request, city_name):
    city: City = get_object_or_404(City, name=city_name)
    mense = Mensa.objects.filter(city=city).all()
    if len(mense) == 0:
        return redirect("home")

    user_lat = request.position['lat']
    user_lon = request.position['lon']

    for mensa in mense:
        mensa.distance = round(
            haversine(user_lat, user_lon, mensa.latitude, mensa.longitude), 2)

    mense = sorted(mense, key=lambda x: x.stars, reverse=True)

    context = {"city": city, "mense": mense}

    return render(request, "mensa/city.html", context)


def mensa_details(request, city_name, mensa_name):
    mensa: Mensa = get_object_or_404(Mensa,
                                     name=mensa_name,
                                     city__name=city_name)
    context = {"mensa": mensa, "current_user": request.user}

    return render(request, "mensa/details.html", context)
