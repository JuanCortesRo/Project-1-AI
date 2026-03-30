from flask import Flask, render_template, request
import importlib
from graph import graph, coords, get_map_html

app = Flask(__name__)

ALGORITHMS = {
    "BFS": "bfs",
    "DFS": "dfs",
    "UCS": "ucs",
    "A*": "astar",
}

@app.route("/", methods=["GET", "POST"])
def index():
    path = []
    cost = None
    error = None

    selected_algorithm = "BFS"
    selected_start = "Cali"
    selected_goal = "Buga"


    import json
    # Generar el JSON original del archivo graph.py
    from graph import graph as default_graph
    original_graph_json = json.dumps(default_graph, indent=4, ensure_ascii=False)
    
    # graph_json será lo que se muestre en el textarea (el estado actual)
    graph_json = json.dumps(graph, indent=4, ensure_ascii=False)
    custom_graph = graph
    if request.method == "POST":
        selected_algorithm = request.form["algorithm"]
        selected_start = request.form["start"]
        selected_goal = request.form["goal"]
        graph_input = request.form.get("graphInput")
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
            result = algo_module.search(custom_graph, selected_start, selected_goal)
            if isinstance(result, tuple):
                path, cost = result
            else:
                path = result
            if path is None and not error:
                error = "No se encontró camino entre los nodos seleccionados."
        except Exception as e:
            if not error:
                error = str(e)

    return render_template(
        "index.html",
        algorithms=ALGORITHMS.keys(),
        nodes=custom_graph.keys(),
        path=path,
        cost=cost,
        error=error,
        coords=coords,
        map_html=get_map_html(path, selected_algorithm, graph=custom_graph),
        selected_algorithm=selected_algorithm,
        selected_start=selected_start,
        selected_goal=selected_goal,
        graph_json=graph_json,
        original_graph_json=original_graph_json
    )

if __name__ == "__main__":
    app.run(debug=True)
