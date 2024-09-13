# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'protol_config_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(488, 701)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_import = QPushButton(Form)
        self.pushButton_import.setObjectName(u"pushButton_import")
        self.pushButton_import.setMinimumSize(QSize(32, 32))
        self.pushButton_import.setMaximumSize(QSize(32, 32))
        self.pushButton_import.setIconSize(QSize(28, 28))

        self.horizontalLayout.addWidget(self.pushButton_import)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_text = QVBoxLayout()
        self.verticalLayout_text.setObjectName(u"verticalLayout_text")

        self.verticalLayout.addLayout(self.verticalLayout_text)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton_get = QPushButton(Form)
        self.pushButton_get.setObjectName(u"pushButton_get")
        self.pushButton_get.setMinimumSize(QSize(32, 32))
        self.pushButton_get.setMaximumSize(QSize(32, 32))
        self.pushButton_get.setIconSize(QSize(28, 28))

        self.horizontalLayout_2.addWidget(self.pushButton_get)

        self.pushButton_set = QPushButton(Form)
        self.pushButton_set.setObjectName(u"pushButton_set")
        self.pushButton_set.setMinimumSize(QSize(32, 32))
        self.pushButton_set.setMaximumSize(QSize(32, 32))
        self.pushButton_set.setIconSize(QSize(28, 28))

        self.horizontalLayout_2.addWidget(self.pushButton_set)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_import.setText("")
        self.pushButton_get.setText("")
        self.pushButton_set.setText("")
    # retranslateUi

