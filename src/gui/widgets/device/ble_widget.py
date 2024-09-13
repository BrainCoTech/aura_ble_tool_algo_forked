# -*- coding: utf-8 -*-

from loguru import logger
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QLabel, QWidget, QMessageBox, QApplication

from ..ui.ble_widget import Ui_Form
from ....core.device.base import DeviceStatus
from ....core.device.ble_handler import BleHandler, DEFAULT_UUID, BleStatus, BATTERY

# 为了翻译
MANUFACTURER = "Manufacturer"
MODEL_NUMBER = "Model Number"
SERIAL_NUMBER = "Serial Number"
HARDWARE_REVISION = "Hardware Version"
FIRMWARE_REVISION = "Firmware Version"
BATTERY = "Battery"


class CopyLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)
        # 设置鼠标样式
        self.setCursor(Qt.PointingHandCursor)

    def mouseDoubleClickEvent(self, event) -> None:
        self.copy()
        super(CopyLabel, self).mouseDoubleClickEvent(event)

    def copy(self):
        # 将文本复制到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text())


class BleWidget(QWidget, Ui_Form):
    parse_device_info_ui_dict = {}

    def __init__(self, ble_handler: BleHandler, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.tip_labels = {}
        self._device_handler = ble_handler
        self._create_device_info_ui()
        self._connect_event()

        self.read_battery_timer = QTimer()
        # self.read_battery_timer.timeout.connect(self.on_read_battery_value)  # 需要隔一段时间就刷新的值在定时器中获取
        # self.read_battery_timer.start(3000 * 60)  # 3分钟刷新一次

    def translate_ui(self):
        self.button_scan.setText(self.tr("scan"))
        if self._device_handler.check_device_is_connected():
            self.button_connect.setText(self.tr("disconnect"))
        else:
            self.button_connect.setText(self.tr("connect"))
        self.tip_labels[MANUFACTURER].setText(self.tr("Manufacturer") + ":")
        self.tip_labels[MODEL_NUMBER].setText(self.tr("Model Number") + ":")
        self.tip_labels[SERIAL_NUMBER].setText(self.tr("Serial Number") + ":")
        self.tip_labels[HARDWARE_REVISION].setText(self.tr("Hardware Version") + ":")
        self.tip_labels[FIRMWARE_REVISION].setText(self.tr("Firmware Version") + ":")
        self.tip_labels[BATTERY].setText(self.tr("Battery") + ":")

    def _create_device_info_ui(self):
        for idx, string in enumerate(list(DEFAULT_UUID.keys())):
            row = idx // 3
            col = idx % 3 * 2
            label1 = QLabel(string + ":")
            label2 = CopyLabel("")
            self.tip_labels[string] = label1
            self.parse_device_info_ui_dict[string] = label2
            self.gridLayout_device_info.addWidget(label1, row, col, 1, 1)
            self.gridLayout_device_info.addWidget(label2, row, col+1, 1, 1)

    def hide_device_info_ui(self):
        for i in range(self.gridLayout_device_info.count()):
            widget = self.gridLayout_device_info.itemAt(i)
            if widget:
                widget.hide()

    def _connect_event(self):
        self.button_scan.clicked.connect(self.on_click_scan_button)
        self.button_connect.clicked.connect(self.on_click_connect_button)

    def on_click_scan_button(self):
        self.combobox_devices.clear()
        self.button_scan.setEnabled(False)
        self._device_handler.scan()

    def on_click_connect_button(self):
        self.button_scan.setEnabled(False)
        if self._device_handler.check_device_is_connected():
            # 断开
            self._device_handler.disconnect_to_device()
            self.button_connect.setEnabled(False)
        else:
            # 连接
            ble_data = self.combobox_devices.currentData()
            if ble_data:
                self._device_handler.connect_to_device(ble_data[0])
                self.button_connect.setEnabled(False)

    def on_ble_status(self, status, msg):
        logger.info("ble status updated: {}, {}".format(BleStatus(status).name, msg))
        if status == BleStatus.ENABLED:
            pass
        if status == BleStatus.ENABLED_FAILED:
            self.button_scan.setEnabled(True)
            QMessageBox.warning(self, self.tr("Error"), msg)
        elif status == BleStatus.STOPPED:
            pass
        else:
            pass

    def on_dev_status(self, status, msg):
        if status == DeviceStatus.CONNECTED:
            self._device_handler.subscribe_to_rx_char(self.subscribe_nus_callback)
        elif status == DeviceStatus.DISCONNECTED:
            self.button_connect.setText(self.tr("connect"))
            self.combobox_devices.clear()
            self.combobox_devices.setEnabled(True)
            self.button_scan.setEnabled(True)
            self.button_connect.setEnabled(True)

            for widget in self.parse_device_info_ui_dict.values():
                widget.clear()
            self.combobox_devices.update()

    def subscribe_nus_callback(self, res: bool, msg: str):
        logger.info("subscribe_nus_callback finished")
        if res:

            # 可能在订阅结束时后 设备先断开连接, 所以在此处我们再次确认设备已连接
            if self._device_handler.check_device_is_connected():
                self.button_connect.setText(self.tr("disconnect"))
                self.button_connect.setEnabled(True)
                self.combobox_devices.setEnabled(False)
                self.button_scan.setEnabled(False)

        else:
            self._device_handler.disconnect_to_device()

    def on_scan_result(self, discover_devices: list):
        self.combobox_devices.clear()
        discover_devices = sorted(discover_devices, key=lambda dev: dev.rssi, reverse=True)
        for device in discover_devices:
            info = "{}, {}, {}dBm".format(device.name, device.address, device.rssi)
            self.combobox_devices.addItem(info, (device.address, device.metadata["manufacturer_data"]))
        self.button_scan.setEnabled(True)
        self.combobox_devices.setCurrentIndex(0)

    def on_get_ble_info(self, k, data):
        if k in self.parse_device_info_ui_dict.keys():
            if k == BATTERY:
                value = str(int.from_bytes(data, 'little', signed=False)) + " %"
            else:
                value = data.decode("utf-8")
            self.parse_device_info_ui_dict[k].setText(value)

    def on_read_battery_value(self):
        self._device_handler.read_gatt_char_by_uuid(BATTERY, DEFAULT_UUID[BATTERY])
