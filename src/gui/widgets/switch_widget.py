#!/usr/bin/env python3.6
# -*- coding:utf-8 -*-


from PySide6.QtCore import Signal, QTimer, QRect, Qt, QRectF, QPropertyAnimation, Property
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath
from PySide6.QtWidgets import QWidget


class SwitchWidget(QWidget):
    checked_changed_signal = Signal(bool)

    def __init__(self, text_on, text_off, parent=None):
        super(SwitchWidget, self).__init__(parent)

        self._checked = False
        self._space = 2
        self._start_x = 0
        self._end_x = 0
        self._text_on = text_on
        self._text_off = text_off

        self._bg_color_on = QColor(0, 159, 170)
        self._bg_color_off = QColor(240, 240, 240)
        self._slider_color_on = QColor(255, 255, 255)
        self._slider_color_off = QColor(93, 93, 93)
        self._text_color_off = QColor(93, 93, 93)
        self._text_color_on = QColor(255, 255, 255)

        self.slideAni = QPropertyAnimation(self, b'start_x', self)
        self.slideAni.setDuration(200)

    def switch(self, state):
        self._checked = state
        if state:
            self._end_x = self.width() - self.height()
        else:
            self._end_x = 0
        self.slideAni.setEndValue(self._end_x)
        self.slideAni.start()

    def mousePressEvent(self, event):
        self._checked = not self._checked
        # 发射信号
        self.checked_changed_signal.emit(self._checked)

        if self._checked:
            self._end_x = self.width() - self.height()
        else:
            self._end_x = 0

        self.slideAni.setEndValue(self._end_x)
        self.slideAni.start()

    def paintEvent(self, evt):
        # 绘制准备工作, 启用反锯齿
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        self.draw_bgg(evt, painter)
        # 绘制滑块
        self.draw_slider(evt, painter)
        # 绘制文字
        self.draw_text(evt, painter)

        painter.end()

    def draw_text(self, event, painter):
        painter.save()

        if self._checked:
            painter.setPen(self._text_color_on)
            painter.drawText(0, 0, self.width() / 2 + self._space * 2, self.height(), Qt.AlignCenter, self._text_on)
        else:
            painter.setPen(self._text_color_off)
            painter.drawText(self.width() / 2, 0, self.width() / 2 - self._space, self.height(), Qt.AlignCenter,
                             self._text_off)

        painter.restore()

    def draw_bgg(self, event, painter):
        painter.save()
        painter.setPen(Qt.NoPen)

        if self._checked:
            painter.setBrush(self._bg_color_on)
        else:
            painter.setBrush(self._bg_color_off)

        rect = QRect(0, 0, self.width(), self.height())
        # 半径为高度的一半
        radius = rect.height() / 2
        # 圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()

    def draw_slider(self, event, painter):
        painter.save()
        if self._checked:
            painter.setBrush(self._slider_color_on)
        else:
            painter.setBrush(self._slider_color_off)
        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self._space * 2
        sliderRect = QRect(self._start_x + self._space, self._space, sliderWidth, sliderWidth)
        painter.drawEllipse(sliderRect)
        painter.restore()

    def get_slider_x(self):
        return self._start_x

    def set_slider_x(self, x):
        self._start_x = x
        self.update()

    def is_checked(self):
        return self._checked

    start_x = Property(float, get_slider_x, set_slider_x)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QWidget, QApplication

    app = QApplication(sys.argv)
    window = QWidget()
    button = SwitchWidget("On", "Off", window)
    button.move(50, 50)
    button.resize(200, 50)
    window.resize(500, 500)
    window.setStyleSheet("QWidget{background-color: green;}")
    window.show()
    sys.exit(app.exec())

