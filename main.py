# main.py modificado
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
import sys
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = "mainwindow.ui"

        #carga el archivo .ui
        loader = QUiLoader()
        ui_file = QFile(ui_path)

        #carga el ui como widget independiente
        self.ui = loader.load(ui_file, None)
        ui_file.close()


        #Ventana principal
        self.setWindowTitle(self.ui.windowTitle())
        self.resize(self.ui.size())
        self.setCentralWidget(self.ui)


        self.ui.btnPila.clicked.connect(self.show_stack_view)
        self.ui.btnListaSimple.clicked.connect(self.show_singly_linked_list_view)
        self.ui.btnListaDoble.clicked.connect(self.show_doubly_linked_list_view)
        self.ui.btnListaCircular.clicked.connect(self.show_circular_list_view)
        self.ui.btnArbolBinario.clicked.connect(self.show_binary_tree_view)
        self.ui.btnArbolBusqueda.clicked.connect(self.show_bst_view)


    # la encontre en stack overflow, para despues de apretar un boton se limpie la pantalla anterior
    def clear_central_layout(self):
        layout = self.ui.centralwidget.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


    #cunc de Cada Vista
    def show_stack_view(self):
        print("Mostrar vista de Pila")

    def show_singly_linked_list_view(self):
        print("Mostrar vista de Lista Simple")

    def show_doubly_linked_list_view(self):
        print("Mostrar vista de Lista Doble")

    def show_circular_list_view(self):
        print("Mostrar vista de Lista Circular")

    def show_binary_tree_view(self):
        print("Mostrar vista de Árbol Binario")

    def show_bst_view(self):
        print("Mostrar vista de Árbol de Búsqueda")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())