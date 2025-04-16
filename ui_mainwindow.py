# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(958, 678)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush1)
        brush2 = QBrush(QColor(127, 127, 127, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush2)
        brush3 = QBrush(QColor(170, 170, 170, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, brush3)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush1)
        brush4 = QBrush(QColor(255, 255, 220, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, brush4)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, brush)
        brush5 = QBrush(QColor(0, 0, 0, 127))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush5)
#endif
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Accent, brush1)
#endif
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, brush3)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, brush4)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush5)
#endif
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Accent, brush1)
#endif
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, brush)
        brush6 = QBrush(QColor(127, 127, 127, 127))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush6)
#endif
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Accent, brush1)
#endif
        MainWindow.setPalette(palette)
        MainWindow.setStyleSheet(u"background-color: white;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.labelLogo = QLabel(self.centralwidget)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setPixmap(QPixmap(u"resources/logo.png"))
        self.labelLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mainLayout.addWidget(self.labelLogo)

        self.labelTitulo = QLabel(self.centralwidget)
        self.labelTitulo.setObjectName(u"labelTitulo")
        self.labelTitulo.setStyleSheet(u"font-size: 25px; font-weight: bold; color: #2e3e97")
        self.labelTitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mainLayout.addWidget(self.labelTitulo)

        self.gridLayoutBotones = QGridLayout()
        self.gridLayoutBotones.setObjectName(u"gridLayoutBotones")
        self.btnListaSimple = QPushButton(self.centralwidget)
        self.btnListaSimple.setObjectName(u"btnListaSimple")
        self.btnListaSimple.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_default.png);\n"
"    background-color: transparent;\n"
"	font-weight: bold;\n"
"	font-size: 20px\n"
"}\n"
"QPushButton:hover {\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_hover.png);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_default.png);\n"
"}\n"
"")

        self.gridLayoutBotones.addWidget(self.btnListaSimple, 0, 1, 1, 1)

        self.btnArbolBinario = QPushButton(self.centralwidget)
        self.btnArbolBinario.setObjectName(u"btnArbolBinario")
        self.btnArbolBinario.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_default.png);\n"
"    background-color: transparent;\n"
"	font-weight: bold;\n"
"	font-size: 20px\n"
"}\n"
"QPushButton:hover {\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_hover.png);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_default.png);\n"
"}\n"
"")

        self.gridLayoutBotones.addWidget(self.btnArbolBinario, 2, 0, 1, 1)

        self.btnListaCircular = QPushButton(self.centralwidget)
        self.btnListaCircular.setObjectName(u"btnListaCircular")
        self.btnListaCircular.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_default.png);\n"
"    background-color: transparent;\n"
"	font-weight: bold;\n"
"	font-size: 20px\n"
"}\n"
"QPushButton:hover {\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_hover.png);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_default.png);\n"
"}\n"
"")

        self.gridLayoutBotones.addWidget(self.btnListaCircular, 1, 1, 1, 1)

        self.btnPila = QPushButton(self.centralwidget)
        self.btnPila.setObjectName(u"btnPila")
        self.btnPila.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_default.png);\n"
"    background-color: transparent;\n"
"	font-weight: bold;\n"
"	font-size: 20px\n"
"}\n"
"QPushButton:hover {\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_hover.png);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_default.png);\n"
"}\n"
"\n"
"\n"
"")

        self.gridLayoutBotones.addWidget(self.btnPila, 0, 0, 1, 1)

        self.btnArbolBusqueda = QPushButton(self.centralwidget)
        self.btnArbolBusqueda.setObjectName(u"btnArbolBusqueda")
        self.btnArbolBusqueda.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_default.png);\n"
"    background-color: transparent;\n"
"	font-weight: bold;\n"
"	font-size: 20px\n"
"}\n"
"QPushButton:hover {\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_hover.png);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_default.png);\n"
"}\n"
"")

        self.gridLayoutBotones.addWidget(self.btnArbolBusqueda, 2, 1, 1, 1)

        self.btnListaDoble = QPushButton(self.centralwidget)
        self.btnListaDoble.setObjectName(u"btnListaDoble")
        self.btnListaDoble.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_default.png);\n"
"    background-color: transparent;\n"
"	font-weight: bold;\n"
"	font-size: 20px\n"
"}\n"
"QPushButton:hover {\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_hover.png);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-image: url(/Users/derekmorales/DEREK-PROJECTS/DSV/DataVisualizer/resources/button_default.png);\n"
"}\n"
"")

        self.gridLayoutBotones.addWidget(self.btnListaDoble, 1, 0, 1, 1)


        self.mainLayout.addLayout(self.gridLayoutBotones)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Visualizer de Estructuras de Datos", None))
        self.labelTitulo.setText(QCoreApplication.translate("MainWindow", u"Selecciona una estructura de datos", None))
        self.btnListaSimple.setText(QCoreApplication.translate("MainWindow", u"Lista Simple", None))
        self.btnArbolBinario.setText(QCoreApplication.translate("MainWindow", u"\u00c1rbol Binario", None))
        self.btnListaCircular.setText(QCoreApplication.translate("MainWindow", u"Lista Circular", None))
        self.btnPila.setText(QCoreApplication.translate("MainWindow", u"Pila", None))
        self.btnArbolBusqueda.setText(QCoreApplication.translate("MainWindow", u"\u00c1rbol de B\u00fasqueda", None))
        self.btnListaDoble.setText(QCoreApplication.translate("MainWindow", u"Lista Doble", None))
    # retranslateUi

