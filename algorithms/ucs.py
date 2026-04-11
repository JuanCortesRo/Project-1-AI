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
        tuple[list[str] | None, float | None]: Ruta y costo total acumulado,
        o (None, None) si no existe camino.
    """
    dist = {start: 0}
    parent = {start: None}
    frontier = [(0, start)]  # (coste acumulado, nodo)
    while frontier:
        # seleccionar el nodo con menor costo acumulado
        frontier.sort(key=lambda x: x[0])  # ordena por costo
        cost, node = frontier.pop(0)       # saca el primero (menor costo)
        # ignorar entradas viejas
        if cost > dist.get(node, float('inf')):
            continue
        # Si llegamos al objetivo
        if node == goal:
            # reconstruir camino
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path, cost
        # expandir vecinos
        for neighbor, weight in graph.get(node, {}).items(): # se adapto la iteracion de vecinos al grafo de nuestra app
            new_cost = cost + weight
            if new_cost < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_cost
                parent[neighbor] = node
                frontier.append((new_cost, neighbor))
    return None, None
