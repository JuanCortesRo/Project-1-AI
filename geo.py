import math


def haversine_km(lat1, lon1, lat2, lon2):
    """Distancia geodésica aproximada en km entre dos coordenadas."""
    radius_km = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return radius_km * c


def calculate_geographic_midpoint(lat1, lon1, lat2, lon2):
    """Calcula el punto medio geográfico aproximado entre dos coordenadas."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    bx = math.cos(lat2) * math.cos(dlon)
    by = math.cos(lat2) * math.sin(dlon)
    lat3 = math.atan2(
        math.sin(lat1) + math.sin(lat2),
        math.sqrt((math.cos(lat1) + bx) ** 2 + by ** 2)
    )
    lon3 = lon1 + math.atan2(by, math.cos(lat1) + bx)
    return math.degrees(lat3), math.degrees(lon3)
