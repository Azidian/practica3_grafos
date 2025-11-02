"""
Interfaz gráfica para visualizar grafos y calcular k-caminos
Basado en el código original de Alexander Narváez
"""

import sys
import random
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsTextItem, QGraphicsItem, QMainWindow, QVBoxLayout,
    QHBoxLayout, QPushButton, QTableWidget, QWidget, QLabel,
    QSpinBox, QComboBox, QTextEdit, QGroupBox
)
from algorithms.k_paths import KPaths


class Nodo(QGraphicsEllipseItem):
    """Representa un nodo visual en el grafo"""

    def __init__(self, x, y, radius, id, app):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)
        self.setBrush(QtGui.QBrush(QtGui.QColor("#4A90E2")))
        self.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        self.id = id
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges)
        self.text_item = QGraphicsTextItem(str(self.id), self)
        self.text_item.setDefaultTextColor(QtCore.Qt.white)
        font = QtGui.QFont("Arial", 10, QtGui.QFont.Bold)
        self.text_item.setFont(font)
        text_rect = self.text_item.boundingRect()
        self.text_item.setPos(-text_rect.width() / 2, -text_rect.height() / 2)
        self.app = app
        self.aristas = []

    def agregar_arista(self, arista):
        self.aristas.append(arista)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for arista in self.aristas:
                arista.actualizar_posiciones()
        return super().itemChange(change, value)

    def resaltar(self, color="#E74C3C"):
        """Resalta el nodo con un color específico"""
        self.setBrush(QtGui.QBrush(QtGui.QColor(color)))
        self.setPen(QtGui.QPen(QtCore.Qt.red, 3))

    def restaurar(self):
        """Restaura el color original del nodo"""
        self.setBrush(QtGui.QBrush(QtGui.QColor("#4A90E2")))
        self.setPen(QtGui.QPen(QtCore.Qt.black, 2))


class Arista(QGraphicsLineItem):
    """Representa una arista visual en el grafo"""

    def __init__(self, nodo1, nodo2, peso, scene):
        super().__init__()
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.peso = peso
        self.scene = scene
        self.text_item = QGraphicsTextItem(str(self.peso))
        self.text_item.setDefaultTextColor(QtCore.Qt.blue)
        font = QtGui.QFont("Arial", 9, QtGui.QFont.Bold)
        self.text_item.setFont(font)
        self.scene.addItem(self.text_item)
        self.actualizar_posiciones()
        self.setFlag(QGraphicsLineItem.ItemIsSelectable)
        self.setPen(QtGui.QPen(QtCore.Qt.black, 2))

    def actualizar_posiciones(self):
        x1, y1 = self.nodo1.scenePos().x(), self.nodo1.scenePos().y()
        x2, y2 = self.nodo2.scenePos().x(), self.nodo2.scenePos().y()
        self.setLine(x1, y1, x2, y2)
        self.text_item.setPos((x1 + x2) / 2, (y1 + y2) / 2)

    def resaltar(self):
        self.setPen(QtGui.QPen(QtCore.Qt.red, 4))

    def restaurar(self):
        self.setPen(QtGui.QPen(QtCore.Qt.black, 2))

    def mousePressEvent(self, event):
        self.resaltar()
        self.nodo1.resaltar()
        self.nodo2.resaltar()
        super().mousePressEvent(event)


