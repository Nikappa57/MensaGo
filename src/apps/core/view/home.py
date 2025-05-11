from django.shortcuts import render
from apps.mensa.models import City, Event


def homepage(request):
    # Recupera tutte le città e gli eventi dal database
    cities = City.objects.all()
    events = Event.objects.all().order_by('date')
    
    context = {
        'cities': cities,
        'events': events,
    }
    return render(request, "index.html", context)
