"""
Punto de entrada principal del programa
Inicializa la aplicación de K-Caminos
"""

import sys
from PyQt5 import QtWidgets
from ui import GraphUI


def main():
    """Inicializa y ejecuta la aplicación"""
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("K-Paths Algorithm")

    window = GraphUI()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