class GrafoApp(QMainWindow):
    """Aplicación principal para visualizar grafos y calcular k-caminos"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Algoritmo de K-Caminos Más Cortos")
        self.setGeometry(100, 100, 1400, 800)
        self.nodos = []
        self.aristas = []
        self.kpaths = KPaths()
        self.matrix = []
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        left_panel = self.crear_panel_controles()
        main_layout.addWidget(left_panel, 1)
        right_panel = self.crear_panel_grafo()
        main_layout.addWidget(right_panel, 2)
        central_widget.setLayout(main_layout)

    def crear_panel_controles(self):
        panel = QWidget()
        layout = QVBoxLayout()
        titulo = QLabel("Control de Grafos")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(titulo)

        grupo_matriz = QGroupBox("Matriz de Adyacencia")
        layout_matriz = QVBoxLayout()
        layout_tam = QHBoxLayout()
        layout_tam.addWidget(QLabel("Tamaño:"))
        self.spin_tamano = QSpinBox()
        self.spin_tamano.setRange(3, 10)
        self.spin_tamano.setValue(5)
        self.spin_tamano.valueChanged.connect(self.cambiar_tamano_matriz)
        layout_tam.addWidget(self.spin_tamano)
        layout_matriz.addLayout(layout_tam)

        self.tabla_matriz = QTableWidget(5, 5)
        layout_matriz.addWidget(self.tabla_matriz)
        btn_aleatorio = QPushButton("Generar Matriz Aleatoria")
        btn_aleatorio.clicked.connect(self.llenar_matriz_aleatoria)
        layout_matriz.addWidget(btn_aleatorio)
        btn_limpiar = QPushButton("Limpiar Matriz")
        btn_limpiar.clicked.connect(self.limpiar_matriz)
        layout_matriz.addWidget(btn_limpiar)
        grupo_matriz.setLayout(layout_matriz)
        layout.addWidget(grupo_matriz)

        grupo_visual = QGroupBox("Visualización")
        layout_visual = QVBoxLayout()
        btn_dibujar = QPushButton("Dibujar Grafo")
        btn_dibujar.setStyleSheet("background-color: #27AE60; color: white; font-weight: bold; padding: 10px;")
        btn_dibujar.clicked.connect(self.dibujar_grafo)
        layout_visual.addWidget(btn_dibujar)
        btn_restaurar = QPushButton("Restaurar Colores")
        btn_restaurar.clicked.connect(self.restaurar_colores)
        layout_visual.addWidget(btn_restaurar)
        grupo_visual.setLayout(layout_visual)
        layout.addWidget(grupo_visual)

        grupo_k = QGroupBox("Calcular K-Caminos")
        layout_k = QVBoxLayout()
        layout_k_sel = QHBoxLayout()
        layout_k_sel.addWidget(QLabel("Valor de k:"))
        self.combo_k = QComboBox()
        self.combo_k.addItems(["1", "2", "3"])
        self.combo_k.setCurrentText("2")
        layout_k_sel.addWidget(self.combo_k)
        layout_k.addLayout(layout_k_sel)
        btn_calcular = QPushButton("Calcular Matriz K-Paths")
        btn_calcular.setStyleSheet("background-color: #3498DB; color: white; font-weight: bold; padding: 10px;")
        btn_calcular.clicked.connect(self.calcular_k_paths)
        layout_k.addWidget(btn_calcular)
        layout_nodos = QHBoxLayout()
        layout_nodos.addWidget(QLabel("Origen:"))
        self.spin_origen = QSpinBox()
        self.spin_origen.setRange(0, 4)
        layout_nodos.addWidget(self.spin_origen)
        layout_nodos.addWidget(QLabel("Destino:"))
        self.spin_destino = QSpinBox()
        self.spin_destino.setRange(0, 4)
        self.spin_destino.setValue(4)
        layout_nodos.addWidget(self.spin_destino)
        layout_k.addLayout(layout_nodos)
        btn_camino = QPushButton("Encontrar K Caminos")
        btn_camino.clicked.connect(self.encontrar_caminos_especificos)
        layout_k.addWidget(btn_camino)
        grupo_k.setLayout(layout_k)
        layout.addWidget(grupo_k)
        self.texto_resultados = QTextEdit()
        self.texto_resultados.setReadOnly(True)
        self.texto_resultados.setMaximumHeight(200)
        layout.addWidget(QLabel("Resultados:"))
        layout.addWidget(self.texto_resultados)
        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def crear_panel_grafo(self):
        panel = QWidget()
        layout = QVBoxLayout()
        titulo = QLabel("Visualización del Grafo")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(titulo)
        self.graphics_view = QtWidgets.QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setRenderHint(QtGui.QPainter.Antialiasing)
        layout.addWidget(self.graphics_view)
        panel.setLayout(layout)
        return panel

    def cambiar_tamano_matriz(self, tamano):
        self.tabla_matriz.setRowCount(tamano)
        self.tabla_matriz.setColumnCount(tamano)
        self.spin_origen.setRange(0, tamano - 1)
        self.spin_destino.setRange(0, tamano - 1)
        self.spin_destino.setValue(tamano - 1)
        self.limpiar_matriz()

    def llenar_matriz_aleatoria(self):
        """Llena la matriz con valores aleatorios y asegura que todos los nodos estén conectados"""
        filas = self.tabla_matriz.rowCount()
        columnas = self.tabla_matriz.columnCount()

        # Ajustar la probabilidad según el tamaño (más grande = menos conexiones)
        if filas <= 4:
            prob_conexion = 0.9
        elif filas <= 6:
            prob_conexion = 0.75
        elif filas <= 8:
            prob_conexion = 0.6
        else:
            prob_conexion = 0.5

        # Inicializar matriz con ceros
        matriz = [[0 for _ in range(columnas)] for _ in range(filas)]

        # Generar conexiones aleatorias según la probabilidad
        for i in range(filas):
            for j in range(i + 1, columnas):
                if random.random() < prob_conexion:
                    peso = random.randint(1, 20)
                    matriz[i][j] = peso
                    matriz[j][i] = peso  # grafo no dirigido

        # Asegurar que todos los nodos estén conectados al menos una vez
        for i in range(filas):
            if all(matriz[i][j] == 0 for j in range(columnas) if j != i):
                # Si el nodo está aislado, conéctalo a otro nodo aleatorio
                j = random.choice([x for x in range(filas) if x != i])
                peso = random.randint(1, 20)
                matriz[i][j] = peso
                matriz[j][i] = peso

        # Mostrar en la tabla
        for i in range(filas):
            for j in range(columnas):
                item = QtWidgets.QTableWidgetItem(str(matriz[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tabla_matriz.setItem(i, j, item)

        self.texto_resultados.append(
            f"Grafo aleatorio generado ({int(prob_conexion * 100)}% conectividad garantizada)\n"
        )

    def limpiar_matriz(self):
        filas = self.tabla_matriz.rowCount()
        columnas = self.tabla_matriz.columnCount()
        for i in range(filas):
            for j in range(columnas):
                item = QtWidgets.QTableWidgetItem("0")
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tabla_matriz.setItem(i, j, item)

    def obtener_matriz(self):
        filas = self.tabla_matriz.rowCount()
        matriz = []
        for i in range(filas):
            fila = []
            for j in range(filas):
                item = self.tabla_matriz.item(i, j)
                valor = int(item.text()) if item and item.text().isdigit() else 0
                fila.append(valor)
            matriz.append(fila)
        return matriz

    def dibujar_grafo(self):
        self.scene.clear()
        self.nodos.clear()
        self.aristas.clear()
        self.matrix = self.obtener_matriz()
        num_nodos = len(self.matrix)
        radius = 20
        center_x = self.graphics_view.width() / 2
        center_y = self.graphics_view.height() / 2
        circle_radius = min(center_x, center_y) - 100
        for i in range(num_nodos):
            angulo = 2 * np.pi * i / num_nodos
            x = center_x + circle_radius * np.cos(angulo)
            y = center_y + circle_radius * np.sin(angulo)
            nodo = Nodo(x, y, radius, i, self)
            nodo.setPos(x, y)
            self.scene.addItem(nodo)
            self.nodos.append(nodo)
        for i in range(num_nodos):
            for j in range(num_nodos):
                if self.matrix[i][j] > 0 and i != j:
                    arista = Arista(self.nodos[i], self.nodos[j], self.matrix[i][j], self.scene)
                    self.scene.addItem(arista)
                    self.aristas.append(arista)
                    self.nodos[i].agregar_arista(arista)
        self.texto_resultados.append("✓ Grafo dibujado exitosamente\n")

    def restaurar_colores(self):
        for nodo in self.nodos:
            nodo.restaurar()
        for arista in self.aristas:
            arista.restaurar()

    def calcular_k_paths(self):
        if not self.matrix:
            self.texto_resultados.append("⚠ Primero debes dibujar el grafo\n")
            return
        k = int(self.combo_k.currentText())
        matriz_k = self.kpaths.compute(self.matrix, k)
        texto = f"\n=== MATRIZ DE {k}-CAMINOS ===\n"
        for i in range(len(matriz_k)):
            row = " ".join(f"{int(v) if v != float('inf') else '∞':>4}" for v in matriz_k[i])
            texto += f"N{i}: {row}\n"
        self.texto_resultados.append(texto)

    def encontrar_caminos_especificos(self):
        if not self.matrix:
            self.texto_resultados.append("⚠ Primero debes dibujar el grafo\n")
            return
        origen = self.spin_origen.value()
        destino = self.spin_destino.value()
        k = int(self.combo_k.currentText())
        caminos = self.kpaths.find_k_shortest_paths(origen, destino, k)
        if not caminos:
            self.texto_resultados.append(f"✗ No hay caminos entre N{origen} y N{destino}\n")
            return
        self.restaurar_colores()
        texto = f"\n{'=' * 50}\nBuscando {k} caminos de N{origen} a N{destino}\n{'=' * 50}\n"
        for idx, (costo, camino) in enumerate(caminos, 1):
            camino_str = " → ".join(f"N{n}" for n in camino)
            texto += f"\nCamino #{idx}:\n  Ruta: {camino_str}\n  Costo: {costo}\n"
            # Resaltar primer camino
            if idx == 1:
                for i in range(len(camino) - 1):
                    self.nodos[camino[i]].resaltar("#2ECC71")
                    for arista in self.aristas:
                        if ((arista.nodo1.id == camino[i] and arista.nodo2.id == camino[i + 1]) or
                                (arista.nodo2.id == camino[i] and arista.nodo1.id == camino[i + 1])):
                            arista.resaltar()
                self.nodos[camino[-1]].resaltar("#2ECC71")
        self.texto_resultados.append(texto)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ventana = GrafoApp()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
