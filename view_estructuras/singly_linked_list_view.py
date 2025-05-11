from PySide6.QtCore import Qt, QFile, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QPoint, QSize
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QScrollArea,
    QHBoxLayout, QVBoxLayout, QMessageBox, QFileDialog, QFrame,
    QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QFont, QColor, QPixmap, QFontDatabase
from estructuras.singly_linked_list import ListaSimple
import resources_rc


class ListaSimpleView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.lista = ListaSimple()
        self.animations = QParallelAnimationGroup()

        self.ui = None
        self.scroll_area = None
        self.lista_layout = None
        self.input_valor = None

        self.inicializar_ui()
        self.inicializar_componentes()
        self.conectar_eventos()
        self.configurar_estilos()

    def inicializar_ui(self):
        try:
            loader = QUiLoader()
            ui_file = QFile("estructuras_ui/singly_linked_list_view.ui")
            if not ui_file.open(QFile.ReadOnly):
                raise FileNotFoundError(f"Archivo UI no encontrado: {ui_file.fileName()}")

            # Cargar el widget principal correctamente
            self.ui = loader.load(ui_file, self)
            ui_file.close()

            if not self.ui:
                raise RuntimeError("El archivo UI no pudo ser cargado. Verifica el diseño.")

            layout = QVBoxLayout(self)
            layout.addWidget(self.ui)
            layout.setContentsMargins(0, 0, 0, 0)
            self.setLayout(layout)

        except Exception as e:
            QMessageBox.critical(None, "Error UI", f"Error crítico al cargar la UI:\n{str(e)}")
            raise

    def inicializar_componentes(self):
        # Obtener el scroll area
        self.scroll_area = self.ui.findChild(QScrollArea, "scrollArea")

        # Buscar el contenedor por su nombre
        contenedor = self.scroll_area.findChild(QWidget, "contenedorLista")

        if contenedor is None:
            raise RuntimeError("Asegúrate de que el QScrollArea contenga un QWidget llamado 'contenedorLista'")

        # Configurar el layout
        if not contenedor.layout():
            contenedor.setLayout(QHBoxLayout())

        self.lista_layout = contenedor.layout()
        self.input_valor = self.ui.findChild(QLineEdit, "input_valor")

    def configurar_estilos(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                background-color: #f0f0f0;
            }
            QFrame#nodo {
                background-color: #2d334a;
                border-radius: 15px;
                border: 3px solid #4a5065;
                margin: 15px;
                min-width: 200px;
                min-height: 120px;
            }
            QLabel#valor {
                color: #ffffff;
                font: bold 24px;
                qproperty-alignment: AlignCenter;
            }
            QLabel#direccion {
                color: #cbd5e1;
                font: 14px 'Consolas';
                qproperty-alignment: AlignCenter;
            }
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)

    def conectar_eventos(self):
        try:
            self.ui.btn_insertar_inicio.clicked.connect(lambda: self.insertar("inicio"))
            self.ui.btn_insertar_final.clicked.connect(lambda: self.insertar("final"))
            self.ui.btn_eliminar_inicio.clicked.connect(lambda: self.eliminar("inicio"))
            self.ui.btn_eliminar_final.clicked.connect(lambda: self.eliminar("final"))
            self.ui.btn_buscar.clicked.connect(self.buscar_valor)
            self.ui.btn_reiniciar.clicked.connect(self.reiniciar_lista)
            self.ui.btn_guardar.clicked.connect(self.guardar_lista)
            self.ui.btn_cargar.clicked.connect(self.cargar_lista)
            self.ui.btn_regresar.clicked.connect(self.regresar_al_dashboard)
        except AttributeError as e:
            QMessageBox.critical(self, "Error", f"Componente no encontrado: {str(e)}")
            raise

    def convertir_valor(self, texto):
        texto = texto.strip()
        if not texto:
            raise ValueError("Ingrese un valor válido")

        if self.lista.tipo_dato:
            if self.lista.tipo_dato == bool:
                if texto.lower() in ['true', 'false']:
                    return texto.lower() == 'true'
                raise ValueError("Para booleanos use 'true' o 'false'")
            return self.lista.tipo_dato(texto)

        try:
            return int(texto)
        except:
            pass
        try:
            return float(texto)
        except:
            pass
        if texto.lower() in ['true', 'false']:
            return texto.lower() == 'true'
        return texto

    def insertar(self, posicion):
        texto = self.input_valor.text()
        try:
            valor = self.convertir_valor(texto)
            if posicion == "inicio":
                self.lista.insertar_inicio(valor)
            else:
                self.lista.insertar_final(valor)

            self.animar_insercion(posicion)
            self.actualizar_vista()
            self.input_valor.clear()
        except Exception as e:
            self.mostrar_error("Error de Inserción", str(e))

    def animar_insercion(self, posicion):
        nodo = self.lista.cabeza if posicion == "inicio" else self.lista.cola
        widget = self.crear_nodo_widget(nodo)
        widget.setGraphicsEffect(self.crear_sombra())

        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(800)
        anim.setEasingCurve(QEasingCurve.OutBack)
        anim.setStartValue(QPoint(-100, 0) if posicion == "inicio" else QPoint(100, 0))
        anim.setEndValue(QPoint(0, 0))

        self.animations.addAnimation(anim)
        self.animations.start()

    def eliminar(self, posicion):
        if self.lista.esta_vacia():
            self.mostrar_error("Lista Vacía", "No hay elementos para eliminar")
            return
        try:
            valor = self.lista.eliminar_inicio() if posicion == "inicio" else self.lista.eliminar_final()
            self.animar_eliminacion(posicion)
            self.actualizar_vista()
            self.mostrar_mensaje("Éxito", f"Valor eliminado: {valor}")
        except Exception as e:
            self.mostrar_error("Error de Eliminación", str(e))

    def animar_eliminacion(self, posicion):
        index = 0 if posicion == "inicio" else self.lista_layout.count() - 1
        widget = self.lista_layout.itemAt(index).widget()

        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(800)
        anim.setEasingCurve(QEasingCurve.InBack)
        anim.setEndValue(QPoint(-200 if posicion == "inicio" else 200, 0))
        anim.finished.connect(widget.deleteLater)
        anim.start()

    def buscar_valor(self):
        texto = self.input_valor.text().strip()
        if not texto:
            self.mostrar_error("Campo Vacío", "Ingrese un valor para buscar")
            return
        try:
            valor = self.convertir_valor(texto)
            index = self.lista.buscar(valor)

            if index == -1:
                self.mostrar_mensaje("Búsqueda", "Valor no encontrado")
            else:
                self.mostrar_mensaje("Éxito", f"Valor encontrado en posición {index + 1}")
                self.resaltar_nodo(index)

        except Exception as e:
            self.mostrar_error("Error de Búsqueda", str(e))

    def resaltar_nodo(self, index):
        # Calcula el índice real considerando las flechas entre nodos (cada 2 elementos: nodo + flecha)
        widget_index = index * 2
        if widget_index >= self.lista_layout.count():
            return

        widget_item = self.lista_layout.itemAt(widget_index)
        if not widget_item:
            return

        widget = widget_item.widget()
        widget.setStyleSheet("""
                QFrame#nodo {
                    background-color: #3a405a;
                    border: 3px solid #ff9f1c;
                }
            """)
        if not widget:
            return

        # Animación mejorada
        anim = QPropertyAnimation(widget, b"geometry")
        anim.setDuration(1000)
        original_geo = widget.geometry()

        anim.setKeyValueAt(0, original_geo)
        anim.setKeyValueAt(0.3, original_geo.adjusted(-15, -15, 15, 15))  # Efecto de escala
        anim.setKeyValueAt(0.7, original_geo.adjusted(10, 10, -10, -10))  # Rebote
        anim.setEndValue(original_geo)

        anim.setEasingCurve(QEasingCurve.OutBounce)
        anim.finished.connect(lambda: widget.setStyleSheet(""))
        anim.start()

    def crear_nodo_widget(self, nodo):
        widget = QFrame()
        widget.setObjectName("nodo")
        widget.setStyleSheet("""
            QFrame#nodo {
                background-color: #2d334a;
                border-radius: 15px;
                border: 3px solid #4a5065;
                margin: 15px;
                min-width: 200px;
                min-height: 120px;
            }
        """)
        widget.setFixedSize(220, 140)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        lbl_valor = QLabel(str(nodo.valor))
        lbl_valor.setObjectName("valor")

        lbl_direccion = QLabel(f"0x{id(nodo):x}")
        lbl_direccion.setObjectName("direccion")
        lbl_direccion.setStyleSheet("""
            QLabel#direccion {
                color: #cbd5e1;
                font: 14px 'Consolas';
                qproperty-alignment: AlignCenter;
            }
        """)

        layout.addWidget(lbl_valor)
        layout.addWidget(lbl_direccion)

        widget.setGraphicsEffect(self.crear_sombra())
        return widget

    def crear_sombra(self):
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(25)
        sombra.setXOffset(8)
        sombra.setYOffset(8)
        sombra.setColor(QColor(0, 0, 0, 120))
        return sombra

    def agregar_flecha(self):
        flecha = QLabel()
        node_count = self.lista.tamaño
        size_base = min(max(800 // (node_count + 1), 150), 300)

        pixmap = QPixmap(":/resources/arrow.png")
        if not pixmap.isNull():
            flecha.setPixmap(pixmap.scaled(size_base, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            flecha.setText("→")
        flecha.setStyleSheet("font: bold 40px 'Arial'; color: #4a5065;")

        contenedor = QFrame()
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(flecha)
        layout.addStretch()
        contenedor.setLayout(layout)

        self.lista_layout.addWidget(contenedor)

    def actualizar_vista(self):
        self.limpiar_layout(self.lista_layout)
        actual = self.lista.cabeza
        while actual:
            self.lista_layout.addWidget(self.crear_nodo_widget(actual))
            if actual.siguiente:
                self.agregar_flecha()
            actual = actual.siguiente
        self.lista_layout.addStretch()
        self.actualizar_informacion()
        self.scroll_area.viewport().update()

    def limpiar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def actualizar_informacion(self):
        tipo = self.lista._nombre_tipo() if self.lista.tipo_dato else "No definido"
        cabeza = str(self.lista.cabeza.valor) if self.lista.cabeza else "N/A"
        cola = str(self.lista.cola.valor) if self.lista.cola else "N/A"

        self.ui.lbl_tamaño.setText(f"Tamaño: {self.lista.tamaño}")
        self.ui.lbl_tipo.setText(f"Tipo: {tipo}")
        self.ui.lbl_cabeza.setText(f"Cabeza: {cabeza}")
        self.ui.lbl_cola.setText(f"Cola: {cola}")

    def regresar_al_dashboard(self):
        if self.main_window:
            self.main_window.show()  # Mostrar la ventana principal
            self.close()  # Cerrar esta vista
        else:
            QMessageBox.warning(self, "Advertencia", "No hay referencia al dashboard principal")

    def guardar_lista(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Guardar Lista", "", "JSON Files (*.json)")
        if filename:
            try:
                if not filename.endswith('.json'):
                    filename += '.json'
                self.lista.guardar_a_archivo(filename)
                self.mostrar_mensaje("Éxito", f"Lista guardada en:\n{filename}")
            except Exception as e:
                self.mostrar_error("Error al Guardar", str(e))

    def cargar_lista(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Cargar Lista", "", "JSON Files (*.json)")
        if filename:
            try:
                self.lista = ListaSimple.cargar_desde_archivo(filename)
                self.actualizar_vista()
                self.mostrar_mensaje("Éxito", f"Lista cargada desde:\n{filename}")
            except Exception as e:
                self.mostrar_error("Error al Cargar", str(e))

    def reiniciar_lista(self):
        self.lista.reiniciar()
        self.actualizar_vista()
        self.mostrar_mensaje("Lista Reiniciada", "La lista ha sido vaciada correctamente")

    def mostrar_mensaje(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)
