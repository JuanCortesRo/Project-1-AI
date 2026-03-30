import folium
import math

# GRAFO
graph = {
    'Cali': {'Palmira': 28.5, 'Rozo': 27, 'Dagua' : 48, 'Yumbo' : 18.3, 'Jamundí' : 23.4, 'Candelaria' : 26.3, 'Puerto Tejada' : 35.8},
    'Palmira': {'Cali': 28.5, 'El Cerrito':20.5, 'Rozo' : 16.6, 'Candelaria' : 16},
    'El Cerrito': {'Palmira': 20.5, 'Rozo' : 13.8, 'Guacarí' : 9.7},
    'Rozo' : {'Cali': 27, 'Palmira' : 16.6, 'El Cerrito' : 13.8, 'Mulaló' : 10.5},
    'Buga' : {'Guacarí' : 18.1, 'Yotoco' : 7.9, 'Tuluá' : 27.8},
    'Mulaló' : {'Rozo' : 10.5, 'Vijes' : 10.4, 'Yumbo' : 6.1},
    'Vijes' : {'Mulaló' : 10.4, 'Yotoco' : 28.3, 'Calima' : 30.6},
    'Guacarí' : {'El Cerrito' : 9.7, 'Buga' : 18.1},
    'Yotoco' : {'Buga' : 7.9, 'Vijes' : 28.3, 'Calima' : 25.5},
    'Tuluá' : {'Buga' : 27.8},
    'Dagua' : {'Cali' : 48, 'Lobo Guerrero' : 13.3},
    'Yumbo' : {'Cali' : 18.3, 'Mulaló' : 6.1},
    'Calima' : {'Lobo Guerrero' : 24.5, 'Yotoco' : 25.5, 'Vijes': 30.6},
    'Lobo Guerrero' : {'Calima' : 24.5, 'Dagua' : 13.3, 'Buenaventura' : 50},
    'Buenaventura' : {'Lobo Guerrero' : 50},
    'Jamundí' : {'Cali' : 23.4, 'Puerto Tejada' : 23.5, 'Santander de Quilichao' : 33},
    'Puerto Tejada' : {'Jamundí' : 23.5, 'Santander de Quilichao' : 26.7, 'Candelaria' : 26.5, 'Cali' : 35.8, 'Corinto' : 26.2, 'Florida' : 27.8},
    'Santander de Quilichao' : {'Puerto Tejada' : 26.7, 'Jamundí' : 33, 'Corinto': 36.9},
    'Candelaria' : {'Puerto Tejada' : 26.5, 'Cali' : 26.3, 'Palmira': 16, 'Florida' : 18},
    'Corinto' : {'Florida' : 19, 'Santander de Quilichao' : 36.9, 'Puerto Tejada': 26.2},
    'Florida' : {'Corinto' : 19, 'Candelaria' : 18, 'Puerto Tejada' : 27.8}
}

# COORDENADAS
coords = {
    'Cali': (3.4479129327977103, -76.53241229310366),
    'Palmira': (3.5375794648769365, -76.3162299504712),
    'El Cerrito': (3.68350795638867, -76.31331267695438),
    'Rozo' : (3.6158979069578394, -76.39688773075113),
    'Buga' : (3.8953841331042707, -76.30273326493281),
    'Mulaló' : (3.6321437790944806, -76.47117223606111),
    'Vijes' : (3.69561781817302, -76.4376737764281),
    'Guacarí' : (3.7651159286901907, -76.33135876240381),
    'Yotoco' : (3.8917230577718303, -76.3720957189082),
    'Tuluá' : (4.082290591951527, -76.19619549974745),
    'Buenaventura' : (3.871917400105139, -76.99242021713145),
    'Lobo Guerrero' : (3.7610208247341723, -76.66497635143317),
    'Calima' : (3.872930207334682, -76.5334468417096),
    'Dagua' : (3.656828462916506, -76.6890032028438),
    'Yumbo' : (3.5823717606593504, -76.49262447180307),
    'Jamundí' : (3.263946423456881, -76.53280736292925),
    'Puerto Tejada' : (3.2222214045563082, -76.41725207217368),
    'Santander de Quilichao' : (3.016461446768818, -76.48246053361977),
    'Candelaria' : (3.4086555009976185, -76.35004435108867),
    'Corinto' : (3.176145892399019, -76.26204308386959),
    'Florida' : (3.323456370369777, -76.23782689315841),
}

def punto_medio(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    Bx = math.cos(lat2) * math.cos(dlon)
    By = math.cos(lat2) * math.sin(dlon)
    lat3 = math.atan2(
        math.sin(lat1) + math.sin(lat2),
        math.sqrt((math.cos(lat1) + Bx)**2 + By**2)
    )
    lon3 = lon1 + math.atan2(By, math.cos(lat1) + Bx)
    return math.degrees(lat3), math.degrees(lon3)

def get_map_html(path=None, algorithm="BFS", graph=None):
    if graph is None:
        from graph import graph as default_graph
        graph = default_graph
    mapa = folium.Map(location=[3.45, -76.53], zoom_start=10)

    colors = {
        "BFS": "#1f77ff",
        "DFS": "#8e44ad",
        "UCS": "#27ae60",
        "A*": "#f39c12"
    }

    route_color = colors.get(algorithm, "#ff0000")

    # nodos
    path_set = set(path) if path else set()
    for ciudad, (lat, lon) in coords.items():
        color = "red" if ciudad in path_set else "blue"
        folium.Marker(
            location=[lat, lon],
            popup=ciudad,
            icon=folium.Icon(color=color)
        ).add_to(mapa)

    dibujadas = set()
    for ciudad, vecinos in graph.items():
        for vecino, distancia in vecinos.items():
            if (vecino, ciudad) not in dibujadas:
                lat1, lon1 = coords[ciudad]
                lat2, lon2 = coords[vecino]

                folium.PolyLine(
                    locations=[[lat1, lon1], [lat2, lon2]],
                    color="blue",
                    weight=3,
                    opacity=0.6
                ).add_to(mapa)

                mid_lat, mid_lon = punto_medio(lat1, lon1, lat2, lon2)

                folium.Marker(
                    location=[mid_lat, mid_lon],
                    icon=folium.DivIcon(
                        html=f"""
                        <div style="
                            display: inline-block;
                            background-color: rgba(255,255,255,0.95);
                            padding: 4px 8px;
                            border-radius: 12px;
                            font-size: 11px;
                            font-weight: 600;
                            color: #333;
                            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
                            border: 1px solid rgba(0,0,0,0.2);
                            white-space: nowrap;
                            text-align: center;
                        ">
                            {distancia} km
                        </div>
                        """,
                        icon_size=(60, 25),     
                        icon_anchor=(30, 12),
                    )
                ).add_to(mapa)

                dibujadas.add((ciudad, vecino))
                
    if path and len(path) > 1:
        for i in range(len(path) - 1):
            lat1, lon1 = coords[path[i]]
            lat2, lon2 = coords[path[i+1]]

            folium.PolyLine(
                locations=[[lat1, lon1], [lat2, lon2]],
                color=route_color,
                weight=6,
                opacity=1
            ).add_to(mapa)

    return mapa._repr_html_()