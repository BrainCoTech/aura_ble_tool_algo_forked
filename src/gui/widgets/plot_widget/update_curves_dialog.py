# -*- coding: utf-8 -*-
from PySide6.QtGui import QColor, QPen, Qt
from PySide6.QtWidgets import QDialog, QFormLayout, QPushButton, QVBoxLayout, QSpinBox, QColorDialog, QTabWidget, \
    QWidget, QLabel


class UpdateCurvesDialog(QDialog):
    def __init__(self, title, curves, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{title}")
        self.resize(300, 100)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.widgets = {}

        tab_widget = QTabWidget()
        self.tips_color_labels = []
        self.tips_width_labels = []
        for curve in curves:
            name = str(curve.name())
            pen = curve.opts['pen']
            if not isinstance(pen, QPen):
                print("创建曲线时, 使用这种语法pen=mkPen(color=QColor(0, 0, 255), width=2)")
                raise TypeError("pen must be QPen")
            color = pen.color()  # PySide6.QtGui.QColor.fromRgbF
            width = pen.width()

            widget = QWidget()
            f_layout = QFormLayout()
            widget.setLayout(f_layout)

            color_button = QPushButton()
            color_button.setFocusPolicy(Qt.NoFocus)
            setattr(color_button, "curve", curve)
            color_button.setStyleSheet(f"background: rgb({color.red()}, {color.green()}, {color.blue()})")

            spx_box = QSpinBox()
            spx_box.setMinimum(1)
            setattr(spx_box, "curve", curve)
            spx_box.setValue(width)
            self.widgets[name] = [color_button, spx_box]
            color_label = QLabel(self.tr("Color"))
            width_label = QLabel(self.tr("Width"))
            self.tips_color_labels.append(color_label)
            self.tips_width_labels.append(width_label)
            f_layout.addRow(color_label, color_button)
            f_layout.addRow(width_label, spx_box)

            tab_widget.addTab(widget, name)

            color_button.clicked.connect(self._change_curve_color)
            spx_box.valueChanged.connect(self._change_curve_width)

        main_layout.addWidget(tab_widget)

    def translate_ui(self):
        self.setWindowTitle(self.tr("Curves"))
        for label in self.tips_color_labels:
            label.setText(self.tr("Color"))
        for label in self.tips_width_labels:
            label.setText(self.tr("Width"))

    def _change_curve_width(self, value):
        sender = self.sender()
        curve = getattr(sender, "curve")
        pen = curve.opts['pen']
        pen.setWidth(value)
        curve.setPen(pen)
        curve.update()

    def _change_curve_color(self):
        sender = self.sender()
        curve = getattr(sender, "curve")
        pen = curve.opts['pen']
        color = QColorDialog.getColor(pen.color())
        if color.isValid():
            pen.setColor(color)
            curve.setPen(pen)
            curve.update()
            sender.setStyleSheet(f"background: rgb({color.red()}, {color.green()}, {color.blue()})")


class UpdateAllCurvesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Curves"))
        self.resize(400, 100)
        self.curves = None

        f_layout = QFormLayout()
        self.setLayout(f_layout)

        self.color_button = QPushButton()
        self.color_button.setFocusPolicy(Qt.NoFocus)
        default_color = QColor(255, 0, 0)
        setattr(self.color_button, "color", default_color)
        self.color_button.setStyleSheet(f"background: rgb({default_color.red()}, {default_color.green()}, {default_color.blue()})")

        spx_box = QSpinBox()
        spx_box.setMinimum(1)
        spx_box.setValue(1)
        self.color_label = QLabel(self.tr("Color"))
        self.width_label = QLabel(self.tr("Width"))
        f_layout.addRow(self.color_label, self.color_button)
        f_layout.addRow(self.width_label, spx_box)

        self.color_button.clicked.connect(self._change_curves_color)
        spx_box.valueChanged.connect(self._change_curves_width)

    def translate_ui(self):
        self.setWindowTitle(self.tr("Curves"))
        self.color_label.setText(self.tr("Color"))
        self.width_label.setText(self.tr("Width"))

    def _change_curves_width(self, value):
        for curve in self.curves:
            pen = curve.opts['pen']
            pen.setWidth(value)
            curve.setPen(pen)
            curve.update()

    def _change_curves_color(self):
        cur_color = getattr(self.color_button, "color")
        color = QColorDialog.getColor(cur_color)
        if color.isValid():
            for curve in self.curves:
                pen = curve.opts['pen']
                pen.setColor(color)
                curve.setPen(pen)
                curve.update()
            setattr(self.color_button, "color", color)
            self.color_button.setStyleSheet(f"background: rgb({color.red()}, {color.green()}, {color.blue()})")
