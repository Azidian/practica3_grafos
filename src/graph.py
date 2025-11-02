"""
Clases para representar y visualizar grafos
"""

from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
import math
import random


class Node(QGraphicsEllipseItem):
    """Representa un nodo visual en el grafo"""
    
    def __init__(self, node_id, x, y, radius=25):
        super().__init__(-radius, -radius, radius*2, radius*2)
        self.node_id = node_id
        self.radius = radius
        self.edges = []
        
        # Estilo del nodo
        self.setBrush(QBrush(QColor(66, 165, 245)))
        self.setPen(QPen(QColor(33, 150, 243), 2))
        
        # Posición
        self.setPos(x, y)
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges)
        
        # Etiqueta del nodo
        self.label = QGraphicsTextItem(str(node_id), self)
        self.label.setDefaultTextColor(Qt.white)
        font = QFont("Arial", 12, QFont.Bold)
        self.label.setFont(font)
        
        # Centrar etiqueta
        label_rect = self.label.boundingRect()
        self.label.setPos(-label_rect.width()/2, -label_rect.height()/2)
        
    def add_edge(self, edge):
        """Agrega una arista conectada a este nodo"""
        self.edges.append(edge)
        
    def itemChange(self, change, value):
        """Se llama cuando el nodo se mueve"""
        if change == QGraphicsEllipseItem.ItemPositionHasChanged:
            for edge in self.edges:
                edge.update_position()
        return super().itemChange(change, value)


class Edge(QGraphicsLineItem):
    """Representa una arista visual en el grafo"""
    
    def __init__(self, source_node, target_node, weight):
        super().__init__()
        self.source = source_node
        self.target = target_node
        self.weight = weight
        
        # Estilo de la arista
        self.setPen(QPen(QColor(100, 100, 100), 2))
        
        # Etiqueta del peso
        self.label = QGraphicsTextItem(str(weight))
        self.label.setDefaultTextColor(QColor(255, 87, 34))
        font = QFont("Arial", 10, QFont.Bold)
        self.label.setFont(font)
        
        # Agregar esta arista a los nodos
        source_node.add_edge(self)
        target_node.add_edge(self)
        
        self.update_position()
        
    def update_position(self):
        """Actualiza la posición de la línea cuando los nodos se mueven"""
        source_pos = self.source.pos()
        target_pos = self.target.pos()
        
        # Calcular puntos en el borde de los círculos
        dx = target_pos.x() - source_pos.x()
        dy = target_pos.y() - source_pos.y()
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalizar
            dx /= distance
            dy /= distance
            
            # Puntos en el borde
            start_x = source_pos.x() + dx * self.source.radius
            start_y = source_pos.y() + dy * self.source.radius
            end_x = target_pos.x() - dx * self.target.radius
            end_y = target_pos.y() - dy * self.target.radius
            
            self.setLine(start_x, start_y, end_x, end_y)
            
            # Posicionar etiqueta en el medio
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            label_rect = self.label.boundingRect()
            self.label.setPos(mid_x - label_rect.width()/2, 
                            mid_y - label_rect.height()/2)


class Graph:
    """Representa la estructura del grafo y maneja su visualización"""
    
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.matrix = []
        
    def load_from_matrix(self, matrix):
        """Carga el grafo desde una matriz de adyacencia"""
        self.matrix = matrix
        
    def draw(self, scene, width=800, height=600):
        """Dibuja el grafo en la escena"""
        self.nodes.clear()
        self.edges.clear()
        
        n = len(self.matrix)
        if n == 0:
            return
            
        # Calcular posiciones en círculo
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) * 0.35
        
        # Crear nodos
        for i in range(n):
            angle = 2 * math.pi * i / n - math.pi / 2
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            node = Node(i, x, y)
            self.nodes.append(node)
            scene.addItem(node)
            scene.addItem(node.label)
            
        # Crear aristas
        for i in range(n):
            for j in range(i+1, n):
                weight = self.matrix[i][j]
                if weight > 0:
                    edge = Edge(self.nodes[i], self.nodes[j], weight)
                    self.edges.append(edge)
                    scene.addItem(edge)
                    scene.addItem(edge.label)
