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
from .widgets.data_logger_dialog import DataLoggerDialog

from ..core.data_layer import DataLayer
from ..core.device.base import DeviceStatus
from ..core.device.ble_handler import BleHandler
from .widgets.device.ble_widget import BleWidget
from .widgets.plot_widget.plot_widget import PlotQTWidget, MultiCurvesInOnePlot, SingleCurvesInOnePlot, PlotWidgetWith2Y
from ..core.data_handler import ToolProtoDataManageHandler
from ..config.settings import PROTO_CONFIG, BLE_CONFIG, TOOL_CONFIG, BASIC
from ..utils.path import APP_ROOT_PATH


from aura_algo import AuraAlgo


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

        self.aura_algo = AuraAlgo(QIcon(os.path.join(APP_ROOT_PATH, "material", "edu.ico")), mx_ppg=False)
        self.data_layer.ppg_raw_signal.connect(self.aura_algo.update_ppg)
        self.data_layer.acc_raw_signal.connect(self.aura_algo.update_imu)
        self.aura_algo.show()

        self.imu_widgets = {}
        self.ppg_widgets = {}

        self.data_logger_dialog = DataLoggerDialog(self)

        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plots)
        self.plot_timer.start(50)

        self.init_proto_config_window(PROTO_CONFIG, self._send_device_command)

        self._init_ui()
        self._init_device_ui()
        self._connect_event()

    def _connect_event(self):
        self.data_logger_dialog.start_signal.connect(self._on_start_data_logger)
        self.data_logger_dialog.stop_signal.connect(self._on_stop_data_logger)

    def _init_ui(self):
        self.main_tab_widget = QTabWidget()
        self.add_widget_to_center_layout(self.main_tab_widget)

        self.tools_menu = self.menuBar().addMenu("Tools")
        self.tools_menu.addAction("Data Logger", self.data_logger_dialog.show)

        self._init_imu_ui()
        self._init_ppg_ui()

    def _init_imu_ui(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)
        for title, label in zip(["ACC", "GYRO"], [["x", "y", "z"], ["x", "y", "z"]]):
            plot_widget = MultiCurvesInOnePlot(title, label, ["r", "g", "y"])
            layout.addWidget(plot_widget)
            self.imu_widgets[title] = plot_widget
        self.main_tab_widget.addTab(widget, "IMU")

    def _init_ppg_ui(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        for title, label in zip(["HR", "RR"], [["hr", "confidence"], ["rr", "confidence"]]):
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

    def _on_start_data_logger(self, label):
        folder = os.path.join(DATA_PATH, datetime.datetime.now().strftime("%Y%m%d"))
        if not os.path.exists(folder):
            os.makedirs(folder)

        file_name = "".join([datetime.datetime.now().strftime("%H-%M-%S"), "_", label])
        file_path = os.path.join(folder, file_name)
        self.data_layer.enable_save_data(file_path)
        self.aura_algo.enable_data_logger(file_path)

    def _on_stop_data_logger(self):
        self.data_layer.enable_save_data("")
        self.aura_algo.enable_data_logger("")

    def update_plots(self):
        # imu
        imu_buffer = self.data_layer.imu_buffer
        for title, widget in self.imu_widgets.items():
            for idx, curve in enumerate(widget.curve_list):
                curve.setData(imu_buffer[title.lower()][idx])

        # ppg
        ppg_algo = self.data_layer.ppg_algo_buffer
        ppg_algo_value_list = list(ppg_algo.values())
        for idx, title in enumerate(["HR", "RR"]):
            widget = self.ppg_widgets[title]
            widget.curve_list[0].setData(ppg_algo_value_list[idx * 2])
            widget.curve_list[1].setData(ppg_algo_value_list[idx * 2 + 1])

        ppg_raw = self.data_layer.ppg_raw_buffer
        ppg_raw_value_list = list(ppg_raw.values())
        for idx, curve in enumerate(self.ppg_widgets["RAW"].curve_list):
            curve.setData(ppg_raw_value_list[idx])

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



