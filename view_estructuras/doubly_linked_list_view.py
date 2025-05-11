
from PySide6.QtCore import Qt, QFile, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QPoint, QSize
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QScrollArea,
    QHBoxLayout, QVBoxLayout, QMessageBox, QFileDialog, QFrame,
    QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem, QApplication
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QFont, QColor, QPixmap, QFontDatabase, QTransform
from estructuras.doubly_linked_list import ListaDoble
import resources_rc


class ListaDobleView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        print("Flecha cargada:", QPixmap(":/resources/twoside_arrow.png").isNull())
        self.setStyleSheet("background-color: #ffffff;")  # Agregar en inicializar_ui()
        self.lista = ListaDoble()
        self.animations = QParallelAnimationGroup()

        self.ui = None
        self.scroll_area = None
        self.lista_layout = None
        self.input_valor = None
        self.input_posicion = None

        self.inicializar_ui()
        self.inicializar_componentes()
        self.conectar_eventos()
        self.configurar_estilos()

    def inicializar_ui(self):
        try:
            loader = QUiLoader()
            ui_file = QFile("estructuras_ui/doubly_linked_list_view.ui")
            if not ui_file.open(QFile.ReadOnly):
                raise FileNotFoundError(f"Archivo UI no encontrado: {ui_file.fileName()}")

            self.ui = loader.load(ui_file, self)
            ui_file.close()
            self.setStyleSheet("background-color: #ffffff;")  # Agregar en inicializar_ui()

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
        self.scroll_area = self.ui.findChild(QScrollArea, "scrollArea")
        contenedor = self.scroll_area.findChild(QWidget, "contenedorLista")

        if contenedor is None:
            raise RuntimeError("Asegúrate de que el QScrollArea contenga un QWidget llamado 'contenedorLista'")

        if not contenedor.layout():
            contenedor.setLayout(QHBoxLayout())

        self.lista_layout = contenedor.layout()
        self.input_valor = self.ui.findChild(QLineEdit, "input_valor")
        self.input_posicion = self.ui.findChild(QLineEdit, "input_posicion")

    def configurar_estilos(self):
        self.setStyleSheet("background-color: #ffffff;")  # Agregar en inicializar_ui()

        self.setStyleSheet("""
            QFrame#nodo {
                background-color: #3a0ca3 !important;
                border-radius: 15px !important;
                border: 3px solid #7209b7 !important;
            }

            QLabel {
                background: transparent !important;
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
            self.ui.btn_insertar_pos.clicked.connect(lambda: self.insertar("posicion"))
            self.ui.btn_eliminar_inicio.clicked.connect(lambda: self.eliminar("inicio"))
            self.ui.btn_eliminar_final.clicked.connect(lambda: self.eliminar("final"))
            self.ui.btn_eliminar_pos.clicked.connect(lambda: self.eliminar("posicion"))
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

    def obtener_posicion(self):
        texto = self.input_posicion.text().strip()
        if not texto:
            raise ValueError("Ingrese una posición válida")

        try:
            pos = int(texto)
            if pos < 1 or pos > self.lista.tamaño + 1:
                raise ValueError(f"Posición debe estar entre 1 y {self.lista.tamaño + 1}")
            return pos - 1  # Convertir a índice base 0
        except ValueError:
            raise ValueError("La posición debe ser un número entero válido")

    def crear_conexion_widget(self, tipo, nodo=None):
        frame = QFrame()
        frame.setFixedSize(60, 120)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if tipo in ["HEAD", "TAIL"]:
            # Configurar HEAD/TAIL sin flechas
            label = QLabel(tipo)
            label.setStyleSheet("""
                   font: bold 14pt 'Segoe UI';
                   color: #2b2d42;
                   background-color: #edf2f4;
                   padding: 8px;
                   border-radius: 8px;
               """)
            layout.addWidget(label)
        else:
            # Flecha bidireccional centrada
            label_arrow = QLabel()
            pixmap = QPixmap(":/resources/twoside_arrow.png")
            label_arrow.setPixmap(pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label_arrow.setAlignment(Qt.AlignCenter)
            layout.addWidget(label_arrow)

            # Dirección de memoria con fondo
            if nodo:
                dir_label = QLabel(f"0x{id(nodo):x}")
                dir_label.setStyleSheet("""
                       font: 10px 'Consolas';
                       color: #ffffff;
                       background-color: #4a4e69;
                       padding: 4px;
                       border-radius: 4px;
                       margin: 4px 0;
                   """)
                layout.addWidget(dir_label, alignment=Qt.AlignCenter)

        return frame

    def crear_nodo_widget(self, nodo):
        main_frame = QFrame()
        main_frame.setStyleSheet("background: transparent;")
        main_layout = QHBoxLayout(main_frame)
        main_layout.setContentsMargins(0, 30, 0, 30)  # Espacio vertical para flechas
        main_layout.setSpacing(0)

        # Conexión izquierda (solo flecha si hay nodo anterior)
        if nodo.anterior:
            main_layout.addWidget(self.crear_conexion_widget("prev", nodo.anterior))

        # Nodo principal
        nodo_frame = QFrame()
        nodo_frame.setStyleSheet("""
               background-color: #3a0ca3;
               border-radius: 15px;
               border: 3px solid #7209b7;
               margin: 0 10px;
           """)
        nodo_frame.setFixedSize(140, 80)  # Tamaño más compacto

        layout_nodo = QVBoxLayout(nodo_frame)
        valor_label = QLabel(str(nodo.valor))
        valor_label.setStyleSheet("""
               color: #ffffff;
               font: bold 20px 'Segoe UI';
               qproperty-alignment: AlignCenter;
           """)
        layout_nodo.addWidget(valor_label)

        main_layout.addWidget(nodo_frame)

        # Conexión derecha (solo flecha si hay nodo siguiente)
        if nodo.siguiente:
            main_layout.addWidget(self.crear_conexion_widget("next", nodo))

        return main_frame

    def actualizar_vista(self):
        self.limpiar_layout(self.lista_layout)
        self.lista_layout.addWidget(self.crear_conexion_widget("HEAD"))  # HEAD

        actual = self.lista.cabeza
        while actual:
            self.lista_layout.addWidget(self.crear_nodo_widget(actual))
            actual = actual.siguiente

        self.lista_layout.addWidget(self.crear_conexion_widget("TAIL"))  # TAIL
        self.actualizar_informacion()

    def limpiar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def insertar(self, posicion):
        texto = self.input_valor.text()
        try:
            valor = self.convertir_valor(texto)
            pos = None

            if posicion == "inicio":
                self.lista.insertar_inicio(valor)
            elif posicion == "final":
                self.lista.insertar_final(valor)
            else:
                pos = self.obtener_posicion()
                self.lista.insertar_en_posicion(pos, valor)

            self.animar_insercion(posicion, pos)
            self.actualizar_vista()
            self.input_valor.clear()
            self.input_posicion.clear()
        except Exception as e:
            self.mostrar_error("Error de Inserción", str(e))

    def animar_insercion(self, posicion, pos=None):
        if posicion == "inicio":
            nodo = self.lista.cabeza
        elif posicion == "final":
            nodo = self.lista.cola
        else:
            nodo = self.lista.obtener_nodo(pos)

        widget = self.crear_nodo_widget(nodo)
        widget.setGraphicsEffect(self.crear_sombra())

        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(800)
        anim.setEasingCurve(QEasingCurve.OutBack)

        if posicion == "inicio":
            anim.setStartValue(QPoint(-200, 0))
        elif posicion == "final":
            anim.setStartValue(QPoint(200, 0))
        else:
            anim.setStartValue(QPoint(0, -100))

        anim.setEndValue(QPoint(0, 0))

        self.animations.addAnimation(anim)
        self.animations.start()

    def eliminar(self, posicion):
        if self.lista.esta_vacia():
            self.mostrar_error("Lista Vacía", "No hay elementos para eliminar")
            return
        try:
            if posicion == "inicio":
                valor = self.lista.eliminar_inicio()
            elif posicion == "final":
                valor = self.lista.eliminar_final()
            else:
                pos = self.obtener_posicion()
                valor = self.lista.eliminar_en_posicion(pos)

            self.animar_eliminacion(posicion)
            self.actualizar_vista()
            self.mostrar_mensaje("Éxito", f"Valor eliminado: {valor}")
            self.input_posicion.clear()
        except Exception as e:
            self.mostrar_error("Error de Eliminación", str(e))

    def animar_eliminacion(self, posicion):
        if posicion == "inicio":
            index = 1  # Saltar el HEAD
        elif posicion == "final":
            index = self.lista_layout.count() - 2  # Saltar el TAIL
        else:
            index = posicion * 2 + 1  # Considerando HEAD y conexiones

        widget = self.lista_layout.itemAt(index).widget()

        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(800)
        anim.setEasingCurve(QEasingCurve.InBack)
        anim.setEndValue(QPoint(-300 if posicion == "inicio" else 300, 0))
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
        # Cada nodo ocupa 1 posición (HEAD + nodos + TAIL)
        widget_index = index * 1 + 1  # +1 para saltar el HEAD
        if widget_index >= self.lista_layout.count() - 1:  # -1 para saltar el TAIL
            return

        widget_item = self.lista_layout.itemAt(widget_index)
        if not widget_item:
            return

        widget = widget_item.widget()
        if not widget:
            return

        # Encontrar el frame del nodo dentro del widget
        nodo_frame = widget.findChild(QFrame, "nodo")
        if not nodo_frame:
            return

        # Efecto de resaltado mejorado
        nodo_frame.setStyleSheet("""
            QFrame#nodo {
                background-color: #7209b7;
                border: 3px solid #f72585;
            }
            QLabel#valor {
                color: #ffffff;
                font: bold 28px 'Segoe UI';
            }
        """)

        # Animación
        anim_group = QParallelAnimationGroup()

        # Animación de escala
        anim_scale = QPropertyAnimation(nodo_frame, b"geometry")
        anim_scale.setDuration(1000)
        original_geo = nodo_frame.geometry()
        anim_scale.setKeyValueAt(0, original_geo)
        anim_scale.setKeyValueAt(0.3, original_geo.adjusted(-15, -15, 15, 15))
        anim_scale.setKeyValueAt(0.7, original_geo.adjusted(10, 10, -10, -10))
        anim_scale.setEndValue(original_geo)
        anim_scale.setEasingCurve(QEasingCurve.OutBounce)

        # Animación de color
        anim_color = QPropertyAnimation(nodo_frame, b"styleSheet")
        anim_color.setDuration(1000)
        anim_color.setStartValue("""
            QFrame#nodo {
                background-color: #f72585;
                border: 3px solid #7209b7;
            }
        """)
        anim_color.setEndValue("""
            QFrame#nodo {
                background-color: #7209b7;
                border: 3px solid #f72585;
            }
        """)
        anim_color.setLoopCount(2)

        anim_group.addAnimation(anim_scale)
        anim_group.addAnimation(anim_color)
        anim_group.start()

        # Restaurar estilo al finalizar
        anim_group.finished.connect(lambda: nodo_frame.setStyleSheet("""
            QFrame#nodo {
                background-color: #3a0ca3;
                border: 3px solid #7209b7;
            }
        """))

    def crear_sombra(self):
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(25)
        sombra.setXOffset(8)
        sombra.setYOffset(8)
        sombra.setColor(QColor(0, 0, 0, 120))
        return sombra

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
            self.main_window.show()
            self.close()
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
                self.lista = ListaDoble.cargar_desde_archivo(filename)
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