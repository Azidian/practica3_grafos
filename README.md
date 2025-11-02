# Algoritmo de K-Caminos Más Cortos

## Autores

**WENDY VANESSA ATEHORTUA CHAVERRA**
**ISABELLA CADAVID POSADA**
**ANA SOFÍA ANGARITA**

---

## Descripción

Implementación del **algoritmo de K-Caminos Más Cortos** con interfaz gráfica en **PyQt5**. Este proyecto permite visualizar grafos ponderados y calcular los *k caminos más cortos* entre nodos utilizando una variante del algoritmo de **Dijkstra**.

---

## Características

* **Interfaz Gráfica Intuitiva:** Visualización interactiva de grafos con nodos y aristas.
* **Generación de Grafos:** Crear grafos aleatorios o definir matriz de adyacencia manualmente.
* **Cálculo de K-Caminos:** Encuentra los k caminos más cortos *(k=1, 2, 3)* entre todos los pares de nodos.
* **Nodos Movibles:** Los nodos pueden arrastrarse para mejor visualización.
* **Matrices Dinámicas:** Ajusta el tamaño del grafo *(3–10 nodos)*.

---

## Instalación

### Requisitos Previos

* Python **3.12.11 o superior**
* **pip** (gestor de paquetes de Python)

### Dependencias

```bash
pip install PyQt5 numpy
```

O usando el archivo **requirements.txt**:

```bash
pip install -r requirements.txt
```

**Contenido de requirements.txt:**

```text
PyQt5>=5.15.0
numpy>=1.19.0
```

---

## Estructura del Proyecto

```text
k-paths-algorithm/
│
├── src/
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── k_paths.py
|   |   ├── shortest_path.py          
│   │   └── utils.py          # Funciones auxiliares
│   │
|   ├── grafo_visual.py
│   ├── graph.py                # Clases de visualización del grafo
│   ├── ui.py                   # Interfaz gráfica principal
│   └── main.py                 # Punto de entrada
│
├── scripts/
│   ├── demo_consola.py         # Demostraciones en consola
│   └── test_k_paths.py         # Casos de pruebas
│          
└── README.md
```

---

## Uso

### Ejecutar la Aplicación Principal

```bash
python main.py
```

### Ejecutar Tests

```bash
python examples/test_k_paths.py
```

---

## Guía de Usuario

### 1. Configuración del Grafo

#### Opción A: Generar Grafo Aleatorio

1. Selecciona el número de nodos *(3–10)*.
2. Click en **"Generar Matriz Aleatoria"**.
3. Click en **"Dibujar Grafo"**.

#### Opción B: Definir Manualmente

1. Selecciona el tamaño de la matriz.
2. Ingresa los pesos en la tabla *(0 = sin conexión)*.
3. Click en **"Dibujar Grafo"**.

### 2. Calcular K-Caminos

#### Calcular Matriz Completa

* Selecciona el valor de *k* (1, 2 o 3).
* Click en **"Calcular Matriz K-Paths"**.
* Revisa la matriz resultado en el panel de resultados.

### 3. Interacción con el Grafo

* **Mover Nodos:** Arrastra los nodos para reorganizar la visualización.

---

## Ejemplos de Uso

### Matriz de Adyacencia (pesos)

```text
    A  B  C  D
A [ 0  2  4  ∞ ]
B [ 2  0  1  5 ]
C [ 4  1  0  3 ]
D [ ∞  5  3  0 ]
```

### Grafo Visual

```text
  A ---2--- B
  |          |    |
  4      1      5
  |    |          |
  C ---3--- D
```

### Algoritmo para K=1

```text
    A  B  C  D
A [ 0  2  3  6 ]
B [ 2  0  1  4 ]
C [ 3  1  0  3 ]
D [ 6  4  3  0 ]
```

### Algoritmo para K=2 (Segundo camino más corto)

```text
    A  B  C  D
A [ ∞  4  4  7 ]
B [ 4  ∞  2  5 ]
C [ 4  2  ∞  4 ]
D [ 7  5  4  ∞ ]
```

---

## Algoritmo

### Funcionamiento

El algoritmo implementa una **variante de Dijkstra** que permite encontrar no solo el camino más corto, sino los *k caminos más cortos* entre dos nodos.

---

## Solución de Problemas

### Error: `No module named 'PyQt5'`

```bash
pip install PyQt5
```

---

### Manejo de Infinito

El programa usa `np.inf` de **NumPy** para representar distancias infinitas *(nodos no conectados)*. En la visualización se muestra como **“∞”**.

---

## Video sustentación
