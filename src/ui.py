"""
Interfaz gráfica para el algoritmo de K-Caminos
Maneja toda la interacción con el usuario y visualización
"""

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QLabel, QComboBox, QSpinBox, QTextEdit, QGroupBox,
                             QGraphicsView, QGraphicsScene, QMessageBox)
from PyQt5.QtCore import Qt
from graph import Graph
from algorithms.k_paths import KPaths


class GraphUI(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        self.graph = Graph()
        self.kpaths = KPaths()
        self.scene = QGraphicsScene()
        
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """Inicializa todos los componentes de la interfaz"""
        self.setWindowTitle("Algoritmo de K-Caminos Más Cortos")
        self.setGeometry(100, 100, 1400, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Panel izquierdo: controles
        left_panel = self.create_control_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Panel derecho: visualización
        right_panel = self.create_visualization_panel()
        main_layout.addWidget(right_panel, 2)
        
    def create_control_panel(self):
        """Crea el panel de controles"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Título
        title = QLabel("Control de Grafos")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Grupo: Configuración del grafo
        config_group = QGroupBox("Configuración")
        config_layout = QVBoxLayout()
        
        # Número de nodos
        nodes_layout = QHBoxLayout()
        nodes_layout.addWidget(QLabel("Número de nodos:"))
        self.spin_nodes = QSpinBox()
        self.spin_nodes.setRange(3, 10)
        self.spin_nodes.setValue(5)
        nodes_layout.addWidget(self.spin_nodes)
        config_layout.addLayout(nodes_layout)
        
        # Botón generar grafo aleatorio
        self.btn_generate = QPushButton("Generar Grafo Aleatorio")
        self.btn_generate.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        config_layout.addWidget(self.btn_generate)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Grupo: Matriz de adyacencia
        matrix_group = QGroupBox("Matriz de Adyacencia")
        matrix_layout = QVBoxLayout()
        
        self.table_matrix = QTableWidget()
        self.table_matrix.setMaximumHeight(250)
        matrix_layout.addWidget(self.table_matrix)
        
        self.btn_draw = QPushButton("Dibujar Grafo")
        self.btn_draw.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        matrix_layout.addWidget(self.btn_draw)
        
        matrix_group.setLayout(matrix_layout)
        layout.addWidget(matrix_group)
        
        # Grupo: K-Paths
        kpaths_group = QGroupBox("Algoritmo K-Paths")
        kpaths_layout = QVBoxLayout()
        
        k_layout = QHBoxLayout()
        k_layout.addWidget(QLabel("Valor de K:"))
        self.combo_k = QComboBox()
        self.combo_k.addItems(["1", "2", "3"])
        self.combo_k.setCurrentText("2")
        k_layout.addWidget(self.combo_k)
        kpaths_layout.addLayout(k_layout)
        
        self.btn_compute = QPushButton("Calcular K-Caminos")
        self.btn_compute.setStyleSheet("background-color: #FF9800; color: white; padding: 8px;")
        kpaths_layout.addWidget(self.btn_compute)
        
        kpaths_group.setLayout(kpaths_layout)
        layout.addWidget(kpaths_group)
        
        # Área de resultados
        results_group = QGroupBox("Resultados")
        results_layout = QVBoxLayout()
        
        self.text_results = QTextEdit()
        self.text_results.setReadOnly(True)
        self.text_results.setMaximumHeight(200)
        results_layout.addWidget(self.text_results)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        layout.addStretch()
        return panel
        
    def create_visualization_panel(self):
        """Crea el panel de visualización del grafo"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        title = QLabel("Visualización del Grafo")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.graphics_view = QGraphicsView()
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphics_view.setStyleSheet("background-color: #f5f5f5; border: 2px solid #ddd;")
        layout.addWidget(self.graphics_view)
        
        return panel
        
    def setup_connections(self):
        """Conecta señales con slots"""
        self.btn_generate.clicked.connect(self.generate_random_graph)
        self.btn_draw.clicked.connect(self.draw_graph)
        self.btn_compute.clicked.connect(self.compute_kpaths)
        self.spin_nodes.valueChanged.connect(self.update_table_size)
        
        # Inicializar tabla
        self.update_table_size()
        
    def update_table_size(self):
        """Actualiza el tamaño de la tabla según el número de nodos"""
        n = self.spin_nodes.value()
        self.table_matrix.setRowCount(n)
        self.table_matrix.setColumnCount(n)
        
        # Headers
        headers = [str(i) for i in range(n)]
        self.table_matrix.setHorizontalHeaderLabels(headers)
        self.table_matrix.setVerticalHeaderLabels(headers)
        
        # Inicializar con ceros
        for i in range(n):
            for j in range(n):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                self.table_matrix.setItem(i, j, item)
                
    def generate_random_graph(self):
        """Genera un grafo aleatorio (no completamente conectado)"""
        import random
        n = self.spin_nodes.value()
        
        # Generar matriz con probabilidad de conexión del 40%
        for i in range(n):
            for j in range(n):
                if i == j:
                    self.table_matrix.item(i, j).setText("0")
                elif i < j:
                    # 40% de probabilidad de conexión
                    if random.random() < 0.4:
                        peso = random.randint(1, 15)
                        self.table_matrix.item(i, j).setText(str(peso))
                        self.table_matrix.item(j, i).setText(str(peso))
                    else:
                        self.table_matrix.item(i, j).setText("0")
                        self.table_matrix.item(j, i).setText("0")
                        
        self.text_results.append("Grafo aleatorio generado (40% conectividad)\n")
        
    def get_matrix_from_table(self):
        """Obtiene la matriz de adyacencia desde la tabla"""
        n = self.table_matrix.rowCount()
        matrix = []
        
        for i in range(n):
            row = []
            for j in range(n):
                try:
                    value = int(self.table_matrix.item(i, j).text())
                    row.append(value)
                except:
                    row.append(0)
            matrix.append(row)
            
        return matrix
        
    def draw_graph(self):
        """Dibuja el grafo en la escena"""
        matrix = self.get_matrix_from_table()
        self.graph.load_from_matrix(matrix)
        
        self.scene.clear()
        self.graph.draw(self.scene, self.graphics_view.width(), self.graphics_view.height())
        
        self.text_results.append("Grafo dibujado correctamente\n")

    def compute_kpaths(self):
        """Calcula y muestra los K-caminos"""
        matrix = self.get_matrix_from_table()
        k = int(self.combo_k.currentText())

        try:
            result_matrix = self.kpaths.compute(matrix, k)

            self.text_results.clear()
            self.text_results.append(f"=== MATRIZ DE {k}-CAMINOS MÁS CORTOS ===\n")

            # Mostrar matriz resultado
            n = len(result_matrix)
            for i in range(n):
                row_str = " ".join([
                    f"{val:6.1f}" if val != float('inf') else "   ∞  "
                    for val in result_matrix[i]
                ])
                self.text_results.append(f"Nodo {i}: [{row_str}]")

            self.text_results.append(f"\nCálculo completado para K={k}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al calcular K-Paths: {str(e)}")

