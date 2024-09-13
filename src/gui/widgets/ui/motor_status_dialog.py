# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'motor_status_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDialog,
    QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1210, 484)
        Dialog.setStyleSheet(u"font: 11pt")
        self.horizontalLayout_3 = QHBoxLayout(Dialog)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.finger_comboBox = QComboBox(Dialog)
        self.finger_comboBox.setObjectName(u"finger_comboBox")
        self.finger_comboBox.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.finger_comboBox)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.type_comboBox = QComboBox(Dialog)
        self.type_comboBox.setObjectName(u"type_comboBox")
        self.type_comboBox.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.type_comboBox)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label)

        self.spinBox_x_axis_time_s = QSpinBox(Dialog)
        self.spinBox_x_axis_time_s.setObjectName(u"spinBox_x_axis_time_s")
        self.spinBox_x_axis_time_s.setMaximumSize(QSize(300, 16777215))
        self.spinBox_x_axis_time_s.setMinimum(1)
        self.spinBox_x_axis_time_s.setMaximum(120)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.spinBox_x_axis_time_s)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.plot_widget = PlotWidget(Dialog)
        self.plot_widget.setObjectName(u"plot_widget")
        self.plot_widget.setMaximumSize(QSize(16777215, 400))

        self.verticalLayout.addWidget(self.plot_widget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton_freeze = QPushButton(Dialog)
        self.pushButton_freeze.setObjectName(u"pushButton_freeze")

        self.horizontalLayout_2.addWidget(self.pushButton_freeze)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.label_tips = QLabel(Dialog)
        self.label_tips.setObjectName(u"label_tips")

        self.verticalLayout.addWidget(self.label_tips)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 40, -1, -1)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.radioButton_motor_current = QRadioButton(self.groupBox)
        self.radioButton_motor_current.setObjectName(u"radioButton_motor_current")

        self.gridLayout.addWidget(self.radioButton_motor_current, 2, 0, 1, 1)

        self.spinBox_positions_5 = QSpinBox(self.groupBox)
        self.spinBox_positions_5.setObjectName(u"spinBox_positions_5")
        self.spinBox_positions_5.setMinimumSize(QSize(50, 0))
        self.spinBox_positions_5.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_positions_5.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_positions_5, 0, 5, 1, 1)

        self.spinBox_positions_1 = QSpinBox(self.groupBox)
        self.spinBox_positions_1.setObjectName(u"spinBox_positions_1")
        self.spinBox_positions_1.setMinimumSize(QSize(50, 0))
        self.spinBox_positions_1.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_positions_1.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_positions_1, 0, 1, 1, 1)

        self.radioButton_motor_position = QRadioButton(self.groupBox)
        self.radioButton_motor_position.setObjectName(u"radioButton_motor_position")

        self.gridLayout.addWidget(self.radioButton_motor_position, 0, 0, 1, 1)

        self.radioButton_motor_speed = QRadioButton(self.groupBox)
        self.radioButton_motor_speed.setObjectName(u"radioButton_motor_speed")

        self.gridLayout.addWidget(self.radioButton_motor_speed, 1, 0, 1, 1)

        self.spinBox_positions_6 = QSpinBox(self.groupBox)
        self.spinBox_positions_6.setObjectName(u"spinBox_positions_6")
        self.spinBox_positions_6.setMinimumSize(QSize(50, 0))
        self.spinBox_positions_6.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_positions_6.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_positions_6, 0, 6, 1, 1)

        self.spinBox_positions_2 = QSpinBox(self.groupBox)
        self.spinBox_positions_2.setObjectName(u"spinBox_positions_2")
        self.spinBox_positions_2.setMinimumSize(QSize(50, 0))
        self.spinBox_positions_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_positions_2.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_positions_2, 0, 2, 1, 1)

        self.radioButton_motor_pwm = QRadioButton(self.groupBox)
        self.radioButton_motor_pwm.setObjectName(u"radioButton_motor_pwm")

        self.gridLayout.addWidget(self.radioButton_motor_pwm, 3, 0, 1, 1)

        self.spinBox_positions_4 = QSpinBox(self.groupBox)
        self.spinBox_positions_4.setObjectName(u"spinBox_positions_4")
        self.spinBox_positions_4.setMinimumSize(QSize(50, 0))
        self.spinBox_positions_4.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_positions_4.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_positions_4, 0, 4, 1, 1)

        self.spinBox_positions_3 = QSpinBox(self.groupBox)
        self.spinBox_positions_3.setObjectName(u"spinBox_positions_3")
        self.spinBox_positions_3.setMinimumSize(QSize(50, 0))
        self.spinBox_positions_3.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_positions_3.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_positions_3, 0, 3, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setFamilies([u"\u65b0\u5b8b\u4f53"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 4, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 4, 2, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_7, 4, 3, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 4, 4, 1, 1)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_9, 4, 5, 1, 1)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_10, 4, 6, 1, 1)

        self.spinBox_speed_1 = QSpinBox(self.groupBox)
        self.spinBox_speed_1.setObjectName(u"spinBox_speed_1")
        self.spinBox_speed_1.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_speed_1.setMinimum(-100)
        self.spinBox_speed_1.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_speed_1, 1, 1, 1, 1)

        self.spinBox_speed_2 = QSpinBox(self.groupBox)
        self.spinBox_speed_2.setObjectName(u"spinBox_speed_2")
        self.spinBox_speed_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_speed_2.setMinimum(-100)
        self.spinBox_speed_2.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_speed_2, 1, 2, 1, 1)

        self.spinBox_speed_3 = QSpinBox(self.groupBox)
        self.spinBox_speed_3.setObjectName(u"spinBox_speed_3")
        self.spinBox_speed_3.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_speed_3.setMinimum(-100)
        self.spinBox_speed_3.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_speed_3, 1, 3, 1, 1)

        self.spinBox_speed_4 = QSpinBox(self.groupBox)
        self.spinBox_speed_4.setObjectName(u"spinBox_speed_4")
        self.spinBox_speed_4.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_speed_4.setMinimum(-100)
        self.spinBox_speed_4.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_speed_4, 1, 4, 1, 1)

        self.spinBox_speed_5 = QSpinBox(self.groupBox)
        self.spinBox_speed_5.setObjectName(u"spinBox_speed_5")
        self.spinBox_speed_5.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_speed_5.setMinimum(-100)
        self.spinBox_speed_5.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_speed_5, 1, 5, 1, 1)

        self.spinBox_speed_6 = QSpinBox(self.groupBox)
        self.spinBox_speed_6.setObjectName(u"spinBox_speed_6")
        self.spinBox_speed_6.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_speed_6.setMinimum(-100)
        self.spinBox_speed_6.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_speed_6, 1, 6, 1, 1)

        self.spinBox_current_1 = QSpinBox(self.groupBox)
        self.spinBox_current_1.setObjectName(u"spinBox_current_1")
        self.spinBox_current_1.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_current_1.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_current_1, 2, 1, 1, 1)

        self.spinBox_current_2 = QSpinBox(self.groupBox)
        self.spinBox_current_2.setObjectName(u"spinBox_current_2")
        self.spinBox_current_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_current_2.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_current_2, 2, 2, 1, 1)

        self.spinBox_current_3 = QSpinBox(self.groupBox)
        self.spinBox_current_3.setObjectName(u"spinBox_current_3")
        self.spinBox_current_3.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_current_3.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_current_3, 2, 3, 1, 1)

        self.spinBox_current_4 = QSpinBox(self.groupBox)
        self.spinBox_current_4.setObjectName(u"spinBox_current_4")
        self.spinBox_current_4.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_current_4.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_current_4, 2, 4, 1, 1)

        self.spinBox_current_5 = QSpinBox(self.groupBox)
        self.spinBox_current_5.setObjectName(u"spinBox_current_5")
        self.spinBox_current_5.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_current_5.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_current_5, 2, 5, 1, 1)

        self.spinBox_current_6 = QSpinBox(self.groupBox)
        self.spinBox_current_6.setObjectName(u"spinBox_current_6")
        self.spinBox_current_6.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_current_6.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_current_6, 2, 6, 1, 1)

        self.spinBox_pwm_1 = QSpinBox(self.groupBox)
        self.spinBox_pwm_1.setObjectName(u"spinBox_pwm_1")
        self.spinBox_pwm_1.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_pwm_1.setMinimum(-100)
        self.spinBox_pwm_1.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_pwm_1, 3, 1, 1, 1)

        self.spinBox_pwm_2 = QSpinBox(self.groupBox)
        self.spinBox_pwm_2.setObjectName(u"spinBox_pwm_2")
        self.spinBox_pwm_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_pwm_2.setMinimum(-100)
        self.spinBox_pwm_2.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_pwm_2, 3, 2, 1, 1)

        self.spinBox_pwm_3 = QSpinBox(self.groupBox)
        self.spinBox_pwm_3.setObjectName(u"spinBox_pwm_3")
        self.spinBox_pwm_3.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_pwm_3.setMinimum(-100)
        self.spinBox_pwm_3.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_pwm_3, 3, 3, 1, 1)

        self.spinBox_pwm_4 = QSpinBox(self.groupBox)
        self.spinBox_pwm_4.setObjectName(u"spinBox_pwm_4")
        self.spinBox_pwm_4.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_pwm_4.setMinimum(-100)
        self.spinBox_pwm_4.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_pwm_4, 3, 4, 1, 1)

        self.spinBox_pwm_5 = QSpinBox(self.groupBox)
        self.spinBox_pwm_5.setObjectName(u"spinBox_pwm_5")
        self.spinBox_pwm_5.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_pwm_5.setMinimum(-100)
        self.spinBox_pwm_5.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_pwm_5, 3, 5, 1, 1)

        self.spinBox_pwm_6 = QSpinBox(self.groupBox)
        self.spinBox_pwm_6.setObjectName(u"spinBox_pwm_6")
        self.spinBox_pwm_6.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_pwm_6.setMinimum(-100)
        self.spinBox_pwm_6.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox_pwm_6, 3, 6, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_apply = QPushButton(self.groupBox)
        self.pushButton_apply.setObjectName(u"pushButton_apply")

        self.horizontalLayout.addWidget(self.pushButton_apply)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 226, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addWidget(self.groupBox)

        self.horizontalLayout_3.setStretch(0, 1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Motor Status", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Finger", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Type", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"X Axis Range Time_s", None))
        self.pushButton_freeze.setText(QCoreApplication.translate("Dialog", u"Freeze", None))
        self.label_tips.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Motor Control", None))
        self.radioButton_motor_current.setText(QCoreApplication.translate("Dialog", u"currents", None))
        self.radioButton_motor_position.setText(QCoreApplication.translate("Dialog", u"positions", None))
        self.radioButton_motor_speed.setText(QCoreApplication.translate("Dialog", u"speeds", None))
        self.radioButton_motor_pwm.setText(QCoreApplication.translate("Dialog", u"pwms", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Thumb<br/>Ad/Ab</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Thumb<br/>FI/Ex</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Index<br/>FI/Ex</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Middle<br/>FI/Ex</span></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Ring<br/>FI/Ex</span></p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Pinky<br/>FI/Ex</span></p></body></html>", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
    # retranslateUi

