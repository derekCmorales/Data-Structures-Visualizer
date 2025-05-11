from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
import sys
import os
import resources_rc
import json
from view_estructuras.singly_linked_list_view import ListaSimpleView
from view_estructuras.stack_view import PilaView
from view_estructuras.queue_view import ColaView
from estructuras.stack import Pila
from estructuras.queue import Cola
from estructuras.singly_linked_list import ListaSimple
from view_estructuras.doubly_linked_list_view import ListaDobleView
from view_estructuras.circular_list_view import ListaCircularView
from estructuras.circular_linked_list import ListaCircular



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicializar variables de vista
        self.vista_pila = None
        self.vista_cola = None
        self.vista_lista_simple = None
        self.vista_lista_doble = None
        self.vista_lista_circular = None

        # Cargar la interfaz
        self.cargar_interfaz()

        # Conectar señales
        self.conectar_signals()

    def cargar_interfaz(self):
        """Carga la interfaz desde el archivo .ui"""
        ui_path = "mainwindow.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)

        if not ui_file.open(QFile.ReadOnly):
            raise Exception("No se pudo abrir el archivo de UI: " + ui_path)

        self.ui = loader.load(ui_file)
        ui_file.close()

        self.setWindowTitle(self.ui.windowTitle())
        self.resize(self.ui.size())
        self.setCentralWidget(self.ui)

        # Asegurarse de que el botón de carga existe
        if not hasattr(self.ui, 'btnCargar'):
            raise AttributeError("El archivo UI debe contener un botón llamado 'btnCargar'")

    def conectar_signals(self):
        """Conecta todas las señales de los botones"""
        self.ui.btnPila.clicked.connect(self.show_stack_view)
        self.ui.btnListaSimple.clicked.connect(self.show_singly_linked_list_view)
        self.ui.btnListaDoble.clicked.connect(self.show_doubly_linked_list_view)
        self.ui.btnListaCircular.clicked.connect(self.show_circular_list_view)
        self.ui.btnArbolBinario.clicked.connect(self.show_binary_tree_view)
        self.ui.btnArbolBusqueda.clicked.connect(self.show_bst_view)
        self.ui.btnCola.clicked.connect(self.show_queue_view)
        self.ui.btnCargar.clicked.connect(self.cargar_archivo)

    def clear_central_layout(self):
        layout = self.ui.centralwidget.layout()
        if layout:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

    def show_stack_view(self):
        if not self.vista_pila:
            self.vista_pila = PilaView(main_window=self)

        self.hide()
        self.vista_pila.show()
        self.vista_pila.resize(self.size())

    def show_singly_linked_list_view(self):
        if not self.vista_lista_simple:
            self.vista_lista_simple = ListaSimpleView(main_window=self)

        self.hide()
        self.vista_lista_simple.show()
        self.vista_lista_simple.resize(self.size())
    def show_doubly_linked_list_view(self):
        if not self.vista_lista_doble:
            self.vista_lista_doble = ListaDobleView(main_window=self)

        self.hide()
        self.vista_lista_doble.show()
        self.vista_lista_doble.resize(self.size())

    def show_circular_list_view(self):
        if not self.vista_lista_circular:
            self.vista_lista_circular = ListaCircularView(main_window=self)

        self.hide()
        self.vista_lista_circular.show()
        self.vista_lista_circular.resize(self.size())

    def show_binary_tree_view(self):
        print("Mostrar vista de Árbol Binario")

    def show_bst_view(self):
        print("Mostrar vista de Árbol de Búsqueda")

    def show_queue_view(self):
        if not self.vista_cola:
            self.vista_cola = ColaView(main_window=self)

        self.hide()
        self.vista_cola.show()
        self.vista_cola.resize(self.size())

    def cargar_archivo(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Abrir archivo", "", "JSON Files (*.json)")

        if not filename:
            return

        try:
            with open(filename, 'r') as f:
                datos = json.load(f)

            tipo_estructura = datos.get('tipo_estructura')

            if tipo_estructura == 'pila':
                pila = Pila.cargar_desde_archivo(filename)
                if not self.vista_pila:
                    self.vista_pila = PilaView(main_window=self)
                self.vista_pila.pila = pila
                self.vista_pila.actualizar_vista()
                self.hide()
                self.vista_pila.show()

            elif tipo_estructura == 'cola':
                cola = Cola.cargar_desde_archivo(filename)
                if not self.vista_cola:
                    self.vista_cola = ColaView(main_window=self)
                self.vista_cola.cola = cola
                self.vista_cola.actualizar_vista()
                self.hide()
                self.vista_cola.show()

            else:
                self.mostrar_error("Error", "Tipo de estructura no reconocido")

        except Exception as e:
            self.mostrar_error("Error", f"No se pudo cargar el archivo: {str(e)}")

    def mostrar_error(self, titulo, mensaje):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())