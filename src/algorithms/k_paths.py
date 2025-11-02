"""
Clase para calcular los K caminos más cortos en un grafo ponderado.
Basado en el algoritmo de Dijkstra y de Yen para k = 1 , k = 2 , k = 3.



"""

import heapq
import copy
import numpy as np


class KPaths:
    """Clase que implementa el algoritmo de K caminos más cortos"""

    def __init__(self):
        self.matriz = None
        self.num_nodos = 0

    def compute(self, matriz, k=1):
        """
        Calcula la matriz de los k caminos más cortos entre todos los pares de nodos.
        Retorna una matriz donde cada posición [i][j] representa el costo del k-ésimo
        camino más corto entre el nodo i y el nodo j.
        """
        self.matriz = np.array(matriz)
        self.num_nodos = len(matriz)
        matriz_k = np.full((self.num_nodos, self.num_nodos), np.inf)

        for i in range(self.num_nodos):
            for j in range(self.num_nodos):
                if i != j:
                    caminos = self.find_k_shortest_paths(i, j, k)
                    if len(caminos) >= k:
                        matriz_k[i][j] = caminos[k - 1][0]
                    elif caminos:
                        matriz_k[i][j] = caminos[-1][0]

        return matriz_k.tolist()

    def dijkstra(self, origen):
        """
        Aplica el algoritmo de Dijkstra desde un nodo origen.
        Retorna las distancias mínimas a todos los demás nodos y los predecesores
        para poder reconstruir los caminos.
        """
        distancias = [np.inf] * self.num_nodos
        predecesores = [None] * self.num_nodos
        distancias[origen] = 0
        visitados = set()
        cola = [(0, origen)]

        while cola:
            dist, actual = heapq.heappop(cola)
            if actual in visitados:
                continue
            visitados.add(actual)

            for vecino in range(self.num_nodos):
                peso = self.matriz[actual][vecino]
                if peso > 0 and vecino not in visitados:
                    nueva_dist = dist + peso
                    if nueva_dist < distancias[vecino]:
                        distancias[vecino] = nueva_dist
                        predecesores[vecino] = actual
                        heapq.heappush(cola, (nueva_dist, vecino))

        return distancias, predecesores

    def reconstruir_camino(self, predecesores, destino):
        """
        Reconstruye el camino más corto usando la lista de predecesores
        obtenida con Dijkstra.
        """
        camino = []
        nodo = destino
        while nodo is not None:
            camino.append(nodo)
            nodo = predecesores[nodo]
        return list(reversed(camino))

    def find_k_shortest_paths(self, origen, destino, k=3):
        """
        Encuentra los K caminos más cortos entre dos nodos usando el algoritmo de Yen.
        El primer camino se obtiene con Dijkstra, y los siguientes se generan
        modificando temporalmente el grafo para encontrar rutas alternativas.
        """
        distancias, predecesores = self.dijkstra(origen)
        if np.isinf(distancias[destino]):
            return []

        primer_camino = self.reconstruir_camino(predecesores, destino)
        A = [(distancias[destino], primer_camino)]  # Caminos confirmados
        B = []  # Caminos candidatos

        for i in range(1, k):
            for j in range(len(A[i - 1][1]) - 1):
                spur_node = A[i - 1][1][j]
                root_path = A[i - 1][1][:j + 1]

                # Hacer una copia del grafo para modificar
                matriz_copia = copy.deepcopy(self.matriz)

                # Eliminar aristas que ya fueron usadas en caminos anteriores
                for costo, camino in A:
                    if len(camino) > j and camino[:j + 1] == root_path:
                        n1 = camino[j]
                        n2 = camino[j + 1]
                        matriz_copia[n1][n2] = 0

                # Eliminar nodos del camino raíz excepto el spur_node
                for nodo in root_path[:-1]:
                    for vecino in range(self.num_nodos):
                        matriz_copia[nodo][vecino] = 0
                        matriz_copia[vecino][nodo] = 0

                # Calcular el camino desde el spur_node al destino
                temp = KPaths()
                temp.matriz = matriz_copia
                temp.num_nodos = self.num_nodos
                dist_spur, pred_spur = temp.dijkstra(spur_node)

                if not np.isinf(dist_spur[destino]):
                    spur_path = temp.reconstruir_camino(pred_spur, destino)
                    total_path = root_path[:-1] + spur_path
                    total_cost = self.calcular_costo(total_path)
                    if (total_cost, total_path) not in B:
                        B.append((total_cost, total_path))

            if not B:
                break

            # Seleccionar el candidato más corto y agregarlo a la lista de caminos confirmados
            B.sort(key=lambda x: x[0])
            A.append(B[0])
            B.pop(0)

        return A

    def calcular_costo(self, camino):
        """
        Calcula el costo total de un camino sumando los pesos de las aristas
        que lo componen.
        """
        costo = 0
        for i in range(len(camino) - 1):
            a, b = camino[i], camino[i + 1]
            peso = self.matriz[a][b]
            if peso == 0:
                return np.inf
            costo += peso
        return costo
