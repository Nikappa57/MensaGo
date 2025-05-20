import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def save_user_pos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        lat = data.get('lat')
        lon = data.get('lon')

        if lat is None or lon is None:
            return JsonResponse({'error': 'Invalid data'}, status=400)

        request.session['lat'] = lat
        request.session['lon'] = lon

        return JsonResponse({'status': 'ok', 'lat': lat, 'lon': lon})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
