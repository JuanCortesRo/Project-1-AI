"""
algorithms/bfs.py

Descripción: Implementación del algoritmo de búsqueda en amplitud (BFS) para grafos.
Autor original: ANDRES MAURICIO VALENCIA RESTREPO
Modificado por: JUAN JOSÉ CORTÉS RODRÍGUEZ, CARLOS MANUEL VILLAMIL GRISALES, JUAN DAVID CHARRY MEDINA, LAURA VALENTINA ARBELAEZ LEUDO

Proyecto 1 - IA - Universidad del Valle, 2026
"""

from collections import deque

def search(graph, start, goal):
    # Cola FIFO: garantiza exploración por niveles (BFS)
    cola = deque([start])
    
    # Conjunto de nodos visitados para evitar ciclos
    visitados = {start}
    
    # Diccionario para reconstruir el camino recorrido
    predecesor = {start: None}

    while cola:
        # Extrae el nodo más antiguo (primero en entrar)
        nodo = cola.popleft()

        # Si se alcanza el objetivo, se reconstruye el camino
        if nodo == goal:
            camino = []
            while nodo is not None:
                camino.append(nodo)
                nodo = predecesor[nodo]  # retrocede al nodo anterior
            return list(reversed(camino))  # invierte para orden correcto

        # Explora los vecinos del nodo actual (sin usar los pesos)
        for vecino in graph[nodo].keys():
            if vecino not in visitados:
                visitados.add(vecino)           # marca como visitado
                predecesor[vecino] = nodo       # guarda de dónde viene
                cola.append(vecino)            # lo agrega a la cola

    # Si no se encuentra camino entre inicio y objetivo
    return None