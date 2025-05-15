from django.shortcuts import render
from django.http import JsonResponse
from apps.mensa.models import City, Event
from apps.core.forms import ContactForm


def homepage(request):
    # Recupera tutte le città e gli eventi dal database
    cities = City.objects.all()
    events = Event.objects.all().order_by('date')
    
    # Gestione del form di contatto
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Estrai i dati dal form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Stampa i dati sulla console del server
            print("================= CONTACT FORM DATA =================")
            print(f"Nome: {name}")
            print(f"Email: {email}")
            print(f"Messaggio: {message}")
            print("====================================================")
            
            # Ritorna una risposta JSON di successo
            return JsonResponse({'status': 'success', 'message': 'Messaggio inviato con successo!'})
        else:
            # Ritorna errori del form
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = ContactForm()
    
    context = {
        'cities': cities,
        'events': events,
        'form': form,
    }
    return render(request, "index.html", context)
