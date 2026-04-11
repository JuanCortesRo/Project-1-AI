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
    """Construye h(n) como distancia Haversine desde cada ciudad hasta la meta."""
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
    path = []
    cost = None
    error = None
    show_heuristic = False

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
            if isinstance(result, tuple):
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
    return "OK", 200

@app.route("/", methods=["GET", "POST"])
def index():
    state = resolve_search_state(request)

    return render_template(
        "index.html",
        algorithms=ALGORITHMS.keys(),
        nodes=[node for node in state["custom_graph"].keys() if node != "heuristic"],
        path=state["path"],
        cost=state["cost"],
        error=state["error"],
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
    state = resolve_search_state(request)
    return render_template(
        "map_panel.html",
        split_map=state["split_map"],
        map_left_html=state["map_left_html"],
        map_right_html=state["map_right_html"],
    )

if __name__ == "__main__":
    app.run(debug=True)