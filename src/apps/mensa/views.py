from django.shortcuts import get_object_or_404, render

from .models import City, Mensa


from apps.world.utils import haversine

def mensa_city(request, city_name):
    city: City = get_object_or_404(City, name=city_name)
    mense = Mensa.objects.filter(city=city).all()
    user_lat = request.position['lat']
    user_lon = request.position['lon']

    def distance(mensa):
        if(mensa.latitude is None or mensa.longitude is None):
            return haversine(user_lon, user_lat, city.longitude, city.latitude)
        return haversine(user_lon, user_lat, mensa.longitude, mensa.latitude)

    if request.position['valid']:
        mense = sorted(mense, key=distance)
        print("Sorted mense:", mense)

    context = {"city": city, "mense": mense}

    return render(request, "mensa/city.html", context)




def mensa_details(request, city_name, mensa_name):
    mensa: Mensa = get_object_or_404(Mensa,
                                     name=mensa_name,
                                     city__name=city_name)
    
    from .models.Hours import Hours
    from .models.Menu import Menu, Includes
    from datetime import datetime
    
    # Get the weekday choices
    hours_weekdays = dict(Hours.WEEKDAY)
    hours_weekdays = sorted(hours_weekdays.items())
    gallery = mensa.gallery.all()
    
    # Get weekly menus
    weekly_menus = {}
    weekday_names = {
        0: 'Lunedì',
        1: 'Martedì', 
        2: 'Mercoledì',
        3: 'Giovedì',
        4: 'Venerdì',
        5: 'Sabato',
        6: 'Domenica'
    }
    
    today = datetime.now().weekday()  # Monday = 0, Sunday = 6
    
    for weekday in range(7):  # 0-6 (Monday to Sunday)
        day_menus = Menu.objects.filter(mensa=mensa, weekday=weekday).order_by('day_part')
        day_menu_data = []
        
        for menu in day_menus:
            dishes_by_type = {}
            includes = Includes.objects.filter(menu=menu).select_related('dish')
            for include in includes:
                dish_type = include.get_type_display()
                if dish_type not in dishes_by_type:
                    dishes_by_type[dish_type] = []
                dishes_by_type[dish_type].append(include.dish)
            
            day_menu_data.append({
                'day_part': menu.get_day_part_display(),
                'dishes_by_type': dishes_by_type
            })
        
        weekly_menus[weekday] = {
            'name': weekday_names[weekday],
            'menus': day_menu_data,
            'is_today': weekday == today
        }
    
    context = {
        "mensa": mensa, 
        "current_user": request.user,
        "hours_weekdays": hours_weekdays,
        "gallery": gallery,
        "weekly_menus": weekly_menus
    }

    return render(request, "mensa/details.html", context)
