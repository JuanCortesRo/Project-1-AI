"""
algorithms/astar.py

Descripción: Implementación del algoritmo de búsqueda informada A estrella (A*) para grafos.
Autor original: ANDRES MAURICIO VALENCIA RESTREPO
Modificado por: JUAN JOSÉ CORTÉS RODRÍGUEZ, CARLOS MANUEL VILLAMIL GRISALES, JUAN DAVID CHARRY MEDINA, LAURA VALENTINA ARBELAEZ LEUDO

Proyecto 1 - IA - Universidad del Valle, 2026
"""

def search(graph, start, goal):
    import heapq

    # Aquí saco la heurística del grafo (si no existe, toma 0 por defecto)
    heuristic = graph.get('heuristic', {})

    # Este diccionario guarda el costo acumulado desde el nodo inicial (g(n))
    dist = {start: 0}

    # Este lo uso para poder reconstruir el camino al final
    parent = {start: None}

    # La frontera funciona como una cola de prioridad (heap)
    # Guarda tuplas de la forma: (f(n), g(n), nodo)
    frontier = []
    heapq.heappush(frontier, (heuristic.get(start, 0), 0, start))

    while frontier:
        # Saco el nodo con menor f(n)
        f_cost, g_cost, node = heapq.heappop(frontier)

        # Si este nodo ya tiene un mejor costo registrado, lo ignoro
        # (esto evita procesar caminos peores, igual que en UCS)
        if g_cost > dist.get(node, float('inf')):
            continue

        # Si llegué al objetivo, reconstruyo el camino
        if node == goal:
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path, dist[goal]

        # Recorro los vecinos del nodo actual
        for neighbor, weight in graph.get(node, {}).items():

            # Evito que la clave 'heuristic' interfiera como si fuera un nodo
            if neighbor == 'heuristic':
                continue

            # Calculo el nuevo costo acumulado (g(n))
            new_cost = dist[node] + weight

            # Si encontré un camino mejor hacia ese vecino, actualizo todo
            if new_cost < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_cost
                parent[neighbor] = node

                # Aquí aplico la fórmula de A*: f(n) = g(n) + h(n)
                f_neighbor = new_cost + heuristic.get(neighbor, 0)

                # Agrego el vecino a la frontera para seguir explorando
                heapq.heappush(frontier, (f_neighbor, new_cost, neighbor))

    # Si no se encontró ningún camino
        # Implementa algoritmo A*