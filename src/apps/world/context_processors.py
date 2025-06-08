def position_context(request):

    pos = request.position
    if pos is not None:
        lat = pos.get('lat')
        lon = pos.get('lon')
        if lat is not None and lon is not None:
            return {
                'pos': {
                    'lat': lat,
                    'lon': lon,
                }
            }
    return {}
