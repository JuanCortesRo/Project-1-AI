"""
algorithms/dfs.py

Descripción: Implementación del algoritmo de búsqueda en profundidad (DFS) para grafos.
Autor original: ANDRES MAURICIO VALENCIA RESTREPO
Modificado por: JUAN JOSÉ CORTÉS RODRÍGUEZ, CARLOS MANUEL VILLAMIL GRISALES, JUAN DAVID CHARRY MEDINA, LAURA VALENTINA ARBELAEZ LEUDO

Proyecto 1 - IA - Universidad del Valle, 2026
"""

def search(graph, start, goal):
    pila = [start]              # pila para DFS
    visitados = set()            # conjunto de nodos visitados
    predecesores = {start: None}  # diccionario de predecesores
    
    while pila:
        nodo = pila.pop()  # se saca el último
        if nodo not in visitados:
            visitados.add(nodo)
            # Si llegamos al objetivo, reconstruimos el camino
            if nodo == goal:
                camino = []
                actual = nodo
                while actual is not None:
                    camino.append(actual)
                    actual = predecesores[actual]
                camino.reverse()
                # return camino, visitados, predecesores
                return camino
            # Agregar vecinos a la pila
            vecinos = graph[nodo]
            for vecino in reversed(vecinos):  # invertir orden
                if vecino not in predecesores:
                    predecesores[vecino] = nodo
                    pila.append(vecino)
    return None