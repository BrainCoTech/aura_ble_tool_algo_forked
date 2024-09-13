import time
from typing import Optional

from PySide6.QtCore import Qt, QCoreApplication, Signal
from loguru import logger
from PySide6.QtWidgets import QMainWindow, QProgressDialog, QLabel, QFrame, QWidget, QGridLayout, QDockWidget, \
    QScrollArea, QAbstractScrollArea, QApplication, QVBoxLayout, QPushButton

from ....utils.messagebox_helper import MessageBoxHelper


class DeviceWidgetBase(QWidget):
    recv_data_signal = Signal(bytes)

    _device_handler = None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.msg_box_helper = MessageBoxHelper(self)

    def on_recv_device_data(self, data: bytes):
        buffer = []
        for i in range(len(data)):
            buffer.append("{:02X}".format(data[i]))
        logger.debug("received:" + str(" ".join(buffer)))

        self.recv_data_signal.emit(data)

    def send_data_to_device(self, *args, **kwargs):
        pass

