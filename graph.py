import folium
import json
from branca.element import Element
from geo import haversine_km, calculate_geographic_midpoint

# GRAFO
graph = {
    'Cali': {'Palmira': 28.5, 'Rozo': 27, 'Dagua' : 48, 'Yumbo' : 18.3, 'Jamundí' : 23.4, 'Candelaria' : 26.3, 'Puerto Tejada' : 35.8},
    'Palmira': {'Cali': 28.5, 'El Cerrito':20.5, 'Rozo' : 16.6, 'Candelaria' : 16, 'Pradera' : 18.9},
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
    'Candelaria' : {'Puerto Tejada' : 26.5, 'Cali' : 26.3, 'Palmira': 16, 'Florida' : 18, 'Pradera' : 14.2},
    'Corinto' : {'Florida' : 19, 'Santander de Quilichao' : 36.9, 'Puerto Tejada': 26.2},
    'Florida' : {'Corinto' : 19, 'Candelaria' : 18, 'Puerto Tejada' : 27.8, 'Pradera' : 14.5},
    'Pradera' : {'Palmira' : 18.9, 'Candelaria' : 14.2, 'Florida' : 14.5}
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
    'Pradera' : (3.4215776102533497, -76.24366085079745),
}

def get_map_html(path=None, algorithm="BFS", graph=None, show_heuristic=False, heuristic_goal=None):
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
    edge_opacity = 0.3 if show_heuristic else 0.6
    show_edge_labels = not show_heuristic

    # nodos
    path_set = set(path) if path else set()
    city_markers = {}
    for ciudad, (lat, lon) in coords.items():
        color = "red" if ciudad in path_set else "blue"
        marker = folium.Marker(
            location=[lat, lon],
            popup=ciudad,
            icon=folium.Icon(color=color)
        )
        marker.add_to(mapa)
        city_markers[ciudad] = marker

    dibujadas = set()
    for ciudad, vecinos in graph.items():
        if ciudad == 'heuristic' or ciudad not in coords:
            continue

        for vecino, distancia in vecinos.items():
            if vecino == 'heuristic' or vecino not in coords:
                continue

            if (vecino, ciudad) not in dibujadas:
                lat1, lon1 = coords[ciudad]
                lat2, lon2 = coords[vecino]

                folium.PolyLine(
                    locations=[[lat1, lon1], [lat2, lon2]],
                    color="blue",
                    weight=3,
                    opacity=edge_opacity
                ).add_to(mapa)

                if show_edge_labels:
                    mid_lat, mid_lon = calculate_geographic_midpoint(lat1, lon1, lat2, lon2)

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

    if show_heuristic and algorithm == "A*" and heuristic_goal in coords:
        goal_lat, goal_lon = coords[heuristic_goal]
        heuristic_lines = {}
        heuristic_label_ids = {}

        for idx, (ciudad, (lat, lon)) in enumerate(coords.items()):
            if ciudad == heuristic_goal:
                continue

            heur_dist = haversine_km(lat, lon, goal_lat, goal_lon)

            heur_line = folium.PolyLine(
                locations=[[lat, lon], [goal_lat, goal_lon]],
                color="#f39c12",
                weight=2,
                opacity=0.55,
                dash_array="6, 8"
            )
            heur_line.add_to(mapa)
            heuristic_lines[ciudad] = heur_line

            mid_lat, mid_lon = calculate_geographic_midpoint(lat, lon, goal_lat, goal_lon)
            label_id = f"heur-label-{idx}"
            heuristic_label_ids[ciudad] = label_id
            folium.Marker(
                location=[mid_lat, mid_lon],
                icon=folium.DivIcon(
                    html=f"""
                    <div id="{label_id}" style="
                        display: inline-block;
                        background-color: rgba(243,156,18,0.55);
                        padding: 3px 7px;
                        border-radius: 10px;
                        font-size: 10px;
                        font-weight: 700;
                        color: white;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.25);
                        white-space: nowrap;
                        text-align: center;
                        border: 1px solid rgba(255,255,255,0.5);
                    ">
                        h: {heur_dist:.1f} km
                    </div>
                    """,
                    icon_size=(70, 22),
                    icon_anchor=(35, 11),
                )
            ).add_to(mapa)

        if heuristic_lines:
            line_entries = ",\n".join(
                f"{json.dumps(city)}: {json.dumps(line.get_name())}"
                for city, line in heuristic_lines.items()
            )
            marker_entries = ",\n".join(
                f"{json.dumps(city)}: {json.dumps(marker.get_name())}"
                for city, marker in city_markers.items()
            )
            label_entries = ",\n".join(
                f"{json.dumps(city)}: {json.dumps(label_id)}"
                for city, label_id in heuristic_label_ids.items()
            )

            highlight_script = f"""
            <script>
            (function() {{
                const heuristicLineVarNames = {{
                    {line_entries}
                }};

                const cityMarkerVarNames = {{
                    {marker_entries}
                }};

                const heuristicLabelIds = {{
                    {label_entries}
                }};

                const defaultStyle = {{
                    color: '#f39c12',
                    weight: 2,
                    opacity: 0.55,
                    dashArray: '6, 8'
                }};

                const activeStyle = {{
                    color: '#f39c12',
                    weight: 4,
                    opacity: 1,
                    dashArray: null
                }};

                function resetHeuristicLabels() {{
                    Object.values(heuristicLabelIds).forEach((id) => {{
                        const el = document.getElementById(id);
                        if (el) {{
                            el.style.backgroundColor = 'rgba(243,156,18,0.55)';
                        }}
                    }});
                }}

                function resolveLayers(varMap) {{
                    const resolved = {{}};
                    Object.entries(varMap).forEach(([city, varName]) => {{
                        if (window[varName]) {{
                            resolved[city] = window[varName];
                        }}
                    }});
                    return resolved;
                }}

                function initHighlighting() {{
                    const heuristicLines = resolveLayers(heuristicLineVarNames);
                    const cityMarkers = resolveLayers(cityMarkerVarNames);

                    if (!Object.keys(heuristicLines).length || !Object.keys(cityMarkers).length) {{
                        setTimeout(initHighlighting, 120);
                        return;
                    }}

                    function resetHeuristicLines() {{
                        Object.values(heuristicLines).forEach((line) => line.setStyle(defaultStyle));
                        resetHeuristicLabels();
                    }}

                    function highlightCity(city) {{
                        resetHeuristicLines();
                        const line = heuristicLines[city];
                        if (line) {{
                            line.setStyle(activeStyle);
                            line.bringToFront();

                            const labelId = heuristicLabelIds[city];
                            const labelEl = labelId ? document.getElementById(labelId) : null;
                            if (labelEl) {{
                                labelEl.style.backgroundColor = 'rgba(243,156,18,0.92)';
                            }}
                        }}
                    }}

                    Object.keys(cityMarkers).forEach((city) => {{
                        cityMarkers[city].on('click', () => highlightCity(city));
                    }});
                }}

                initHighlighting();
            }})();
            </script>
            """
            mapa.get_root().html.add_child(Element(highlight_script))
                
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