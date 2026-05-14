"""
geo.py

Descripción: Utilidades geográficas para cálculo de distancias y puntos medios entre coordenadas.
Autores: JUAN JOSÉ CORTÉS RODRÍGUEZ, CARLOS MANUEL VILLAMIL GRISALES, JUAN DAVID CHARRY MEDINA, LAURA VALENTINA ARBELAEZ LEUDO

Proyecto 1 - IA - Universidad del Valle, 2026
"""

import math


def haversine_km(lat1, lon1, lat2, lon2):
    """Calcula la distancia aproximada entre dos coordenadas

    Parametros:
        lat1 (float): Latitud del punto de origen.
        lon1 (float): Longitud del punto de origen.
        lat2 (float): Latitud del punto de destino.
        lon2 (float): Longitud del punto de destino.

    Retorna:
        float: Distancia aproximada en kilometros usando la formula de Haversine.
    """
    radius_km = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    calc = radius_km * (2 * math.asin(math.sqrt(math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)))
    return calc


def calculate_geographic_midpoint(lat1, lon1, lat2, lon2):
    """Calcula el punto medio geografico aproximado entre dos coordenadas

    Parametros:
        lat1 (float): Latitud del punto de origen.
        lon1 (float): Longitud del punto de origen.
        lat2 (float): Latitud del punto de destino.
        lon2 (float): Longitud del punto de destino.

    Retorna:
        tuple[float, float]: Latitud y longitud del punto medio aproximado.
    """
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

