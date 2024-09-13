# -*- coding: utf-8 -*-
import datetime
import os
from typing import Iterable

from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QIcon
from loguru import logger
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QTabWidget, QScrollArea, QFrame, QAbstractScrollArea, QWidget, \
    QVBoxLayout, QGroupBox, QGridLayout, QFileDialog, QSpacerItem, QSizePolicy, QSpacerItem

from version import VERSION
from .main_window_base import ToolBase, Direction

from ..core.data_layer import DataLayer
from ..core.device.base import DeviceStatus
from ..core.device.ble_handler import BleHandler
from .widgets.device.ble_widget import BleWidget
from .widgets.plot_widget.plot_widget import PlotQTWidget, MultiCurvesInOnePlot, SingleCurvesInOnePlot, PlotWidgetWith2Y
from ..core.data_handler import ToolProtoDataManageHandler
from ..config.settings import PROTO_CONFIG, BLE_CONFIG, TOOL_CONFIG, BASIC
from ..utils.path import APP_ROOT_PATH


DATA_PATH = "data"


class Gui(ToolBase):

    ble_discover_callback_signal = Signal(list)
    ble_status_callback_signal = Signal(DeviceStatus, str)
    ble_data_received_callback_signal = Signal(bytes)
    append_ble_chart_signal = Signal(str, bytes)

    serial_status_callback_signal = Signal(DeviceStatus, str)
    serial_data_received_callback_signal = Signal(bytes)

    def __init__(self):
        super().__init__()
        self.resize(1300, 800)
        self.setWindowTitle(BASIC["main_window_title"] + "  " + VERSION)
        self.setWindowIcon(QIcon(os.path.join(APP_ROOT_PATH, "material", "edu.ico")))

        self.data_manage_handler = ToolProtoDataManageHandler()
        self.data_layer = DataLayer(self.data_manage_handler)

        self.imu_widgets = {}
        self.ppg_widgets = {}

        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plots)
        self.plot_timer.start(50)

        self.init_proto_config_window(PROTO_CONFIG, self._send_device_command)

        self._init_ui()
        self._init_device_ui()
        self._connect_event()

    def _connect_event(self):
        pass

    def _init_ui(self):
        self.main_tab_widget = QTabWidget()
        self.add_widget_to_center_layout(self.main_tab_widget)

    def _init_imu_ui(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)
        for title, label in zip(["ACC", "GYRO", "EULAR"], [["x", "y", "z"], ["x", "y", "z"], ["yaw", "pitch", "roll"]]):
            plot_widget = MultiCurvesInOnePlot(title, label, ["r", "g", "y"])
            layout.addWidget(plot_widget)
            self.imu_widgets[title] = plot_widget
        self.main_tab_widget.addTab(widget, "IMU")

    def _init_ppg_ui(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        for title, label in zip(["HR", "RR", "SPO2"], [["hr", "confidence"], ["rr", "confidence"], ["spo2", "confidence"]]):
            plot_widget = PlotWidgetWith2Y(title, label[0], label[1], range2=(0, 100))
            layout.addWidget(plot_widget)
            self.ppg_widgets[title] = plot_widget

        raw_plot_widget = MultiCurvesInOnePlot(title="Raw Data", labels=["1: Green1", "2: Green2", "3: IR", "4: Red"], colors=["g", "y", "r", "c"])
        layout.addWidget(raw_plot_widget)
        self.ppg_widgets["RAW"] = raw_plot_widget

        self.main_tab_widget.addTab(widget, "PPG")

    def _init_device_ui(self):
        self.device_handler = BleHandler(service_uuid=BLE_CONFIG["server_uuid"],
                                         tx_uuid=BLE_CONFIG["tx_uuid"],
                                         rx_uuid=BLE_CONFIG["rx_uuid"])
        self.device_handler.set_callbacks(on_scan_result=self.ble_discover_callback_signal.emit,
                                          on_dev_status=self.ble_status_callback_signal.emit,
                                          on_recv_data=self.ble_data_received_callback_signal.emit,
                                          on_get_ble_info=self.append_ble_chart_signal.emit)
        self.device_widget = BleWidget(self.device_handler)
        self.verticalLayout_device.addWidget(self.device_widget)

        self.ble_discover_callback_signal.connect(self.device_widget.on_scan_result)
        self.ble_status_callback_signal.connect(self._on_ble_status_callback)
        self.ble_data_received_callback_signal.connect(self.recv_device_raw_data)
        self.append_ble_chart_signal.connect(self.device_widget.on_get_ble_info)

    def update_plots(self):
        pass

    def _on_ble_status_callback(self, status, msg):
        logger.info("ble updated: {}, {}".format(DeviceStatus(status).name, msg))
        self.device_widget.on_dev_status(status, msg)
        if status == DeviceStatus.DISCONNECTED:
            pass
        elif status == DeviceStatus.CONNECTED:
            pass

    def recv_device_raw_data(self, data: bytes):
        # logger.info("received: {}".format(data))
        self.data_manage_handler.on_received_device_raw_message(data)

    def _send_device_command(self, command):
        self.device_handler.send_data_to_device(command)



