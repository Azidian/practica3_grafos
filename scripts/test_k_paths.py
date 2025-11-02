"""
Script de prueba para verificar el funcionamiento del algoritmo K-Paths
Prueba la implementación modular con diferentes casos de grafos
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from algorithms.k_paths import KPaths
from algorithms.utils import print_matrix


def test_caso_1():
    """Test con grafo pequeño y completamente conectado"""
    print("\n" + "="*70)
    print(" TEST CASO 1: Grafo Pequeño Completamente Conectado ".center(70))
    print("="*70 + "\n")
    
    matriz = [
        [0, 1, 4, 0],
        [1, 0, 2, 5],
        [4, 2, 0, 1],
        [0, 5, 1, 0]
    ]
    
    kpaths = KPaths()
    
    print("Matriz Original:")
    print_matrix(matriz, "Matriz de Adyacencia")
    
    for k in [1, 2, 3]:
        print(f"\n{'='*70}")
        matriz_k = kpaths.compute(matriz, k)
        print_matrix(matriz_k, f"Matriz K={k}")
    
    print("\n✓ Test Caso 1 completado")


def test_caso_2():
    """Test con grafo parcialmente conectado"""
    print("\n" + "="*70)
    print(" TEST CASO 2: Grafo Parcialmente Conectado ".center(70))
    print("="*70 + "\n")
    
    matriz = [
        [0, 3, 0, 0, 0],
        [3, 0, 2, 0, 0],
        [0, 2, 0, 4, 1],
        [0, 0, 4, 0, 5],
        [0, 0, 1, 5, 0]
    ]
    
    kpaths = KPaths()
    
    print("Matriz Original:")
    print_matrix(matriz, "Matriz de Adyacencia")
    
    for k in [1, 2, 3]:
        print(f"\n{'='*70}")
        matriz_k = kpaths.compute(matriz, k)
        print_matrix(matriz_k, f"Matriz K={k}")
    
    # Probar caminos específicos
    print("\n" + "="*70)
    print("Caminos específicos de Nodo 0 a Nodo 4:")
    print("-"*70)
    
    caminos = kpaths.find_k_shortest_paths(0, 4, 3)
    
    for idx, (costo, camino) in enumerate(caminos, 1):
        camino_str = " → ".join([f"N{n}" for n in camino])
        print(f"  Camino #{idx}: {camino_str} (Costo: {costo})")
    
    print("\n✓ Test Caso 2 completado")


def test_caso_3():
    """Test con grafo más grande"""
    print("\n" + "="*70)
    print(" TEST CASO 3: Grafo Grande (6 nodos) ".center(70))
    print("="*70 + "\n")
    
    matriz = [
        [0, 7, 9, 0, 0, 14],
        [7, 0, 10, 15, 0, 0],
        [9, 10, 0, 11, 0, 2],
        [0, 15, 11, 0, 6, 0],
        [0, 0, 0, 6, 0, 9],
        [14, 0, 2, 0, 9, 0]
    ]
    
    kpaths = KPaths()
    
    print("Matriz Original:")
    print_matrix(matriz, "Matriz de Adyacencia")
    
    for k in [1, 2, 3]:
        print(f"\n{'='*70}")
        matriz_k = kpaths.compute(matriz, k)
        print_matrix(matriz_k, f"Matriz K={k}")
    
    print("\n✓ Test Caso 3 completado")


def test_caso_4():
    """Test con el grafo del ejemplo de la práctica"""
    print("\n" + "="*70)
    print(" TEST CASO 4: Grafo del Ejemplo de la Práctica ".center(70))
    print("="*70 + "\n")
    
    matriz = [
        [0, 4, 2, 0, 0],
        [4, 0, 1, 5, 0],
        [2, 1, 0, 8, 10],
        [0, 5, 8, 0, 2],
        [0, 0, 10, 2, 0]
    ]
    
    kpaths = KPaths()
    
    print("Matriz Original:")
    print_matrix(matriz, "Matriz de Adyacencia")
    
    for k in [1, 2, 3]:
        print(f"\n{'='*70}")
        matriz_k = kpaths.compute(matriz, k)
        print_matrix(matriz_k, f"Matriz K={k}")
    
    # Ejemplo de caminos específicos
    print("\n" + "="*70)
    print("Ejemplo: 3 caminos más cortos de Nodo 0 a Nodo 4:")
    print("-"*70)
    
    caminos = kpaths.find_k_shortest_paths(0, 4, 3)
    
    for idx, (costo, camino) in enumerate(caminos, 1):
        camino_str = " → ".join([f"N{n}" for n in camino])
        print(f"  Camino #{idx}: {camino_str} (Costo: {costo})")
    
    print("\n✓ Test Caso 4 completado")


def ejecutar_todos_los_tests():
    """Ejecuta todos los tests"""
    print("\n" + "="*70)
    print(" SUITE DE PRUEBAS - ALGORITMO K-CAMINOS ".center(70))
    print(" Implementación Modular con PyQt5 ".center(70))
    print("="*70)
    
    try:
        test_caso_1()
        test_caso_2()
        test_caso_3()
        test_caso_4()
        
        print("\n" + "="*70)
        print(" ✓ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE ".center(70))
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error durante los tests: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    ejecutar_todos_los_tests()
