import pprint

from loguru import logger
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDockWidget, QWidget, QScrollArea, QFrame, QGridLayout, \
    QAbstractScrollArea, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox
from PySide6.QtCore import Qt, Signal

from .protobuf_widget import create_ui_for_proto
from ...config.register_proto import get_proto_class
from ...core.tool_packet import ToolPacket
from ...utils.images import REFRESH_IMG_BASE64
from ...utils.public_func import get_pixmap


class CommonDockWidget(QDockWidget):
    def __init__(self, enable_double_click=True, show_title=True):
        """

        Args:
            enable_double_click: if True, double click to maximize the window
            show_title: if True, show title bar, all features are disabled
        """
        super(CommonDockWidget, self).__init__()

        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setContentsMargins(0, 0, 0, 0)

        self.enable_double_click = enable_double_click
        self.show_title = show_title

        if not show_title:
            # 关闭标题栏后所有特性 “可移动” ,"浮动"等都失效
            title_bar = self.titleBarWidget()
            self.setTitleBarWidget(QWidget())
            del title_bar

    def mouseDoubleClickEvent(self, event) -> None:
        if self.enable_double_click:
            if self.isMaximized():
                self.showNormal()
            else:
                if not self.isFloating():
                    self.setFloating(True)
                self.showMaximized()

            self.raise_()
        super(CommonDockWidget, self).mouseDoubleClickEvent(event)


class ProtoConfigDockWidget(QDockWidget):

    def __init__(self, proto_class_str, send_command_func, source_id=None, destination_id=None, flag=None, parent=None):
        super().__init__(parent)
        self.proto_widget_list = []
        self.proto_groupbox_dict = {}
        self.proto_class_str = proto_class_str
        self.source_id = source_id
        self.destination_id = destination_id
        self.flag = flag
        self.send_command_func = send_command_func

        # create main widget
        widget = create_scroll_widget()
        create_ui_for_proto(get_proto_class(proto_class_str)(), widget.main_widget, [], self.proto_widget_list, self.proto_groupbox_dict)
        button_send_command = QPushButton("Send Command", widget)  # send btn
        button_send_command.clicked.connect(self.on_send_command_button)
        widget.layout().addWidget(button_send_command)
        self.setWidget(widget)

        title_bar = self.titleBarWidget()
        self.setTitleBarWidget(QWidget())
        del title_bar

    def __set_value_to_field(self, field):
        for widget in self.proto_widget_list:
            if widget.is_checked():
                widget.insert_value_to_message(field)

    def on_send_command_button(self):
        proto_obj = get_proto_class(self.proto_class_str)()
        self.__set_value_to_field(proto_obj)
        msg = ToolPacket(payload=proto_obj.SerializeToString(),
                         source_id=self.source_id,
                         destination_id=self.destination_id)
        logger.info("{}\n{}".format(self.proto_class_str, proto_obj))
        logger.info("{}".format(msg.encode()))
        self.send_command_func(msg.encode())


class ProtoDataDockWidget(QDockWidget):
    request_data_signal = Signal()

    def __init__(self, proto_class_str, parent=None):
        super().__init__(parent)
        self.proto_widget_list = []
        self.proto_class_str = proto_class_str

        # create main widget
        widget = create_scroll_widget()
        create_ui_for_proto(get_proto_class(proto_class_str)(), widget.main_widget, [], self.proto_widget_list, self.proto_groupbox_dict)

        layout = QHBoxLayout()
        layout.addStretch()
        button_send_command = QPushButton(widget)  # send btn
        button_send_command.setIcon(QIcon(get_pixmap(REFRESH_IMG_BASE64)))
        button_send_command.setFixedSize(32, 32)
        button_send_command.clicked.connect(self.on_send_command_button)
        layout.addWidget(button_send_command)
        widget.layout().addLayout(layout)
        self.setWidget(widget)

        title_bar = self.titleBarWidget()
        self.setTitleBarWidget(QWidget())
        del title_bar

    def on_send_command_button(self):
        self.request_data_signal.emit()

    def insert_value_to_widget(self, init_dict: dict):
        for proto_widget in self.proto_widget_list:
            if str(proto_widget.path) in init_dict.keys():
                value = init_dict[str(proto_widget.path)]

                if isinstance(proto_widget.widget, QComboBox):
                    if not isinstance(value, int):
                        status_text = f"{'.'.join(proto_widget.path)}: {value}  "
                        print("控件是 QComboBox， 返回数据必须是int类型\n{}".format(status_text))
                        continue
                proto_widget.set_value_to_widget(value)


def create_scroll_widget():
    main_widget = QWidget()
    main_widget.setLayout(QVBoxLayout())

    scroll_area = QScrollArea()
    scroll_area.setFrameShape(QFrame.Shape.NoFrame)
    scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
    scroll_area.setWidgetResizable(True)

    widget = QWidget()
    widget.setLayout(QGridLayout())
    scroll_area.setWidget(widget)
    main_widget.layout().addWidget(scroll_area)

    setattr(main_widget, "main_widget", widget)

    return main_widget
