import pprint
from typing import Any

from PySide6.QtGui import QTextCursor, QColor
from PySide6.QtWidgets import QTextBrowser, QTextEdit


class TextBrowser(QTextBrowser):
    def __init__(self, qss: str, parent=None):
        super(TextBrowser, self).__init__(parent)
        self.setStyleSheet(qss)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.textChanged.connect(self._on_text_browser_changed)
        self.setMinimumHeight(200)

    def _on_text_browser_changed(self):
        # 将光标移动到文本末尾并获取文本末尾的QTextCursor对象
        text_cursor = self.textCursor()
        text_cursor.movePosition(QTextCursor.End)
        self.setTextCursor(text_cursor)
        # 将光标移动到最后一行的开头
        text_cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
        self.setTextCursor(text_cursor)

    def append_text(self, data: Any, rgb: tuple, enable_format=False):

        text = data
        enable_format = enable_format

        if not enable_format:
            msg = repr(text)
        else:
            if isinstance(text, (list, dict, tuple, set)):
                text = pprint.pformat(text)
            else:
                text = str(text)

            msg = text.replace('\r\n', '<br/>')
            msg = msg.replace('\n\r', '<br/>')
            msg = msg.replace('\n', '<br/>')
            msg = msg.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')

        color = QColor(rgb[0], rgb[1], rgb[2])
        color_str = f"rgb({color.red()}, {color.green()}, {color.blue()})"
        colored_text = f"<span style='color: {color_str}'>{msg}</span>"
        self.append(colored_text)

    def mouseDoubleClickEvent(self, event) -> None:
        event.ignore()
