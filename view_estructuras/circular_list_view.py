from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QPointF, QRectF, QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QLabel, QScrollArea, QHBoxLayout, QVBoxLayout, QSizePolicy, QFileDialog, \
    QMessageBox
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QPixmap, QFont
from PySide6.QtWidgets import QPushButton
from estructuras.circular_linked_list import ListaCircular
from view_estructuras.singly_linked_list_view import ListaSimpleView


class CurvedArrowWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(180, 60)
        self.color = QColor("#4a5065")
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(self.color, 3, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)

        # Dibujar curva Bézier ajustada
        path = QPainterPath()
        path.moveTo(10, 30)
        path.cubicTo(60, -20, 120, 80, 170, 30)
        painter.drawPath(path)

        # Punta de flecha
        painter.drawLine(160, 25, 170, 30)
        painter.drawLine(160, 35, 170, 30)


class ListaCircularView(ListaSimpleView):
    def __init__(self, main_window=None):
        super().__init__(main_window)
        # Configurar política de tamaño
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Forzar tamaño inicial
        self.resize(1280, 720)
        # Añadir esto en inicializar_ui()
        self.scroll_area.setWidgetResizable(True)
        self.lista = ListaCircular()
        self.anim_rotacion_group = QParallelAnimationGroup()

        # Configurar ventana completa
        self.setWindowState(Qt.WindowMaximized)

        # Conectar botones de rotación
        self.btn_rotar_izquierda = self.ui.findChild(QPushButton, "btn_rotar_izquierda")
        self.btn_rotar_derecha = self.ui.findChild(QPushButton, "btn_rotar_derecha")
        self.btn_rotar_izquierda.clicked.connect(self.rotar_izquierda)
        self.btn_rotar_derecha.clicked.connect(self.rotar_derecha)

        # Ajustar estilos específicos
        self.configurar_estilos_circulares()

    def configurar_estilos_circulares(self):
        self.ui.label_title.setText("LISTA CIRCULAR")
        self.ui.label_title.setStyleSheet("""
            font: 700 28pt "Segoe UI";
            color: #ffffff;
            background-color: #4a5065;
            padding: 15px 40px;
            border-radius: 20px;
            border: 3px solid #8d99ae;
        """)

    def inicializar_ui(self):
        try:
            loader = QUiLoader()
            ui_file = QFile("estructuras_ui/circular_linked_list_view.ui")  # Asegúrate de la ruta
            if not ui_file.open(QFile.ReadOnly):
                raise FileNotFoundError(f"Archivo UI no encontrado: {ui_file.fileName()}")

            self.ui = loader.load(ui_file, self)
            ui_file.close()

            if not self.ui:
                raise RuntimeError("Error al cargar el archivo UI")

            # ... resto del código ...
        except Exception as e:
            QMessageBox.critical(None, "Error UI", f"Error crítico:\n{str(e)}")
            raise

    def conectar_eventos(self):
        super().conectar_eventos()
        # Reconectar botones heredados con métodos sobreescritos
        self.ui.btn_reiniciar.clicked.disconnect()
        self.ui.btn_reiniciar.clicked.connect(self.reiniciar_lista)
        self.ui.btn_buscar.clicked.disconnect()
        self.ui.btn_buscar.clicked.connect(self.buscar_valor)

    def actualizar_vista(self):
        self.limpiar_layout(self.lista_layout)

        if self.lista.esta_vacia():
            self.actualizar_informacion()
            return

        # Crear todos los nodos primero
        nodos = []
        actual = self.lista.cabeza
        for _ in range(self.lista.tamaño):
            nodo_widget = self.crear_nodo_widget(actual)
            nodos.append(nodo_widget)
            actual = actual.siguiente

        # Añadir al layout con flechas
        for i, widget in enumerate(nodos):
            self.lista_layout.addWidget(widget)
            if i < len(nodos) - 1:
                self.agregar_flecha()

        # Flecha circular final
        if len(nodos) > 1:
            self.agregar_flecha_circular()

        self.lista_layout.addStretch()
        self.ajustar_scroll()

    def agregar_flecha_circular(self):
        container = QWidget()
        container.setLayout(QVBoxLayout())
        container.layout().setContentsMargins(0, 20, 0, 0)  # Margen superior

        flecha = CurvedArrowWidget()
        flecha.setFixedSize(180, 60)

        container.layout().addWidget(flecha)
        self.lista_layout.addWidget(container)

    def animar_flecha_circular(self):
        if self.current_arrow:
            anim = QPropertyAnimation(self.current_arrow, b"control_point_offset")
            anim.setDuration(2000)
            anim.setStartValue(80)
            anim.setEndValue(120)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            anim.setLoopCount(-1)
            anim.start()

    def rotar_izquierda(self):
        if self.lista.tamaño > 1:
            self.lista.rotar_izquierda()
            self.animar_rotacion("izquierda")
            self.actualizar_vista()

    def rotar_derecha(self):
        if self.lista.tamaño > 1:
            self.lista.rotar_derecha()
            self.animar_rotacion("derecha")
            self.actualizar_vista()

    def animar_rotacion(self, direccion):
        self.anim_rotacion_group.stop()
        self.anim_rotacion_group = QParallelAnimationGroup()

        # Obtener todos los widgets de nodo
        widgets = []
        for i in range(self.lista_layout.count()):
            item = self.lista_layout.itemAt(i)
            if item and item.widget() and item.widget().objectName() == "nodo":
                widgets.append(item.widget())

        # Calcular nuevas posiciones
        new_positions = [QPoint(widget.x() + (200 if direccion == "izquierda" else -200), widget.y())
                         for widget in widgets]

        # Animación
        for widget, new_pos in zip(widgets, new_positions):
            anim = QPropertyAnimation(widget, b"pos")
            anim.setDuration(800)
            anim.setEasingCurve(QEasingCurve.OutBack)
            anim.setEndValue(new_pos)
            self.anim_rotacion_group.addAnimation(anim)

        self.anim_rotacion_group.start()

    def ajustar_scroll(self):
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.widget().adjustSize()

    def reiniciar_lista(self):
        self.lista.reiniciar()
        self.actualizar_vista()
        QMessageBox.information(self, "Lista Reiniciada", "La lista circular ha sido vaciada")

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
        # Ajustar índice para layout con flechas
        widget_index = index * 2  # Cada nodo + flecha
        if widget_index >= self.lista_layout.count():
            return

        widget_item = self.lista_layout.itemAt(widget_index)
        if widget_item and widget_item.widget():
            widget = widget_item.widget()
            self.aplicar_animacion_resaltado(widget)

    def aplicar_animacion_resaltado(self, widget):
        anim = QPropertyAnimation(widget, b"geometry")
        anim.setDuration(1000)
        original_geo = widget.geometry()

        anim.setKeyValueAt(0, original_geo)
        anim.setKeyValueAt(0.3, original_geo.adjusted(-10, -10, 10, 10))
        anim.setKeyValueAt(0.7, original_geo.adjusted(5, 5, -5, -5))
        anim.setEndValue(original_geo)

        anim.setEasingCurve(QEasingCurve.OutBounce)
        anim.start()

    def guardar_lista(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Guardar Lista Circular", "", "JSON Files (*.json)")
        if filename:
            try:
                if not filename.endswith('.json'):
                    filename += '.json'
                self.lista.guardar_a_archivo(filename)
                self.mostrar_mensaje("Éxito", f"Lista circular guardada en:\n{filename}")
            except Exception as e:
                self.mostrar_error("Error al Guardar", str(e))

    def cargar_lista(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Cargar Lista Circular", "", "JSON Files (*.json)")
        if filename:
            try:
                self.lista = ListaCircular.cargar_desde_archivo(filename)
                self.actualizar_vista()
                self.mostrar_mensaje("Éxito", f"Lista circular cargada desde:\n{filename}")
            except Exception as e:
                self.mostrar_error("Error al Cargar", str(e))

    def ajustar_tamano_scroll(self):
        self.scroll_area.viewport().update()
        self.scroll_area.ensureVisible(0, 0)

    def limpiar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                if isinstance(widget, CurvedArrowWidget):
                    widget.deleteLater()
                else:
                    super().limpiar_layout(widget.layout()) if widget.layout() else None
                    widget.deleteLater()
            del item