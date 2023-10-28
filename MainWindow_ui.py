# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QHBoxLayout, QLabel,
    QMainWindow, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from pyqtgraph.opengl import GLViewWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1068, 794)
        MainWindow.setMinimumSize(QSize(500, 500))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.plotWidget = GLViewWidget(self.centralwidget)
        self.plotWidget.setObjectName(u"plotWidget")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy)
        self.plotWidget.setMinimumSize(QSize(500, 500))

        self.horizontalLayout.addWidget(self.plotWidget)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.rotXBox = QDoubleSpinBox(self.centralwidget)
        self.rotXBox.setObjectName(u"rotXBox")
        self.rotXBox.setDecimals(1)
        self.rotXBox.setMinimum(-180.000000000000000)
        self.rotXBox.setMaximum(180.000000000000000)

        self.verticalLayout.addWidget(self.rotXBox)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.rotYBox = QDoubleSpinBox(self.centralwidget)
        self.rotYBox.setObjectName(u"rotYBox")
        self.rotYBox.setDecimals(1)
        self.rotYBox.setMinimum(-180.000000000000000)
        self.rotYBox.setMaximum(180.000000000000000)

        self.verticalLayout.addWidget(self.rotYBox)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.rotZBox = QDoubleSpinBox(self.centralwidget)
        self.rotZBox.setObjectName(u"rotZBox")
        self.rotZBox.setDecimals(1)
        self.rotZBox.setMinimum(-180.000000000000000)
        self.rotZBox.setMaximum(180.000000000000000)

        self.verticalLayout.addWidget(self.rotZBox)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.tlXBox = QDoubleSpinBox(self.centralwidget)
        self.tlXBox.setObjectName(u"tlXBox")
        self.tlXBox.setDecimals(0)
        self.tlXBox.setMinimum(-1000.000000000000000)
        self.tlXBox.setMaximum(1000.000000000000000)

        self.verticalLayout.addWidget(self.tlXBox)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.tlYBox = QDoubleSpinBox(self.centralwidget)
        self.tlYBox.setObjectName(u"tlYBox")
        self.tlYBox.setDecimals(0)
        self.tlYBox.setMinimum(-1000.000000000000000)
        self.tlYBox.setMaximum(1000.000000000000000)

        self.verticalLayout.addWidget(self.tlYBox)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout.addWidget(self.label_6)

        self.tlZBox = QDoubleSpinBox(self.centralwidget)
        self.tlZBox.setObjectName(u"tlZBox")
        self.tlZBox.setDecimals(0)
        self.tlZBox.setMinimum(-1000.000000000000000)
        self.tlZBox.setMaximum(1000.000000000000000)

        self.verticalLayout.addWidget(self.tlZBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Rotate X", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Rotate Y", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Rotate Z", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Move X", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Move Y", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Move Z", None))
    # retranslateUi

