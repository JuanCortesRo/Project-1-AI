from flask import Flask, render_template, request
import importlib
from graph import graph, coords, get_map_html

app = Flask(__name__)

ALGORITHMS = {
    "BFS": "bfs",
    "DFS": "dfs",
    "UCS" : "ucs",
    "A*" : "astar",
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    path = []
    cost = None
    error = None
    if request.method == "POST":
        algo_key = request.form["algorithm"]
        start = request.form["start"]
        goal = request.form["goal"]
        try:
            algo_module = importlib.import_module(f"algorithms.{ALGORITHMS[algo_key]}")
            path = algo_module.search(graph, start, goal)
            result = algo_module.search(graph, start, goal)
            if isinstance(result, tuple):
                path, cost = result
            else:
                path = result
                cost = None
            if path is None:
                error = "Algoritmo no implementado o no se encontró camino."
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
        map_html=get_map_html(path)
    )

if __name__ == "__main__":
    app.run(debug=True)