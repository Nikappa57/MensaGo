from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.world.utils import haversine

from .models import City, Mensa, Dish


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
		# Check which day parts have opening hours for this weekday
		available_dayparts = Hours.objects.filter(mensa=mensa, weekday=weekday).values_list('daypart', flat=True)
		has_opening_hours = len(available_dayparts) > 0
				
		day_menus = Menu.objects.filter(mensa=mensa, weekday=weekday).order_by('day_part')
		day_menu_data = []
		
		# Always check both dayparts (0=Pranzo, 1=Cena)
		daypart_info = {}
		for daypart in [0, 1]:  # 0=Pranzo, 1=Cena
			daypart_info[daypart] = {
				'is_open': daypart in available_dayparts,
				'name': 'Pranzo' if daypart == 0 else 'Cena'
			}
		
		# Only process menus if the mensa is open that day
		if has_opening_hours:
			for menu in day_menus:
				# Only include menus for day parts that have opening hours
				if menu.day_part in available_dayparts:
					dishes_by_type = {}
					includes = Includes.objects.filter(menu=menu).select_related('dish')
					for include in includes:
						dish_type = include.get_type_display()
						if dish_type not in dishes_by_type:
							dishes_by_type[dish_type] = []
						dishes_by_type[dish_type].append(include.dish)
					
					day_menu_data.append({
						'day_part': menu.get_day_part_display(),
						'day_part_value': menu.day_part,
						'dishes_by_type': dishes_by_type
					})
		
		weekly_menus[weekday] = {
			'name': weekday_names[weekday],
			'menus': day_menu_data,
			'available_dayparts': list(available_dayparts),
			'daypart_info': daypart_info,
			'is_today': weekday == today and has_opening_hours,
			'is_open': has_opening_hours,
		}
	
	context = {
		"mensa": mensa, 
		"current_user": request.user,
		"hours_weekdays": hours_weekdays,
		"gallery": gallery,
		"weekly_menus": weekly_menus
	}

	return render(request, "mensa/details.html", context)


@login_required
@require_POST
def toggle_like_dish(request, dish_name):
	"""
	Toggle like/unlike for a dish. Only accessible to logged-in users.
	Returns JSON response with the new like status.
	"""
	dish = get_object_or_404(Dish, name=dish_name)
	user = request.user
	
	if dish in user.likes.all():
		# Remove like
		user.likes.remove(dish)
		liked = False
		message = f"Rimosso {dish.name} dai preferiti"
	else:
		# Add like
		user.likes.add(dish)
		liked = True
		message = f"Aggiunto {dish.name} ai preferiti"
	
	return JsonResponse({
		'liked': liked,
		'message': message,
		'dish_id': dish_name
	})


