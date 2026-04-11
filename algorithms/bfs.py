"""
algorithms/bfs.py

Descripción: Implementación del algoritmo de búsqueda en amplitud (BFS) para grafos.
Autor original: ANDRES MAURICIO VALENCIA RESTREPO
Modificado por: JUAN JOSÉ CORTÉS RODRÍGUEZ, CARLOS MANUEL VILLAMIL GRISALES, JUAN DAVID CHARRY MEDINA, LAURA VALENTINA ARBELAEZ LEUDO

Proyecto 1 - IA - Universidad del Valle, 2026
"""

from collections import deque

def search(graph, start, goal):
    """Ejecuta busqueda en amplitud (BFS)

    Parametros:
        graph (dict): Grafo ponderado representado como diccionario de adyacencia.
        start (str): Nodo de inicio.
        goal (str): Nodo objetivo.

    Retorna:
        dict: Estructura con ruta, costo, estadisticas y logs temporales de ejecucion.
    """
    # Cola FIFO: garantiza exploración por niveles (BFS)
    cola = deque([start])
    
    # Conjunto de nodos visitados para evitar ciclos
    visitados = {start}
    
    # Diccionario para reconstruir el camino recorrido
    predecesor = {start: None}

    logs = [
        "=== Inicio BFS ===",
        f"Nodo inicial: {start}",
        f"Nodo objetivo: {goal}",
    ]
    iteracion = 0
    nodos_expandidos = 0

    while cola:
        iteracion += 1

        # Extrae el nodo más antiguo (primero en entrar)
        nodo = cola.popleft()
        nodos_expandidos += 1

        logs.append(f"\nIteracion {iteracion} - Extraccion")
        logs.append(f"Nodo actual: {nodo}")
        logs.append(f"Cola actual: {list(cola)}")
        logs.append(f"Nodos visitados: {sorted(visitados)}")
        logs.append(f"Predecesores: {predecesor}")

        # Si se alcanza el objetivo, se reconstruye el camino
        if nodo == goal:
            camino = []
            while nodo is not None:
                camino.append(nodo)
                nodo = predecesor[nodo]  # retrocede al nodo anterior
            camino = list(reversed(camino))  # invierte para orden correcto

            # Calcula la distancia total recorrida sumando los pesos entre nodos consecutivos.
            distancia_total = 0
            for i in range(len(camino) - 1):
                origen = camino[i]
                destino = camino[i + 1]
                distancia_total += graph[origen][destino]

            logs.append("\n=== Fin BFS ===")
            logs.append(f"Camino encontrado: {' -> '.join(camino)}")
            logs.append(f"Nodos expandidos: {nodos_expandidos}")
            logs.append(f"Nodos descubiertos: {len(visitados)}")
            logs.append(f"Costo final de la ruta: {distancia_total:.2f} km")

            return {
                "path": camino,
                "cost": distancia_total,
                "stats": {
                    "nodes_expanded": nodos_expandidos,
                    "nodes_discovered": len(visitados),
                    "final_cost": distancia_total,
                },
                "logs": logs,
            }

        # Explora los vecinos del nodo actual (sin usar los pesos)
        for vecino in graph[nodo].keys():
            if vecino not in visitados:
                visitados.add(vecino)           # marca como visitado
                predecesor[vecino] = nodo       # guarda de dónde viene
                cola.append(vecino)            # lo agrega a la cola

        siguiente = cola[0] if cola else "Ninguno"
        logs.append(f"Siguiente nodo a visitar: {siguiente}")

    # Si no se encuentra camino entre inicio y objetivo
    logs.append("\n=== Fin BFS ===")
    logs.append("Camino no encontrado.")
    logs.append(f"Nodos expandidos: {nodos_expandidos}")
    logs.append(f"Nodos descubiertos: {len(visitados)}")
    logs.append("Costo final de la ruta: N/A")

    return {
        "path": None,
        "cost": None,
        "stats": {
            "nodes_expanded": nodos_expandidos,
            "nodes_discovered": len(visitados),
            "final_cost": None,
        },
        "logs": logs,
    }