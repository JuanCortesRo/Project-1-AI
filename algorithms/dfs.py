"""
algorithms/dfs.py

Descripción: Implementación del algoritmo de búsqueda en profundidad (DFS) para grafos.
Autor original: ANDRES MAURICIO VALENCIA RESTREPO
Modificado por: JUAN JOSÉ CORTÉS RODRÍGUEZ, CARLOS MANUEL VILLAMIL GRISALES, JUAN DAVID CHARRY MEDINA, LAURA VALENTINA ARBELAEZ LEUDO

Proyecto 1 - IA - Universidad del Valle, 2026
"""

def search(graph, start, goal):
    """Ejecuta busqueda en profundidad (DFS)

    Parametros:
        graph (dict): Grafo ponderado representado como diccionario de adyacencia.
        start (str): Nodo de inicio.
        goal (str): Nodo objetivo.

    Retorna:
        dict: Estructura con ruta, costo, estadisticas y logs temporales de ejecucion.
    """
    pila = [start]               # pila para DFS
    visitados = set()            # conjunto de nodos visitados
    predecesores = {start: None} # diccionario de predecesores

    logs = [
        "=== Inicio DFS ===",
        f"Nodo inicial: {start}",
        f"Nodo objetivo: {goal}",
    ]
    iteracion = 0
    nodos_expandidos = 0

    while pila:
        iteracion += 1
        nodo = pila.pop()  # se saca el último

        logs.append(f"\nIteracion {iteracion} - Extraccion")
        logs.append(f"Nodo actual: {nodo}")
        logs.append(f"Pila actual: {list(pila)}")
        logs.append(f"Nodos visitados: {sorted(visitados)}")
        logs.append(f"Predecesores: {predecesores}")

        if nodo not in visitados:
            visitados.add(nodo)
            nodos_expandidos += 1

            # Si llegamos al objetivo, reconstruimos el camino
            if nodo == goal:
                camino = []
                actual = nodo
                while actual is not None:
                    camino.append(actual)
                    actual = predecesores[actual]
                camino.reverse()

                # Calcula la distancia total recorrida sumando los pesos entre nodos consecutivos.
                distancia_total = 0
                for i in range(len(camino) - 1):
                    origen = camino[i]
                    destino = camino[i + 1]
                    distancia_total += graph[origen][destino]

                logs.append("\n=== Fin DFS ===")
                logs.append(f"Camino encontrado: {' -> '.join(camino)}")
                logs.append(f"Nodos expandidos: {nodos_expandidos}")
                logs.append(f"Nodos descubiertos: {len(predecesores)}")
                logs.append(f"Costo final de la ruta: {distancia_total:.2f} km")

                return {
                    "path": camino,
                    "cost": distancia_total,
                    "stats": {
                        "nodes_expanded": nodos_expandidos,
                        "nodes_discovered": len(predecesores),
                        "final_cost": distancia_total,
                    },
                    "logs": logs,
                }

            # Agregar vecinos a la pila
            vecinos = graph.get(nodo, {})
            for vecino in reversed(list(vecinos.keys())):  # invertir orden
                if vecino not in predecesores:
                    predecesores[vecino] = nodo
                    pila.append(vecino)

            siguiente = pila[-1] if pila else "Ninguno"
            logs.append(f"Siguiente nodo a visitar: {siguiente}")
        else:
            logs.append("Nodo ya visitado, se omite expansion.")

    logs.append("\n=== Fin DFS ===")
    logs.append("Camino no encontrado.")
    logs.append(f"Nodos expandidos: {nodos_expandidos}")
    logs.append(f"Nodos descubiertos: {len(predecesores)}")
    logs.append("Costo final de la ruta: N/A")

    return {
        "path": None,
        "cost": None,
        "stats": {
            "nodes_expanded": nodos_expandidos,
            "nodes_discovered": len(predecesores),
            "final_cost": None,
        },
        "logs": logs,
    }