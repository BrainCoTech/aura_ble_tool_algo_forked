# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextEdit, QSizePolicy, QDialog, QVBoxLayout, QScrollArea, QFrame, QAbstractScrollArea, \
    QWidget, QFormLayout, QLabel


class InfoTextEdit(QTextEdit):
    def __init__(self, title, parent=None):
        super(InfoTextEdit, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMaximumHeight(40)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setReadOnly(True)

        self.show_text_dict = {}
        self.show_info_dialog_label = {}
        self.show_info_dialog = QDialog(self)
        self.show_info_dialog.setWindowFlags(Qt.Tool)

        vertical_layout = QVBoxLayout(self.show_info_dialog)
        vertical_layout.setSpacing(0)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area = QScrollArea(self.show_info_dialog)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        scroll_area.setWidgetResizable(True)

        widget = QWidget()
        self.info_layout = QFormLayout()
        widget.setLayout(self.info_layout)
        scroll_area.setWidget(widget)
        vertical_layout.addWidget(scroll_area)

        self.show_info_dialog.setWindowTitle(title)

    def _reset_label_text(self):
        self.clear()
        text_str = ''
        for key, value in self.show_text_dict.items():
            text_str += f"{key}: {value}   "
        self.setText(text_str)

    def append_info(self, title: str, text_rgb=None, text_wh=None) -> None:
        if title not in self.show_info_dialog_label:
            label1 = QLabel(title + ":")
            label2 = QLabel()
            self.show_info_dialog_label[title] = label2
            self.info_layout.addRow(label1, label2)
        else:
            print(f"已经存在{title}的label, 请使用update_info方法更新")
            return

        if text_rgb:
            qss = f'background-color:rgb({text_rgb[0]},{text_rgb[1]},{text_rgb[2]})'
            self.show_info_dialog_label[title].setStyleSheet(qss)
        if text_wh:
            self.show_info_dialog_label[title].setFixedHeight(text_wh[1])

    def update_info(self, title, text):
        self.show_text_dict[title] = text
        self._reset_label_text()
        if title in self.show_info_dialog_label:
            self.show_info_dialog_label[title].setText(text)

    def mouseDoubleClickEvent(self, event) -> None:
        if len(self.show_info_dialog_label.keys()):
            self.show_info_dialog.show()
            # 移动到当前窗口的中心
            self.show_info_dialog.move(self.mapToGlobal(self.rect().center()) - self.show_info_dialog.rect().center())
        super(InfoTextEdit, self).mouseDoubleClickEvent(event)
