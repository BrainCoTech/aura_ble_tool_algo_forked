# -*- coding: utf-8 -*-
import datetime
import os
import pprint

from PySide6.QtCore import Signal
from google.protobuf.json_format import ParseDict, ParseError
from loguru import logger
from ruamel.yaml import YAML

from ...config.register_proto import get_proto_class
from ...core.device.base import DeviceBase
from ...core.device.ble_handler import BleHandler
from ...core.tool_packet import ToolPacket, StarkMessageId

yaml = YAML()

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QFileDialog, QMessageBox

from .text_browser_widget import TextBrowser
from .ui.protol_config_widget import Ui_Form
from ...utils.images import *
from ...utils.public_func import get_pixmap
from ...utils.path import APP_ROOT_PATH

_SAVE_PATH = os.path.join(APP_ROOT_PATH, "save_data")
if not os.path.exists(_SAVE_PATH):
    os.makedirs(_SAVE_PATH)


class ProtolConfigWidget(QWidget, Ui_Form):
    get_whole_cfg_req_signal = Signal()
    send_command_signal = Signal(bytes)

    def __init__(self, device_handler, parent=None):
        super(ProtolConfigWidget, self).__init__(parent)
        self.setupUi(self)

        self.device_handler = device_handler

        self._current_proto_data = None  # dict

        self.init_ui()
        self._connect_ui()

    def init_ui(self):
        self.text_browser_widget = TextBrowser("")
        self.verticalLayout_text.addWidget(self.text_browser_widget)
        self.pushButton_get.setIcon(QIcon(get_pixmap(REFRESH_IMG_BASE64)))
        self.pushButton_import.setIcon(QIcon(get_pixmap(IMPORT_FILE_IMG)))
        self.pushButton_set.setIcon(QIcon(get_pixmap(SET_IMG)))

        self.pushButton_import.setToolTip("Import")
        self.pushButton_set.setToolTip("Set Configuration")
        self.pushButton_get.setToolTip("Get Configuration")

    def _connect_ui(self):
        self.pushButton_import.clicked.connect(self._on_import_clicked)
        self.pushButton_get.clicked.connect(self._on_get_clicked)
        self.pushButton_set.clicked.connect(self._on_set_clicked)

    def _on_import_clicked(self):
        # 加载配置文件
        file = QFileDialog.getOpenFileName(self, "Open File", _SAVE_PATH, "Proto Files (*.yaml)")
        if file[0]:
            self.text_browser_widget.clear()
            with open(file[0], "r") as f:
                data = yaml.load(f)
                self._current_proto_data = data
                self._show_proto_data()

    def _on_get_clicked(self):
        # 从设备获取配置
        if isinstance(self.device_handler, DeviceBase):
            if not self.device_handler.check_device_is_connected():
                QMessageBox.warning(self.parent(), "Warning", "Device is not connected!")
                return

            self.get_whole_cfg_req_signal.emit()

            self.text_browser_widget.clear()

            command = get_proto_class("U_AppToMainUS")()
            command.whole_cfg_req.req = True
            msg = ToolPacket(payload=command.SerializeToString(),
                             source_id=StarkMessageId.App,
                             destination_id=StarkMessageId.MainBoard)
            logger.info("\n{}\n{}".format(msg, command))
            self.send_command_signal.emit(msg.encode())

    def _save_config(self, file_path):
        try:

            if os.path.exists(file_path):
                os.remove(file_path)

            if isinstance(self._current_proto_data, dict):
                with open(file_path, "w") as f:
                    yaml.dump(self._current_proto_data, f)
        except Exception as e:
            QMessageBox.warning(self.parent(), "Warning", f"Save configuration failed! {e}")

    def _on_set_clicked(self):
        if isinstance(self.device_handler, DeviceBase):
            if not self.device_handler.check_device_is_connected():
                QMessageBox.warning(self.parent(), "Warning", "Device is not connected!")
                return

            # 需要将保存的配置映射到config message中
            if isinstance(self._current_proto_data, dict):

                # 由于协议回复包里面的cmd类型都是resp， 我们设置的时候需要改成set

                config = {}
                if "grip_loop_table_cfg_resp" in self._current_proto_data.keys():
                    config["grip_loop_table_config"] = self._current_proto_data["grip_loop_table_cfg_resp"]
                    config["grip_loop_table_config"]["cmd"] = 'SET'
                if "grip_trigger_cfg_resp" in self._current_proto_data.keys():
                    config["grip_trigger_config"] = self._current_proto_data["grip_trigger_cfg_resp"]
                    config["grip_trigger_config"]["cmd"] = 'SET_ID'
                if "electrode_cfg_resp" in self._current_proto_data.keys():
                    config["electrode_config"] = self._current_proto_data["electrode_cfg_resp"]
                    set_cmd_str = config["electrode_config"]["cmd"]
                    set_cmd_str.replace("RESP", "SET")
                    config["electrode_config"]["cmd"] = set_cmd_str
                if "hand_cfg_resp" in self._current_proto_data.keys():
                    config["hand_config"] = self._current_proto_data["hand_cfg_resp"]
                if "msg_id" in self._current_proto_data.keys():
                    config["msg_id"] = self._current_proto_data["msg_id"]

                command = get_proto_class("U_AppToMainUS")()
                try:
                    ParseDict(config, command)
                except ParseError as e:
                    QMessageBox.warning(self.parent(), "Warning", f"ParseDict failed! {e}")
                    return

                msg = ToolPacket(payload=command.SerializeToString(),
                                 source_id=StarkMessageId.App,
                                 destination_id=StarkMessageId.MainBoard)
                logger.info("\n{}\n{}".format(msg, command))
                self.send_command_signal.emit(msg.encode())
                QMessageBox.information(self.parent(), "Info", "Set configuration success!")

    def _show_proto_data(self):
        self.text_browser_widget.clear()
        if isinstance(self._current_proto_data, dict):
            text = pretty_format(self._current_proto_data)
            self.text_browser_widget.setText(text)

    def recv_proto_data(self, data: dict):
        # 外部调用
        self._current_proto_data = data
        self._show_proto_data()

        file_name_suffix = ""
        if isinstance(self.device_handler, BleHandler):
            if self.device_handler.check_device_is_connected():
                mac = self.device_handler.device.address.replace(":", "")
                # file_name_suffix = mac[-5:]

                # file_name = "".join([datetime.datetime.now().strftime("%H-%M-%S")])
                # file_name = file_name + "_" + file_name_suffix if file_name_suffix else file_name
                file_name = mac + ".yaml"
                file_path = os.path.join(_SAVE_PATH, file_name)
                self._save_config(file_path)


def pretty_format(data: dict, indent=0):
    res = []
    indent_str = '    ' * indent
    for key, value in data.items():
        if isinstance(value, dict):
            res.append(f'{indent_str}{key}:')
            res.append(pretty_format(value, indent+1))
        else:
            res.append(f'{indent_str}{key}: {value}')
    return '\n'.join(res)

