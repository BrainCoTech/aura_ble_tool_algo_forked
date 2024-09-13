# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ble_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(476, 40)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_scan = QPushButton(Form)
        self.button_scan.setObjectName(u"button_scan")

        self.horizontalLayout.addWidget(self.button_scan)

        self.combobox_devices = QComboBox(Form)
        self.combobox_devices.setObjectName(u"combobox_devices")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.combobox_devices.sizePolicy().hasHeightForWidth())
        self.combobox_devices.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.combobox_devices)

        self.button_connect = QPushButton(Form)
        self.button_connect.setObjectName(u"button_connect")

        self.horizontalLayout.addWidget(self.button_connect)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.gridLayout_device_info = QGridLayout()
        self.gridLayout_device_info.setObjectName(u"gridLayout_device_info")

        self.verticalLayout.addLayout(self.gridLayout_device_info)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.button_scan.setText(QCoreApplication.translate("Form", u"scan", None))
        self.button_connect.setText(QCoreApplication.translate("Form", u"connect", None))
    # retranslateUi

