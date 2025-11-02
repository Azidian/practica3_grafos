"""
Implementación de algoritmos de camino más corto
"""

import heapq


def dijkstra(matrix, start):
    """
    Algoritmo de Dijkstra para encontrar el camino más corto desde un nodo origen
    
    Args:
        matrix: Matriz de adyacencia del grafo
        start: Nodo de inicio
        
    Returns:
        distances: Lista de distancias mínimas desde start a cada nodo
        predecessors: Lista de predecesores para reconstruir caminos
    """
    n = len(matrix)
    distances = [float('inf')] * n
    predecessors = [-1] * n
    distances[start] = 0
    
    # Cola de prioridad: (distancia, nodo)
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if u in visited:
            continue
            
        visited.add(u)
        
        # Explorar vecinos
        for v in range(n):
            if matrix[u][v] > 0:  # Hay arista
                weight = matrix[u][v]
                distance = current_dist + weight
                
                if distance < distances[v]:
                    distances[v] = distance
                    predecessors[v] = u
                    heapq.heappush(pq, (distance, v))
                    
    return distances, predecessors


def reconstruct_path(predecessors, start, end):
    """
    Reconstruye el camino desde start hasta end usando los predecesores
    
    Args:
        predecessors: Lista de predecesores de Dijkstra
        start: Nodo inicial
        end: Nodo final
        
    Returns:
        Lista con el camino [start, ..., end] o None si no existe
    """
    if predecessors[end] == -1 and start != end:
        return None
        
    path = []
    current = end
    
    while current != -1:
        path.append(current)
        if current == start:
            break
        current = predecessors[current]
        
    path.reverse()
    return path if path[0] == start else None


def floyd_warshall(matrix):
    """
    Algoritmo de Floyd-Warshall para encontrar todos los caminos más cortos
    
    Args:
        matrix: Matriz de adyacencia del grafo
        
    Returns:
        dist: Matriz de distancias mínimas entre todos los pares de nodos
        next_node: Matriz para reconstruir caminos
    """
    n = len(matrix)
    
    # Inicializar matrices
    dist = [[float('inf')] * n for _ in range(n)]
    next_node = [[-1] * n for _ in range(n)]
    
    # Configuración inicial
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0
            elif matrix[i][j] > 0:
                dist[i][j] = matrix[i][j]
                next_node[i][j] = j
                
    # Algoritmo principal
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]
                    
    return dist, next_node
