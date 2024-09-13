import os
from enum import IntEnum
from PySide6.QtCore import Qt
from ruamel.yaml import YAML
from typing import Optional, Callable
from PySide6.QtWidgets import QMainWindow, QWidget, QTabWidget, QComboBox, QDoubleSpinBox, QSpinBox, QLineEdit, \
    QCheckBox

from .widgets.protobuf_widget import BigIntSpinbox

yaml = YAML()

from .widgets.dock_widget import CommonDockWidget, ProtoConfigDockWidget, ProtoDataDockWidget
from .widgets.ui.mainwindow import Ui_MainWindow
from ..utils.language_support import LanguageSupport
from ..config.settings import PROTO_CONFIG, BASIC, ALL_CONFIG, SETTINGS_FILE_PATH
from ..utils.messagebox_helper import MessageBoxHelper


class Direction(IntEnum):
    RIGHT = 0
    LEFT = 1
    BOTTOM = 2
    # TOP = 3  # 暂时没想好支持上位置的组件添加方式, 可能会导致布局ui不太美观


COMPONENT_DIRECTION_CONFIG = {
    Direction.RIGHT: Qt.RightDockWidgetArea,
    Direction.LEFT: Qt.LeftDockWidgetArea,
    Direction.BOTTOM: Qt.BottomDockWidgetArea
}


class ToolBase(QMainWindow, Ui_MainWindow):
    component_widget_dict = {}  # title: widget

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.msg_box_helper = MessageBoxHelper(self)
        self.language_support = LanguageSupport()

        # self.__init_ui()
        self.__ui_connect_event()

    # def __init_ui(self):
    #     self.language_menu = self.menuBar().addMenu(self.tr("Language"))
    #     self.chinese_action = self.language_menu.addAction("汉语 - Chinese", self._on_change_language_menu)
    #     self.chinese_action.setCheckable(True)
    #     self.chinese_action.setData("Chinese")
    #     self.english_action = self.language_menu.addAction("英语 - English", self._on_change_language_menu)
    #     self.english_action.setCheckable(True)
    #     self.english_action.setData("English")

    # def _on_change_language_menu(self):
    #     self.update_translate_ui(self.sender().data())
    #
    #     ALL_CONFIG["BASIC"]["language"] = self.sender().data()
    #     with open(SETTINGS_FILE_PATH, 'w', encoding='utf-8') as f:
    #         yaml.dump(ALL_CONFIG, f)

    def update_translate_ui(self, language_type: str):
        pass
        # if language_type == "Chinese":
        #     self.chinese_action.setChecked(True)
        #     self.english_action.setChecked(False)
        # else:
        #     self.chinese_action.setChecked(False)
        #     self.english_action.setChecked(True)
        # self.language_support.change_language(language_type)
        # self.language_menu.setTitle(self.tr("Language"))
        # self.retranslateUi(self)

    def __ui_connect_event(self):
        pass

    def _tabify_dock_widgets(self):
        # 调整dock_widget的tab顺序
        dock_widgets = self.component_widget_dict.values()
        left_dock_widgets = []
        right_dock_widgets = []
        bottom_dock_widgets = []
        for widget in dock_widgets:
            if self.dockWidgetArea(widget) == Qt.LeftDockWidgetArea:
                left_dock_widgets.append(widget)
            elif self.dockWidgetArea(widget) == Qt.RightDockWidgetArea:
                right_dock_widgets.append(widget)
            elif self.dockWidgetArea(widget) == Qt.BottomDockWidgetArea:
                bottom_dock_widgets.append(widget)

        for widgets in [left_dock_widgets, right_dock_widgets, bottom_dock_widgets]:
            if len(widgets) > 1:
                for i in range(len(widgets) - 1):
                    self.tabifyDockWidget(widgets[i], widgets[i + 1])

        if right_dock_widgets:  # 优先显示第一个添加的组件
            right_dock_widgets[0].raise_()
        if left_dock_widgets:
            left_dock_widgets[0].raise_()
        if bottom_dock_widgets:
            bottom_dock_widgets[0].raise_()

