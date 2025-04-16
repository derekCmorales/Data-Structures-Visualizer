# view_estructuras/stack_view.py

from PySide6.QtWidgets import (
    QWidget, QScrollArea, QLineEdit, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QFrame, QMessageBox, QListWidgetItem, QMainWindow
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QSize
from PySide6.QtGui import QFont, QColor, QIcon
from estructuras.stack import Pila


class PilaView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.pila = Pila()
        self.cargar_ui()
        self.conectar_signals()

        self.setWindowTitle("Stack | Pila")

    def cargar_ui(self):
        loader = QUiLoader()
        ui_file = QFile("estructuras_ui/stack_view.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise Exception("No se pudo abrir el archivo de UI.")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        def regresar_dashboard(self):
            if self.main_window:
                self.hide()
                self.main_window.show()
            else:
                self.close()

        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(self.ui)
        layout_principal.setContentsMargins(0, 0, 0, 0)  # Para que cubra toda la pantalla
        self.setLayout(layout_principal)

        self.label_tamaño = self.ui.findChild(QLabel, "label_tamaño")
        self.input_valor = self.ui.findChild(QLineEdit, "input_valor")
        self.btn_insertar = self.ui.findChild(QPushButton, "btn_insertar")
        self.btn_eliminar = self.ui.findChild(QPushButton, "btn_eliminar")
        self.btn_buscar = self.ui.findChild(QPushButton, "btn_buscar")
        self.btn_regresar = self.ui.findChild(QPushButton, "btn_regresar")


        try:
            self.btn_regresar.setIcon(QIcon("resources/back_arrow.png"))
            self.btn_regresar.setIconSize(QSize(24, 24))
        except:
            pass

        self.scrollArea = self.ui.findChild(QScrollArea, "scrollArea")
        self.pilaContainer = self.scrollArea.findChild(QWidget, "pilaContainer")
        self.layoutPila = self.pilaContainer.findChild(QVBoxLayout, "layoutPila")

    def conectar_signals(self):
        self.btn_insertar.clicked.connect(self.insertar_valor)
        self.btn_eliminar.clicked.connect(self.eliminar_valor)
        self.btn_buscar.clicked.connect(self.buscar_valor)
        self.btn_regresar.clicked.connect(self.regresar_dashboard)

    def regresar_dashboard(self):
        if self.main_window:
            self.hide()
            self.main_window.show()
            self.main_window.resize(self.main_window.ui.size())
            self.main_window.setCentralWidget(self.main_window.ui)

    def showEvent(self, event):

        if self.main_window:
            self.resize(self.main_window.size())
        super().showEvent(event)

    def actualizar_vista(self):
        self.clear_layout(self.layoutPila)
        elementos = self.pila.obtener_todos()
        for valor in elementos:
            nodo_widget = self.crear_widget_nodo(valor)
            self.layoutPila.addWidget(nodo_widget)
        self.label_tamaño.setText(f"Tamaño: {self.pila.tamaño}")

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def crear_widget_nodo(self, valor):
        nodo = QFrame()
        nodo.setFrameShape(QFrame.NoFrame)
        nodo.setFrameShadow(QFrame.Raised)
        nodo.setStyleSheet(
            "background-color: #3b72bf; border-radius: 3px; padding: 3px; margin: 3px;"
        )
        etiqueta = QLabel(str(valor), nodo)
        etiqueta.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)
        etiqueta.setFont(font)
        layout_nodo = QVBoxLayout(nodo)
        layout_nodo.addWidget(etiqueta)
        return nodo

    def eliminar_valor(self):
        if self.pila.esta_vacia():
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Pila vacía")
            msg_box.setText("No hay elementos para eliminar.")
            msg_box.setStyleSheet("QLabel{color: black;}")
            msg_box.exec()
            return

        valor = self.pila.eliminar()
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Elemento eliminado")
        msg_box.setText(f"Se eliminó: {valor}")
        msg_box.setStyleSheet("QLabel{color: black;}")
        msg_box.exec()
        self.actualizar_vista()

    def insertar_valor(self):
        valor = self.input_valor.text().strip()
        if not valor:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Error")
            msg_box.setText("Ingrese un valor")
            msg_box.setStyleSheet("QLabel{color: white;}")
            msg_box.exec()
            return
        self.pila.insertar(valor)
        self.input_valor.clear()
        self.actualizar_vista()

    def buscar_valor(self):
        valor = self.input_valor.text().strip()
        if not valor:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Error")
            msg_box.setText("Ingrese un valor para buscar.")
            msg_box.setStyleSheet("QLabel{color: white;}")
            msg_box.exec()
            return

        pos = self.pila.buscar(valor)
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Resultado")

        if pos == -1:
            msg_box.setText(f"El valor '{valor}' no se encontró.")
        else:
            msg_box.setText(f"El valor '{valor}' se encontró en la posición {pos} desde la cima.")

        msg_box.setStyleSheet("QLabel{color: white;}")
        msg_box.exec()