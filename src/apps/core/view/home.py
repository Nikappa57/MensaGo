from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

from apps.core.forms import ContactForm
from apps.mensa.models import City, Event
from apps.world.utils import haversine


def homepage(request):
    cities = City.objects.all()
    user_lat = request.position['lat']
    user_lon = request.position['lon']

    def distance(city):
        print("city:", city)
        print("user_lat:", user_lat)
        print("user_lon:", user_lon)
        return haversine(user_lon, user_lat, city.longitude, city.latitude)

    if request.position['valid']:
        cities = sorted(cities, key=distance)
        print("Sorted cities:", cities)

    events = Event.objects.all().order_by('date')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send mail to settings.CONTACT_MAIL
            send_mail(subject=f"Messaggio da {name} ({email})",
                      message=message,
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[settings.CONTACT_EMAIL],
                      fail_silently=False)

            return JsonResponse({
                'status': 'success',
                'message': 'Messaggio inviato con successo!'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            },
                                status=400)
    else:
        form = ContactForm()

    context = {
        'cities': cities,
        'events': events,
        'form': form,
    }

    print("lat:", request.position['lat'])
    print("lon:", request.position['lon'])

    return render(request, "index.html", context)
