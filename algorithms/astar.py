"""
algorithms/astar.py

Descripción: Implementación del algoritmo de búsqueda informada A estrella (A*) para grafos.
Autor original: ANDRES MAURICIO VALENCIA RESTREPO
Modificado por: JUAN JOSÉ CORTÉS RODRÍGUEZ, CARLOS MANUEL VILLAMIL GRISALES, JUAN DAVID CHARRY MEDINA, LAURA VALENTINA ARBELAEZ LEUDO

Proyecto 1 - IA - Universidad del Valle, 2026
"""

def search(graph, start, goal):
    """Ejecuta busqueda A* 

    Parametros:
        graph (dict): Grafo ponderado con clave opcional 'heuristic'.
        start (str): Nodo de inicio.
        goal (str): Nodo objetivo.

    Retorna:
        dict: Estructura con ruta, costo, estadisticas y logs temporales de ejecucion.
    """
    import heapq

    # Saca la heurística del grafo (si no existe, toma 0 por defecto)
    heuristic = graph.get('heuristic', {})

    # Guardar el costo acumulado desde el nodo inicial (g(n))
    dist = {start: 0}

    # Este lo utiliza para poder reconstruir el camino al final
    parent = {start: None}

    # La frontera funciona como una cola de prioridad (heap)
    # Guarda tuplas de la forma: (f(n), g(n), nodo)
    frontier = []
    heapq.heappush(frontier, (heuristic.get(start, 0), 0, start))

    logs = [
        "=== Inicio A* ===",
        f"Nodo inicial: {start}",
        f"Nodo objetivo: {goal}",
    ]
    iteracion = 0
    nodos_expandidos = 0

    while frontier:
        iteracion += 1
        # Se extrae el nodo con menor f(n)
        f_cost, g_cost, node = heapq.heappop(frontier)

        logs.append(f"\nIteracion {iteracion} - Extraccion")
        logs.append(f"Nodo actual: {node}")
        logs.append(f"f(n) actual: {f_cost:.2f}")
        logs.append(f"g(n) actual: {g_cost:.2f}")
        logs.append(f"Distancias conocidas: {dist}")
        logs.append(f"Frontera actual: {frontier}")

        # Si este nodo ya tiene un mejor costo registrado, se ignora
        # (esto evita procesar caminos peores, igual que en UCS)
        if g_cost > dist.get(node, float('inf')):
            logs.append("Entrada obsoleta descartada por costo mayor al mejor conocido.")
            continue

        nodos_expandidos += 1

        # Si se llega al objetivo, reconstruye el camino
        if node == goal:
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()

            logs.append("\n=== Fin A* ===")
            logs.append(f"Camino encontrado: {' -> '.join(path)}")
            logs.append(f"Nodos expandidos: {nodos_expandidos}")
            logs.append(f"Nodos descubiertos: {len(dist)}")
            logs.append(f"Costo final de la ruta: {dist[goal]:.2f} km")

            return {
                "path": path,
                "cost": dist[goal],
                "stats": {
                    "nodes_expanded": nodos_expandidos,
                    "nodes_discovered": len(dist),
                    "final_cost": dist[goal],
                },
                "logs": logs,
            }

        # Recorre los vecinos del nodo actual
        for neighbor, weight in graph.get(node, {}).items():

            # Se ignora la clave 'heuristic' para no tomarla como un nodo
            if neighbor == 'heuristic':
                continue

            # Calculo del nuevo costo acumulado (g(n))
            new_cost = dist[node] + weight

            # Si se encuentra un camino mejor hacia ese vecino, se actualiza todo
            if new_cost < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_cost
                parent[neighbor] = node

                # fórmula de A*: f(n) = g(n) + h(n)
                f_neighbor = new_cost + heuristic.get(neighbor, 0)

                # Agregar el vecino a la frontera para seguir explorando
                heapq.heappush(frontier, (f_neighbor, new_cost, neighbor))

        siguiente = frontier[0][2] if frontier else "Ninguno"
        logs.append(f"Siguiente nodo a visitar: {siguiente}")

    logs.append("\n=== Fin A* ===")
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