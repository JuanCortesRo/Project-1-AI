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

    if request.method == "POST":
        selected_algorithm = request.form["algorithm"]
        selected_start = request.form["start"]
        selected_goal = request.form["goal"]

        try:
            algo_module = importlib.import_module(
                f"algorithms.{ALGORITHMS[selected_algorithm]}"
            )

            result = algo_module.search(graph, selected_start, selected_goal)

            if isinstance(result, tuple):
                path, cost = result
            else:
                path = result

            if path is None:
                error = "No se encontró camino entre los nodos seleccionados."

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        algorithms=ALGORITHMS.keys(),
        nodes=graph.keys(),
        path=path,
        cost=cost,
        error=error,
        coords=coords,
        map_html=get_map_html(path, selected_algorithm),  # 🔥 clave
        selected_algorithm=selected_algorithm,
        selected_start=selected_start,
        selected_goal=selected_goal
    )

if __name__ == "__main__":
    app.run(debug=True)