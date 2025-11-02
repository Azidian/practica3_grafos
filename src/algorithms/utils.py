"""
Funciones utilitarias para algoritmos de grafos
"""


def print_matrix(matrix, title="Matriz"):
    """
    Imprime una matriz de forma legible
    
    Args:
        matrix: Matriz a imprimir
        title: Título de la matriz
    """
    print(f"\n{title}:")
    print("-" * 50)
    
    n = len(matrix)
    for i in range(n):
        row_str = " ".join([f"{val:6.1f}" if val != float('inf') else "   ∞  " 
                           for val in matrix[i]])
        print(f"Nodo {i}: [{row_str}]")
    print()


def validate_matrix(matrix):
    """
    Valida que una matriz sea válida para representar un grafo
    
    Args:
        matrix: Matriz a validar
        
    Returns:
        True si es válida, False en caso contrario
    """
    if not matrix:
        return False
        
    n = len(matrix)
    
    # Verificar que sea cuadrada
    for row in matrix:
        if len(row) != n:
            return False
            
    # Verificar que la diagonal sea cero
    for i in range(n):
        if matrix[i][i] != 0:
            return False
            
    # Verificar simetría (grafo no dirigido)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                return False
                
    return True


def generate_random_matrix(n, density=0.4, max_weight=15):
    """
    Genera una matriz de adyacencia aleatoria
    
    Args:
        n: Número de nodos
        density: Probabilidad de conexión entre nodos (0.0 a 1.0)
        max_weight: Peso máximo de las aristas
        
    Returns:
        Matriz de adyacencia aleatoria
    """
    import random
    
    matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < density:
                weight = random.randint(1, max_weight)
                matrix[i][j] = weight
                matrix[j][i] = weight
                
    return matrix
