# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pid_debug_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QDoubleSpinBox, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(808, 633)
        Dialog.setStyleSheet(u"font: 11pt")
        self.gridLayout_3 = QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.ki_SpinBox = QDoubleSpinBox(Dialog)
        self.ki_SpinBox.setObjectName(u"ki_SpinBox")

        self.gridLayout_2.addWidget(self.ki_SpinBox, 0, 3, 1, 1)

        self.send_pid_pushButton = QPushButton(Dialog)
        self.send_pid_pushButton.setObjectName(u"send_pid_pushButton")

        self.gridLayout_2.addWidget(self.send_pid_pushButton, 0, 6, 1, 1)

        self.kp_SpinBox = QDoubleSpinBox(Dialog)
        self.kp_SpinBox.setObjectName(u"kp_SpinBox")

        self.gridLayout_2.addWidget(self.kp_SpinBox, 0, 1, 1, 1)

        self.kd_SpinBox = QDoubleSpinBox(Dialog)
        self.kd_SpinBox.setObjectName(u"kd_SpinBox")

        self.gridLayout_2.addWidget(self.kd_SpinBox, 0, 5, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 4, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)

        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.gridLayout_2.setColumnStretch(5, 1)

        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.finger_comboBox = QComboBox(Dialog)
        self.finger_comboBox.setObjectName(u"finger_comboBox")

        self.gridLayout.addWidget(self.finger_comboBox, 1, 1, 1, 1)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.type_comboBox = QComboBox(Dialog)
        self.type_comboBox.setObjectName(u"type_comboBox")

        self.gridLayout.addWidget(self.type_comboBox, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)

        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.freeze_Button = QPushButton(Dialog)
        self.freeze_Button.setObjectName(u"freeze_Button")

        self.horizontalLayout_2.addWidget(self.freeze_Button)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)

        self.plot_widget = PlotWidget(Dialog)
        self.plot_widget.setObjectName(u"plot_widget")

        self.gridLayout_3.addWidget(self.plot_widget, 3, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pulse_rp_checkBox = QCheckBox(Dialog)
        self.pulse_rp_checkBox.setObjectName(u"pulse_rp_checkBox")

        self.horizontalLayout_3.addWidget(self.pulse_rp_checkBox)

        self.send_rp_pushButton = QPushButton(Dialog)
        self.send_rp_pushButton.setObjectName(u"send_rp_pushButton")

        self.horizontalLayout_3.addWidget(self.send_rp_pushButton)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 4, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.verticalSlider = QSlider(Dialog)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setMinimum(-100)
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setOrientation(Qt.Vertical)
        self.verticalSlider.setTickPosition(QSlider.TicksBothSides)
        self.verticalSlider.setTickInterval(10)

        self.horizontalLayout.addWidget(self.verticalSlider)

        self.slider_value_label = QLabel(Dialog)
        self.slider_value_label.setObjectName(u"slider_value_label")
        self.slider_value_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.slider_value_label)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 1, 4, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"PID Tuner", None))
        self.send_pid_pushButton.setText(QCoreApplication.translate("Dialog", u"send", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Kd", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Kp", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Ki", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Finger", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Type", None))
        self.freeze_Button.setText(QCoreApplication.translate("Dialog", u"Freeze", None))
        self.pulse_rp_checkBox.setText(QCoreApplication.translate("Dialog", u"pulse response", None))
        self.send_rp_pushButton.setText(QCoreApplication.translate("Dialog", u"send", None))
        self.label_6.setText("")
        self.slider_value_label.setText(QCoreApplication.translate("Dialog", u"0", None))
    # retranslateUi

