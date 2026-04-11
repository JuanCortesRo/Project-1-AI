"""
app.py

Descripción: Aplicación web Flask para visualizar y comparar algoritmos de búsqueda sobre el grafo del proyecto.
Autores: JUAN JOSÉ CORTÉS RODRÍGUEZ, CARLOS MANUEL VILLAMIL GRISALES, JUAN DAVID CHARRY MEDINA, LAURA VALENTINA ARBELAEZ LEUDO

Proyecto 1 - IA - Universidad del Valle, 2026
"""

from flask import Flask, render_template, request
import importlib
from graph import graph, coords, get_map_html
from geo import haversine_km

app = Flask(__name__)

ALGORITHMS = {
    "BFS": "bfs",
    "DFS": "dfs",
    "UCS": "ucs",
    "A*": "astar",
}

def build_heuristic(goal):
    """Construye la heuristica de distancia para A* respecto a una meta.

    Parametros:
        goal (str): Ciudad objetivo para calcular h(n).

    Retorna:
        dict: Diccionario ciudad -> distancia Haversine hasta la meta.
    """
    if goal not in coords:
        return {}

    goal_lat, goal_lon = coords[goal]
    heuristic = {
        city: haversine_km(lat, lon, goal_lat, goal_lon)
        for city, (lat, lon) in coords.items()
    }
    heuristic[goal] = 0.0
    return heuristic


def resolve_search_state(req):
    """Procesa el estado de busqueda a partir de la solicitud HTTP.

    Parametros:
        req (Request): Objeto request de Flask con formulario y metodo.

    Retorna:
        dict: Estado completo para renderizar vista y mapa (camino, costo, errores y opciones UI).
    """
    path = []
    cost = None
    error = None
    show_heuristic = False
    algo_logs = []
    algo_stats = None

    selected_algorithm = "BFS"
    selected_start = "Cali"
    selected_goal = "Buga"

    import json
    from graph import graph as default_graph
    original_graph_json = json.dumps(default_graph, indent=4, ensure_ascii=False)

    graph_json = json.dumps(graph, indent=4, ensure_ascii=False)
    custom_graph = graph

    if req.method == "POST":
        selected_algorithm = req.form["algorithm"]
        selected_start = req.form["start"]
        selected_goal = req.form["goal"]
        show_heuristic = req.form.get("showHeuristic", "0") in ("1", "true", "on")
        graph_input = req.form.get("graphInput")
        if graph_input:
            try:
                custom_graph = json.loads(graph_input)
                graph_json = graph_input
            except Exception as e:
                error = f"Error en el formato del grafo: {e}"

        try:
            algo_module = importlib.import_module(
                f"algorithms.{ALGORITHMS[selected_algorithm]}"
            )

            search_graph = custom_graph
            if selected_algorithm == "A*":
                search_graph = dict(custom_graph)
                search_graph["heuristic"] = build_heuristic(selected_goal)

            result = algo_module.search(search_graph, selected_start, selected_goal)

            if isinstance(result, dict):
                path = result.get("path")
                cost = result.get("cost")
                algo_logs = result.get("logs", [])
                algo_stats = result.get("stats")
            elif isinstance(result, tuple):
                path, cost = result
            else:
                path = result

            if path is None and not error:
                error = "No se encontró camino entre los nodos seleccionados."
        except Exception as e:
            if not error:
                error = str(e)

    split_map = show_heuristic and selected_algorithm == "A*"
    map_left_html = get_map_html(path, selected_algorithm, graph=custom_graph)
    map_right_html = None
    if split_map:
        map_right_html = get_map_html(
            path=None,
            algorithm=selected_algorithm,
            graph=custom_graph,
            show_heuristic=True,
            heuristic_goal=selected_goal,
        )

    return {
        "path": path,
        "cost": cost,
        "error": error,
        "show_heuristic": show_heuristic,
        "algo_logs": algo_logs,
        "algo_stats": algo_stats,
        "selected_algorithm": selected_algorithm,
        "selected_start": selected_start,
        "selected_goal": selected_goal,
        "graph_json": graph_json,
        "original_graph_json": original_graph_json,
        "custom_graph": custom_graph,
        "split_map": split_map,
        "map_left_html": map_left_html,
        "map_right_html": map_right_html,
    }

@app.route("/health")
def health():
    """Endpoint que se utiliza para realizar solicitudes constantes al programa en despliegue para que no se duerma

    Parametros:
        Ninguno.

    Retorna:
        tuple[str, int]: Texto de estado y codigo HTTP 200.
    """
    return "todo ok", 200

@app.route("/", methods=["GET", "POST"])
def index():
    """Renderiza la pagina principal con resultados de busqueda.

    Parametros:
        Ninguno.

    Retorna:
        str: HTML renderizado del template principal.
    """
    state = resolve_search_state(request)

    return render_template(
        "index.html",
        algorithms=ALGORITHMS.keys(),
        nodes=[node for node in state["custom_graph"].keys() if node != "heuristic"],
        path=state["path"],
        cost=state["cost"],
        error=state["error"],
        algo_logs=state["algo_logs"],
        algo_stats=state["algo_stats"],
        coords=coords,
        split_map=state["split_map"],
        map_left_html=state["map_left_html"],
        map_right_html=state["map_right_html"],
        selected_algorithm=state["selected_algorithm"],
        selected_start=state["selected_start"],
        selected_goal=state["selected_goal"],
        show_heuristic=state["show_heuristic"],
        graph_json=state["graph_json"],
        original_graph_json=state["original_graph_json"],
    )


@app.route("/map-panel", methods=["POST"])
def map_panel():
    """Renderiza el panel de mapas como respuesta parcial.

    Parametros:
        Ninguno.

    Retorna:
        str: HTML renderizado del panel de mapa.
    """
    state = resolve_search_state(request)
    return render_template(
        "map_panel.html",
        split_map=state["split_map"],
        map_left_html=state["map_left_html"],
        map_right_html=state["map_right_html"],
    )

if __name__ == "__main__":
    app.run(debug=True)