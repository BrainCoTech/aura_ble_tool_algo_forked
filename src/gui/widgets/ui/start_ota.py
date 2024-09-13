# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'start_ota.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(595, 134)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton_file = QPushButton(Dialog)
        self.pushButton_file.setObjectName(u"pushButton_file")
        self.pushButton_file.setMinimumSize(QSize(0, 30))
        self.pushButton_file.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.pushButton_file)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton_mode_normal = QRadioButton(Dialog)
        self.radioButton_mode_normal.setObjectName(u"radioButton_mode_normal")
        self.radioButton_mode_normal.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_3.addWidget(self.radioButton_mode_normal)

        self.radioButton_mode_force = QRadioButton(Dialog)
        self.radioButton_mode_force.setObjectName(u"radioButton_mode_force")
        self.radioButton_mode_force.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_3.addWidget(self.radioButton_mode_force)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_3)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(Dialog)
        self.pushButton_ok.setObjectName(u"pushButton_ok")
        self.pushButton_ok.setMinimumSize(QSize(0, 30))
        self.pushButton_ok.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.pushButton_ok)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"OTA", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"OTA:", None))
        self.pushButton_file.setText(QCoreApplication.translate("Dialog", u"File", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Mode\uff1a", None))
        self.radioButton_mode_normal.setText(QCoreApplication.translate("Dialog", u"NORMAL ", None))
        self.radioButton_mode_force.setText(QCoreApplication.translate("Dialog", u"FORCE ", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Dialog", u"OK", None))
    # retranslateUi

