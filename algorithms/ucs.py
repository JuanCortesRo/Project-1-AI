"""
algorithms/ucs.py

Descripción: Implementación del algoritmo de búsqueda de costo uniforme (UCS) para grafos.
Autor original: ANDRES MAURICIO VALENCIA RESTREPO
Modificado por: JUAN JOSÉ CORTÉS RODRÍGUEZ, CARLOS MANUEL VILLAMIL GRISALES, JUAN DAVID CHARRY MEDINA, LAURA VALENTINA ARBELAEZ LEUDO

Proyecto 1 - IA - Universidad del Valle, 2026
"""

def search(graph, start, goal):
    """Ejecuta busqueda de costo uniforme (UCS) 

    Parametros:
        graph (dict): Grafo ponderado representado como diccionario de adyacencia.
        start (str): Nodo de inicio.
        goal (str): Nodo objetivo.

    Retorna:
        dict: Estructura con ruta, costo, estadisticas y logs temporales de ejecucion.
    """
    dist = {start: 0}
    parent = {start: None}
    frontier = [(0, start)]  # (coste acumulado, nodo)

    logs = [
        "=== Inicio UCS ===",
        f"Nodo inicial: {start}",
        f"Nodo objetivo: {goal}",
    ]
    iteracion = 0
    nodos_expandidos = 0

    while frontier:
        iteracion += 1
        # seleccionar el nodo con menor costo acumulado
        frontier.sort(key=lambda x: x[0])  # ordena por costo
        cost, node = frontier.pop(0)       # saca el primero (menor costo)

        logs.append(f"\nIteracion {iteracion} - Extraccion")
        logs.append(f"Nodo actual: {node}")
        logs.append(f"Costo acumulado actual: {cost:.2f}")
        logs.append(f"Frontera actual: {frontier}")
        logs.append(f"Distancias conocidas: {dist}")

        # ignorar entradas viejas
        if cost > dist.get(node, float('inf')):
            logs.append("Entrada obsoleta descartada por costo mayor al mejor conocido.")
            continue

        nodos_expandidos += 1

        # Si llegamos al objetivo
        if node == goal:
            # reconstruir camino
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()

            logs.append("\n=== Fin UCS ===")
            logs.append(f"Camino encontrado: {' -> '.join(path)}")
            logs.append(f"Nodos expandidos: {nodos_expandidos}")
            logs.append(f"Nodos descubiertos: {len(dist)}")
            logs.append(f"Costo final de la ruta: {cost:.2f} km")

            return {
                "path": path,
                "cost": cost,
                "stats": {
                    "nodes_expanded": nodos_expandidos,
                    "nodes_discovered": len(dist),
                    "final_cost": cost,
                },
                "logs": logs,
            }

        # expandir vecinos
        for neighbor, weight in graph.get(node, {}).items(): # se adapto la iteracion de vecinos al grafo de nuestra app
            new_cost = cost + weight
            if new_cost < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_cost
                parent[neighbor] = node
                frontier.append((new_cost, neighbor))

        siguiente = frontier[0][1] if frontier else "Ninguno"
        logs.append(f"Siguiente nodo a visitar: {siguiente}")

    logs.append("\n=== Fin UCS ===")
    logs.append("Camino no encontrado.")
    logs.append(f"Nodos expandidos: {nodos_expandidos}")
    logs.append(f"Nodos descubiertos: {len(dist)}")
    logs.append("Costo final de la ruta: N/A")

    return {
        "path": None,
        "cost": None,
        "stats": {
            "nodes_expanded": nodos_expandidos,
            "nodes_discovered": len(dist),
            "final_cost": None,
        },
        "logs": logs,
    }
