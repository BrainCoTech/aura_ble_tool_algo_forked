# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'download_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(415, 170)
        Dialog.setStyleSheet(u"* {\n"
"	font: 13pt;\n"
"}")
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stop_pushbutton = QPushButton(Dialog)
        self.stop_pushbutton.setObjectName(u"stop_pushbutton")

        self.gridLayout.addWidget(self.stop_pushbutton, 4, 2, 1, 1)

        self.progressBar = QProgressBar(Dialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 4)

        self.start_pushbutton = QPushButton(Dialog)
        self.start_pushbutton.setObjectName(u"start_pushbutton")

        self.gridLayout.addWidget(self.start_pushbutton, 4, 1, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 4)

        self.horizontalSpacer = QSpacerItem(90, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 4, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(89, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 4, 3, 1, 1)

        self.label_info = QLabel(Dialog)
        self.label_info.setObjectName(u"label_info")

        self.gridLayout.addWidget(self.label_info, 0, 0, 1, 4)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Download Model", None))
        self.stop_pushbutton.setText(QCoreApplication.translate("Dialog", u"cancel", None))
        self.start_pushbutton.setText(QCoreApplication.translate("Dialog", u"start", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Downloading...", None))
        self.label_info.setText("")
    # retranslateUi

