from PySide6.QtWidgets import (
    QWidget, QScrollArea, QLineEdit, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QFrame, QMessageBox, QFileDialog
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QSize
from PySide6.QtGui import QFont, QIcon, QColor
from estructuras.queue import Cola


class ColaView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.cola = Cola()
        self.cargar_ui()
        self.conectar_signals()
        self.setWindowTitle("Queue | Cola")
        self.setStyleSheet("""
            background-color: white;
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: black;
            }
        """)

    def cargar_ui(self):
        loader = QUiLoader()
        ui_file = QFile("estructuras_ui/queue_view.ui")
        if not ui_file.open(QFile.ReadOnly):
            self.mostrar_error("Error", "No se pudo abrir el archivo de UI.")
            return
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(self.ui)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout_principal)

        self.label_tamaño = self.ui.findChild(QLabel, "label_tamaño")
        self.input_valor = self.ui.findChild(QLineEdit, "input_valor")
        self.btn_insertar = self.ui.findChild(QPushButton, "btn_insertar")
        self.btn_eliminar = self.ui.findChild(QPushButton, "btn_eliminar")
        self.btn_buscar = self.ui.findChild(QPushButton, "btn_buscar")
        self.btn_regresar = self.ui.findChild(QPushButton, "btn_regresar")
        self.btn_reiniciar = self.ui.findChild(QPushButton, "btn_reiniciar")
        self.btn_guardar = self.ui.findChild(QPushButton, "btn_guardar")

        try:
            self.btn_regresar.setIcon(QIcon("resources/back_arrow.png"))
            self.btn_regresar.setIconSize(QSize(24, 24))
        except:
            pass

        self.scrollArea = self.ui.findChild(QScrollArea, "scrollArea")
        self.colaContainer = self.scrollArea.findChild(QWidget, "colaContainer")
        self.layoutCola = self.colaContainer.findChild(QHBoxLayout, "layoutCola")

    def conectar_signals(self):
        self.btn_insertar.clicked.connect(self.insertar_valor)
        self.btn_eliminar.clicked.connect(self.eliminar_valor)
        self.btn_buscar.clicked.connect(self.buscar_valor)
        self.btn_regresar.clicked.connect(self.regresar_dashboard)
        self.btn_reiniciar.clicked.connect(self.reiniciar_cola)
        self.btn_guardar.clicked.connect(self.guardar_cola)



    def convertir_valor(self, texto):
        texto = texto.strip()
        if not texto:
            raise ValueError("Ingrese un valor")

        # Si la cola no está vacía, validar tipo
        if not self.cola.esta_vacia():
            tipo_actual = self.cola.tipo_dato
            # String es el tipo más permisivo
            if tipo_actual == str:
                return texto
            try:
                if tipo_actual == bool:
                    if texto.lower() in ['true', 'false']:
                        return texto.lower() == 'true'
                    raise ValueError("Para booleanos use 'true' o 'false'")
                return tipo_actual(texto)
            except ValueError:
                raise ValueError(f"Ingrese un {tipo_actual.__name__} válido")

        # Si la cola está vacía, determinar tipo
        try:
            return int(texto)
        except ValueError:
            try:
                return float(texto)
            except ValueError:
                if texto.lower() in ['true', 'false']:
                    return texto.lower() == 'true'
                return texto  # Default a string

    def guardar_cola(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Guardar Cola", "", "JSON Files (*.json)")

        if filename:
            if not filename.endswith('.json'):
                filename += '.json'

            try:
                self.cola.guardar_a_archivo(filename)
                self.mostrar_mensaje("Éxito", f"Cola guardada en {filename}")
            except Exception as e:
                self.mostrar_error("Error", f"No se pudo guardar: {str(e)}")

    def insertar_valor(self):
        texto = self.input_valor.text()
        try:
            valor = self.convertir_valor(texto)
            self.cola.insertar(valor)
            self.input_valor.clear()
            self.actualizar_vista()
        except ValueError as e:
            self.mostrar_error("Error de tipo", str(e))
        except Exception as e:
            self.mostrar_error("Error", str(e))

    def eliminar_valor(self):
        if self.cola.esta_vacia():
            self.mostrar_error("Cola vacía", "No hay elementos para eliminar")
            return

        valor = self.cola.eliminar()
        self.mostrar_mensaje("Éxito", f"Se eliminó: {valor}")
        self.actualizar_vista()

    def buscar_valor(self):
        texto = self.input_valor.text()
        if not texto.strip():
            self.mostrar_error("Campo vacío", "Ingrese un valor para buscar")
            return

        try:
            valor = self.convertir_valor(texto)
            pos = self.cola.buscar(valor)
            if pos == -1:
                self.mostrar_mensaje("Búsqueda", f"Valor '{valor}' no encontrado")
            else:
                self.mostrar_mensaje("Búsqueda", f"Valor encontrado en posición {pos}")
        except ValueError as e:
            self.mostrar_error("Error de búsqueda", str(e))

    def reiniciar_cola(self):
        self.cola.reiniciar()
        self.actualizar_vista()
        self.mostrar_mensaje("Cola reiniciada", "Ahora puede ingresar cualquier tipo de dato")

    def actualizar_vista(self):
        self.clear_layout(self.layoutCola)
        elementos = self.cola.obtener_todos()
        for valor in elementos:
            nodo_widget = self.crear_widget_nodo(valor)
            self.layoutCola.addWidget(nodo_widget)
        self.label_tamaño.setText(f"Tamaño: {self.cola.tamaño}")

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def crear_widget_nodo(self, valor):
        nodo = QFrame()
        nodo.setFrameShape(QFrame.NoFrame)
        nodo.setFrameShadow(QFrame.Raised)
        nodo.setStyleSheet("""
            background-color: #3b72bf; 
            border-radius: 3px; 
            padding: 3px; 
            margin: 3px;
        """)
        etiqueta = QLabel(str(valor), nodo)
        etiqueta.setAlignment(Qt.AlignCenter)
        etiqueta.setStyleSheet("color: white;")
        font = QFont("Arial", 20, QFont.Bold)
        etiqueta.setFont(font)
        layout_nodo = QVBoxLayout(nodo)
        layout_nodo.addWidget(etiqueta)
        return nodo

    def regresar_dashboard(self):
        if self.main_window:
            self.hide()
            self.main_window.show()

    def mostrar_error(self, titulo, mensaje):
        msg = QMessageBox(self)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: black;
            }
            QLabel {
                color: black;
                font-size: 14px;
            }
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 5px 10px;
                min-width: 80px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.exec()

    def mostrar_mensaje(self, titulo, mensaje):
        msg = QMessageBox(self)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: black;
            }
            QLabel {
                color: black;
                font-size: 14px;
            }
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 5px 10px;
                min-width: 80px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.exec()

    def showEvent(self, event):
        if self.main_window:
            self.resize(self.main_window.size())
        super().showEvent(event)