class PositionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """ Save user position in request object """

        lat = request.session.get('lat')
        lon = request.session.get('lon')

        request.position = {
            'lat': float(lat) if lat else None,
            'lon': float(lon) if lon else None,
            'valid': lat is not None and lon is not None,
        }

        return self.get_response(request)
