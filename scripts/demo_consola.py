"""
Script de demostración en modo consola
Muestra ejemplos de uso del algoritmo sin interfaz gráfica
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from algorithms.k_paths import KPaths
from algorithms.utils import print_matrix, generate_random_matrix


def demo_basica():
    """Demostración básica del algoritmo"""
    print("\n" + "="*70)
    print(" DEMOSTRACIÓN BÁSICA - ALGORITMO K-CAMINOS ".center(70))
    print("="*70 + "\n")
    
    # Grafo de ejemplo
    matriz = [
        [0, 4, 2, 0, 0],
        [4, 0, 1, 5, 0],
        [2, 1, 0, 8, 10],
        [0, 5, 8, 0, 2],
        [0, 0, 10, 2, 0]
    ]
    
    print("Grafo de Ejemplo:")
    print_matrix(matriz, "Matriz de Adyacencia")
    
    kpaths = KPaths()
    
    # Calcular para k=1, k=2, k=3
    print("\n" + "="*70)
    print(" CÁLCULO DE MATRICES K-CAMINOS ".center(70))
    print("="*70)
    
    for k in [1, 2, 3]:
        print(f"\n{'─'*70}")
        print(f" K = {k} ".center(70, '─'))
        print(f"{'─'*70}")
        
        matriz_k = kpaths.compute(matriz, k)
        print_matrix(matriz_k, f"Matriz de {k}-Caminos")
        
    # Buscar caminos específicos
    print("\n" + "="*70)
    print(" BÚSQUEDA DE CAMINOS ESPECÍFICOS ".center(70))
    print("="*70 + "\n")
    
    origen, destino = 0, 4
    print(f"Buscando los 3 caminos más cortos de Nodo {origen} a Nodo {destino}:\n")
    
    caminos = kpaths.find_k_shortest_paths(origen, destino, 3)
    
    if caminos:
        for idx, (costo, camino) in enumerate(caminos, 1):
            camino_str = " → ".join([f"N{n}" for n in camino])
            print(f"  Camino #{idx}:")
            print(f"    Ruta: {camino_str}")
            print(f"    Costo: {costo}")
            print()
    else:
        print(f"  No hay caminos disponibles de N{origen} a N{destino}\n")


def demo_grafo_aleatorio():
    """Demostración con grafo aleatorio"""
    print("\n" + "="*70)
    print(" DEMOSTRACIÓN CON GRAFO ALEATORIO ".center(70))
    print("="*70 + "\n")
    
    # Generar grafo aleatorio
    n = 6
    matriz = generate_random_matrix(n, density=0.4, max_weight=15)
    
    print(f"Grafo Aleatorio de {n} nodos (40% conectividad):")
    print_matrix(matriz, "Matriz de Adyacencia")
    
    kpaths = KPaths()
    
    # Calcular solo para k=2
    print("\n" + "="*70)
    matriz_k2 = kpaths.compute(matriz, 2)
    print_matrix(matriz_k2, "Matriz de 2-Caminos")


def demo_comparacion():
    """Demostración comparando k=1, k=2, k=3 para un par de nodos"""
    print("\n" + "="*70)
    print(" COMPARACIÓN DE K-CAMINOS PARA UN PAR DE NODOS ".center(70))
    print("="*70 + "\n")
    
    matriz = [
        [0, 2, 4, 0, 0, 0],
        [2, 0, 1, 4, 0, 0],
        [4, 1, 0, 1, 5, 0],
        [0, 4, 1, 0, 1, 3],
        [0, 0, 5, 1, 0, 2],
        [0, 0, 0, 3, 2, 0]
    ]
    
    print("Grafo:")
    print_matrix(matriz, "Matriz de Adyacencia")
    
    kpaths = KPaths()
    
    origen, destino = 0, 5
    print(f"\nAnálisis de caminos de Nodo {origen} a Nodo {destino}:")
    print("="*70 + "\n")
    
    for k in [1, 2, 3]:
        print(f"K = {k}:")
        caminos = kpaths.find_k_shortest_paths(origen, destino, k)
        
        if len(caminos) >= k:
            costo, camino = caminos[k-1]
            camino_str = " → ".join([f"N{n}" for n in camino])
            print(f"  {k}° camino más corto: {camino_str}")
            print(f"  Costo: {costo}")
        else:
            print(f"  No existe un {k}° camino")
        print()


def menu_principal():
    """Menú interactivo para las demostraciones"""
    while True:
        print("\n" + "="*70)
        print(" MENÚ DE DEMOSTRACIONES ".center(70))
        print("="*70)
        print("\n1. Demostración Básica")
        print("2. Grafo Aleatorio")
        print("3. Comparación de K-Caminos")
        print("4. Ejecutar Todas las Demos")
        print("5. Salir")
        print("\n" + "="*70)
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            demo_basica()
        elif opcion == "2":
            demo_grafo_aleatorio()
        elif opcion == "3":
            demo_comparacion()
        elif opcion == "4":
            demo_basica()
            demo_grafo_aleatorio()
            demo_comparacion()
        elif opcion == "5":
            print("\n¡Hasta luego!\n")
            break
        else:
            print("\n❌ Opción inválida. Intenta de nuevo.")
        
        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        # Modo automático: ejecutar todas las demos
        demo_basica()
        demo_grafo_aleatorio()
        demo_comparacion()
    else:
        # Modo interactivo: mostrar menú
        menu_principal()