# --------------------------分享给子类调用的api-------------------------------------------------
    def add_common_component(self,
                             title: str,
                             widget: QWidget,
                             direction: Direction.RIGHT,
                             **kwargs) -> CommonDockWidget:
        """
            Add components to the interface, paying special attention to the fact that when 'title' has been recorded,
            it will return the components that have been recorded instead of creating a new component.

        Args:
            title:
            widget:
            direction:
            **kwargs: All parameters are passed to the 'CommonDockWidget' class.

        Returns: CommonDockWidget

        """
        if title in self.component_widget_dict:
            return self.component_widget_dict[title]

        dock_widget = CommonDockWidget(**kwargs)
        dock_widget.setWindowTitle(title)
        dock_widget.setWidget(widget)
        self.addDockWidget(COMPONENT_DIRECTION_CONFIG[direction], dock_widget)
        self.component_widget_dict[title] = dock_widget

        self._tabify_dock_widgets()

        return dock_widget

    def init_proto_config_window(self, proto_config: dict, send_command_func: Optional[Callable]):
        """

        Returns:

        """
        widgets = []
        proto_class = proto_config["proto_class"]
        for source_destination_id, proto_class_list in proto_class.items():
            proto_config_class_str = proto_class_list[0]
            source_id, destination_id = [int(i) for i in source_destination_id.split(',')]
            dock_widget = ProtoConfigDockWidget(proto_class_str=proto_config_class_str,
                                                source_id=source_id,
                                                destination_id=destination_id,
                                                send_command_func=send_command_func)
            dock_widget.setWindowTitle(proto_config_class_str)

            self.addDockWidget(COMPONENT_DIRECTION_CONFIG[Direction.RIGHT], dock_widget)
            self.component_widget_dict[proto_config_class_str] = dock_widget
            widgets.append(dock_widget)

            self.setTabPosition(dock_widget.allowedAreas(), QTabWidget.TabPosition.North)
            self.resizeDocks([dock_widget], [450], Qt.Horizontal)

        self._tabify_dock_widgets()

    def init_proto_data_component(self, proto_class_str: str):
        dock_widget = ProtoDataDockWidget(proto_class_str=proto_class_str)
        dock_widget.setWindowTitle(proto_class_str)

        self.addDockWidget(COMPONENT_DIRECTION_CONFIG[Direction.RIGHT], dock_widget)
        self.component_widget_dict[proto_class_str] = dock_widget

        self.setTabPosition(dock_widget.allowedAreas(), QTabWidget.TabPosition.North)
        self.resizeDocks([dock_widget], [450], Qt.Horizontal)

        self._tabify_dock_widgets()

        return dock_widget

    def add_widget_to_center_layout(self,
                                    widget: QWidget,
                                    coordinate: Optional[list] = None):
        """

        Args:
            widget:
            coordinate:

        Returns:

        """
        if coordinate:
            self.gridLayout_center.addWidget(widget, *coordinate)
        else:
            self.gridLayout_center.addWidget(widget)

    def remove_component(self, title):
        """

        Args:
            title:

        Returns:

        """
        widget = self.component_widget_dict[title]
        self.removeDockWidget(widget)
        del self.component_widget_dict[title]

    def remove_widget_from_center_layout(self, widget):
        self.gridLayout_center.removeWidget(widget)

    def custom_protobuf_ui_by_yaml(self, protobuf_ui_path: str):
        if not os.path.exists(protobuf_ui_path):
            return
        with open(protobuf_ui_path, 'r') as f:
            protobuf_ui_config = yaml.load(f)
            if not isinstance(protobuf_ui_config, dict) or len(protobuf_ui_config.keys()) == 0:
                return

        for proto_class_name in protobuf_ui_config.keys():
            if proto_class_name not in self.component_widget_dict.keys():
                continue
            title_keys = list(protobuf_ui_config[proto_class_name].keys())
            for proto_widget in self.component_widget_dict[proto_class_name].proto_widget_list:
                if str(proto_widget.path) not in title_keys:
                    continue
                custom_ui_config = protobuf_ui_config[proto_class_name][str(proto_widget.path)]
                enable = custom_ui_config.get("enable", True)
                selected = custom_ui_config.get("selected", False)
                show = custom_ui_config.get("show", True)
                value = custom_ui_config.get("value")
                _range = custom_ui_config.get("range", None)  # Only for QSpinBox and QDoubleSpinBox
                show_name = custom_ui_config.get("show_name", None)

                if not isinstance(proto_widget.selectable_widget, QCheckBox):
                    print(f"{proto_widget.path} widget type is not QCheckBox")
                    continue

                proto_widget.selectable_widget.setEnabled(enable)
                proto_widget.selectable_widget.setVisible(show)
                proto_widget.selectable_widget.setChecked(selected)

                proto_widget.widget.setEnabled(enable)
                proto_widget.widget.setVisible(show)

                if isinstance(show_name, str):
                    proto_widget.selectable_widget.setText(show_name)

                if isinstance(_range, list) and len(_range) == 2:
                    if isinstance(proto_widget.widget, QDoubleSpinBox):
                        proto_widget.widget.setRange(float(_range[0]), float(_range[1]))
                    elif isinstance(proto_widget.widget, (BigIntSpinbox, QSpinBox)):
                        proto_widget.widget.setRange(int(_range[0]), int(_range[1]))
                    else:
                        print(f"{proto_widget.path} widget type is {type(proto_widget.widget)}")

                if value:
                    if isinstance(proto_widget.widget, QComboBox):
                        proto_widget.widget.setCurrentText(str(value))
                    elif isinstance(proto_widget.widget, QDoubleSpinBox):
                        proto_widget.widget.setValue(float(value))
                    elif isinstance(proto_widget.widget, (BigIntSpinbox, QSpinBox)):
                        proto_widget.widget.setValue(int(value))
                    elif isinstance(proto_widget.widget, QLineEdit):
                        proto_widget.widget.setText(str(value))
                    else:
                        print(f"{proto_widget.path} widget type is {type(proto_widget.widget)}")

    def custom_protobuf_ui_by_config(self, protobuf_ui_config: dict):
        if len(protobuf_ui_config.keys()) == 0:
            return

        for proto_class_name in protobuf_ui_config.keys():
            if proto_class_name not in self.component_widget_dict.keys():
                continue
            title_keys = list(protobuf_ui_config[proto_class_name].keys())
            for proto_widget in self.component_widget_dict[proto_class_name].proto_widget_list:
                if str(proto_widget.path) not in title_keys:
                    continue
                custom_ui_config = protobuf_ui_config[proto_class_name][str(proto_widget.path)]
                enable = custom_ui_config.get("enable", True)
                selected = custom_ui_config.get("selected", False)
                show = custom_ui_config.get("show", True)
                value = custom_ui_config.get("value")
                _range = custom_ui_config.get("range", None)  # Only for QSpinBox and QDoubleSpinBox

                if not isinstance(proto_widget.selectable_widget, QCheckBox):
                    print(f"{proto_widget.path} widget type is not QCheckBox")
                    continue

                proto_widget.selectable_widget.setEnabled(enable)
                proto_widget.selectable_widget.setVisible(show)
                proto_widget.selectable_widget.setChecked(selected)

                proto_widget.widget.setEnabled(enable)
                proto_widget.widget.setVisible(show)

                if isinstance(_range, list) and len(_range) == 2:
                    if isinstance(proto_widget.widget, QDoubleSpinBox):
                        proto_widget.widget.setRange(float(_range[0]), float(_range[1]))
                    elif isinstance(proto_widget.widget, (BigIntSpinbox, QSpinBox)):
                        proto_widget.widget.setRange(int(_range[0]), int(_range[1]))
                    else:
                        print(f"{proto_widget.path} widget type is {type(proto_widget.widget)}")

                if value:
                    if isinstance(proto_widget.widget, QComboBox):
                        proto_widget.widget.setCurrentText(str(value))
                    elif isinstance(proto_widget.widget, QDoubleSpinBox):
                        proto_widget.widget.setValue(float(value))
                    elif isinstance(proto_widget.widget, (BigIntSpinbox, QSpinBox)):
                        proto_widget.widget.setValue(int(value))
                    elif isinstance(proto_widget.widget, QLineEdit):
                        proto_widget.widget.setText(str(value))
                    else:
                        print(f"{proto_widget.path} widget type is {type(proto_widget.widget)}")

    # --------------------------分享给子类可调用的api-------------------------------------------------
