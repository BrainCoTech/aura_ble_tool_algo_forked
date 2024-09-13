from enum import Enum

from PySide6.QtWidgets import QComboBox, QLineEdit, QDoubleSpinBox, QCheckBox, QGroupBox, QGridLayout, \
    QAbstractSpinBox, QTableWidget, QSpinBox, QVBoxLayout, QAbstractItemView, QHeaderView, QWidget, QHBoxLayout, \
    QToolButton, QFileDialog, QPushButton, QLabel
from PySide6.QtCore import QObject, QSize, Signal, Qt, QRegularExpression
from PySide6.QtGui import QIcon, QMouseEvent, QRegularExpressionValidator
from google.protobuf.descriptor import FieldDescriptor
from loguru import logger

from ...utils.public_func import get_pixmap
from ...utils.images import ADD_IMG_BASE64, DELETE_IMG_BASE64, FILE_IMG_BASE64, SELECT_ALL_IMG_BASE64, \
    DIS_SELECT_ALL_IMG_BASE64

REGEX_BYTES = r"[A-Fa-f0-9\s]+"
REGEX_REPEATED_INT = r"[0-9\,]+"

CONTROL_HEIGHT = 24
TOOL_BUTTON_SIZE = (20, 20)


# pylint: disable=no-member


"""
当需要在外部对RepeatListWidget和RepeatGroupBox做一些限制时， 按照如下方式进行限制
    def custom_protobuf_ui(self):
        for proto_class_name in ["U_AppToMainUS", "U_AppToMtr"]:
            if proto_class_name not in self.component_widget_dict.keys():
                continue

            proto_loop_table_widget = None
            proto_set_pid_param_perm_widget = None

            for proto_widget in self.component_widget_dict[proto_class_name].proto_widget_list:
                if proto_widget.path == ['grip_loop_table_config', 'loop_table']:
                    proto_loop_table_widget = proto_widget.widget
                elif proto_widget.path == ['factory_req', 'set_pid_param_perm']:
                    proto_set_pid_param_perm_widget = proto_widget.widget.parent()

            if proto_loop_table_widget is not None:
                proto_loop_table_widget.init_table_count(min_row_count=4)
            if proto_set_pid_param_perm_widget is not None:
                proto_set_pid_param_perm_widget.init_groupbox_count(min_row_count=3)
"""


class ProtoCheckBox(QCheckBox):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)


class GroupBoxBase(QGroupBox):
    """
    增加标题窗口
    """

    def __init__(self, text, parent=None):
        super().__init__(parent)

        # 创建一个自定义的QWidget作为标题
        self.title_widget = QWidget()
        self.title_widget.setObjectName('titleWidget')
        # self.title_widget.setStyleSheet('background:transparent')
        self.title_widget.setFixedHeight(40)
        self.title_layout = QHBoxLayout(self.title_widget)
        self.title_layout.setContentsMargins(0, 2, 0, 0)
        self.title_label = QLabel(text)
        self.setLayout(QGridLayout(self))
        self.layout().addWidget(self.title_widget, 0, 0, 1, 2)

        style_sheet = """
            #titleWidget {
            background:transparent;
            border: 1px solid;
            border-color: transparent transparent gray transparent;
            }
        """
        self.setStyleSheet(style_sheet)

        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()

    def title(self) -> str:
        return self.title_label.text()

    def _resize_title_widget(self):
        boundary_width = 0
        self.title_widget.move(boundary_width, 0)
        self.title_widget.resize(self.width() - boundary_width * 2, self.title_widget.height())

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._resize_title_widget()


class MultipleSelectGroupBox(GroupBoxBase):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        self.is_select_all = False
        self.multiple_select_button = QPushButton(self)
        self.multiple_select_button.setFixedSize(TOOL_BUTTON_SIZE[0], TOOL_BUTTON_SIZE[1])
        self.multiple_select_button.setIconSize(QSize(TOOL_BUTTON_SIZE[0] - 2, TOOL_BUTTON_SIZE[1] - 2))
        self._set_select_button_style()

        self.multiple_select_button.clicked.connect(self._on_multiple_select_button_clicked)
        self.multiple_select_button.setToolTip("Multiple select")
        self.title_layout.insertWidget(1, self.multiple_select_button)

    def _set_select_button_style(self):
        if self.is_select_all:
            self.multiple_select_button.setIcon(QIcon(get_pixmap(SELECT_ALL_IMG_BASE64)))
        else:
            self.multiple_select_button.setIcon(QIcon(get_pixmap(DIS_SELECT_ALL_IMG_BASE64)))

    def _on_multiple_select_button_clicked(self):
        self.is_select_all = not self.is_select_all
        self._set_select_button_style()
        for widget in self.findChildren(ProtoCheckBox):
            if widget.parent() is self:
                widget.setChecked(self.is_select_all)

    def showEvent(self, event) -> None:
        total_widget_count = len(self.findChildren(ProtoCheckBox))
        if total_widget_count >= 3:
            self.multiple_select_button.setVisible(True)
        else:
            self.multiple_select_button.setVisible(False)


class EnableSelectGroupBox(GroupBoxBase):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        self.select_box = QCheckBox(self)
        self.title_layout.insertWidget(0, self.select_box)

    def isChecked(self) -> bool:
        return self.select_box.isChecked()

    def setChecked(self, checked: bool) -> None:
        self.select_box.setChecked(checked)


class CommonGroupBox(GroupBoxBase):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.title_label.setVisible(False)


class RepeatGroupBox(GroupBoxBase):  # 增加可添加按钮, 删除功能待优化
    add_btn_clicked_signal = Signal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.min_row_count = 1  # 可添加的最小行数
        self.max_row_count = None
        self._add_count = 1  #  默认已添加的行数

        self.operate_add_btn = QPushButton("+", self)
        self.operate_add_btn.setFixedSize(TOOL_BUTTON_SIZE[0], TOOL_BUTTON_SIZE[1])
        self.title_layout.addWidget(self.operate_add_btn)
        self.operate_add_btn.clicked.connect(self._add)

        self.setLayout(QGridLayout())

    def init_groupbox_count(self, min_row_count=1, max_row_count=None):
        self.min_row_count = min_row_count
        self.max_row_count = max_row_count
        if self.min_row_count > 1:
            for _ in range(self.min_row_count - 1):
                self._add()

    def _add(self):
        if self.max_row_count is None or self._add_count < self.max_row_count:
            self._add_count += 1
            self.add_btn_clicked_signal.emit()


class HexDataLineEdit(QLineEdit):
    # 点击  btn后选择文件 自动转化为 hex 写入控件

    btn_clicked_signal = Signal()

    def __init__(self, parent=None):
        super(HexDataLineEdit, self).__init__(parent)

        self.btn = QToolButton(self)
        self.btn.setIcon(QIcon(get_pixmap(FILE_IMG_BASE64)))
        self.btn.clicked.connect(self.on_btn)

        self.btn.installEventFilter(self)

        self.btn.setVisible(False)

    def on_btn(self):
        file = QFileDialog.getOpenFileName()[0]
        if file:
            with open(file, 'rb') as f:
                content = f.read()
                if len(content):
                    self.setText(str(content))
                    self.setToolTip("size: {}".format(len(content)))
                    self.setReadOnly(True)  # 如果是通过打开文件输入hex的则不能再通过手动输入数据，防止误触

    def mousePressEvent(self, event) -> None:
        self.setCursor(Qt.IBeamCursor)
        super(HexDataLineEdit, self).mousePressEvent(event)

    def eventFilter(self, watched, event) -> bool:
        if watched == self.btn:
            if event.type() == QMouseEvent.Type.HoverEnter:
                self.setCursor(Qt.ArrowCursor)
        return QWidget.eventFilter(self, watched, event)

    def _reset_btn_pos(self):
        self.btn.setGeometry(int(self.width() - self.btn.width() - 3), 3, self.height() - 5, self.height() - 5)
        self.btn.setIconSize(QSize(self.height() - 10, self.height() - 10))

    def resizeEvent(self, event) -> None:
        super(HexDataLineEdit, self).resizeEvent(event)
        self._reset_btn_pos()

    def showEvent(self, event) -> None:
        super(HexDataLineEdit, self).showEvent(event)
        self._reset_btn_pos()


class RepeatListWidget(QWidget):
    # 多行单列表格, 不能修改行号

    def __init__(self, field_descriptor, parent=None):
        super(RepeatListWidget, self).__init__(parent)
        self.min_row_count = 0
        self.max_row_count = None

        self.field_descriptor = field_descriptor
        self.tool_layout = QHBoxLayout()
        self.main_layout = QVBoxLayout()

        self.add_btn = QPushButton(self)
        self.add_btn.setText("+")
        # self.add_btn.setIcon(QIcon(get_pixmap(ADD_IMG_BASE64)))
        self.delete_btn = QPushButton(self)
        self.delete_btn.setText("-")
        # self.delete_btn.setIcon(QIcon(get_pixmap(DELETE_IMG_BASE64)))
        self.add_btn.setFixedSize(TOOL_BUTTON_SIZE[0], TOOL_BUTTON_SIZE[1])
        # self.add_btn.setIconSize(QSize(TOOL_BUTTON_SIZE[0]-4, TOOL_BUTTON_SIZE[0]-4))
        self.delete_btn.setFixedSize(TOOL_BUTTON_SIZE[0], TOOL_BUTTON_SIZE[1])
        # self.delete_btn.setIconSize(QSize(TOOL_BUTTON_SIZE[0]-4, TOOL_BUTTON_SIZE[0]-4))

        self.table_widget = QTableWidget(self)
        self.table_widget.setMinimumHeight(100)
        self.table_widget.setColumnCount(1)
        self.table_widget.verticalHeader().setDefaultSectionSize(CONTROL_HEIGHT)
        self.table_widget.horizontalHeader().setHidden(True)
        self.table_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.tool_layout.addWidget(self.add_btn)
        self.tool_layout.addWidget(self.delete_btn)
        self.tool_layout.addStretch()

        self.main_layout.addLayout(self.tool_layout)
        self.main_layout.addWidget(self.table_widget)

        self.setLayout(self.main_layout)
        self.layout().setContentsMargins(2, 2, 2, 2)

        self.add_btn.clicked.connect(self._add_row)
        self.delete_btn.clicked.connect(self._delete_row)

    def init_table_count(self, min_row_count=0, max_row_count=None):
        self.min_row_count = min_row_count
        self.max_row_count = max_row_count
        if self.min_row_count > 0:
            for _ in range(self.min_row_count):
                self._add_row()

    def _add_row(self):
        if self.max_row_count is None or self.table_widget.rowCount() < self.max_row_count:
            widget = create_widget_for_field(self.field_descriptor)
            self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
            self.table_widget.setCellWidget(self.table_widget.rowCount() - 1, 0, widget)

    def _delete_row(self):
        if self.table_widget.rowCount() <= self.min_row_count:
            return
        indexs = self.table_widget.selectedIndexes()
        if len(indexs) == 0:
            # 一个都没选则默认从最后一个开始删除
            if self.table_widget.rowCount() > 0:
                self.table_widget.removeRow(self.table_widget.rowCount() - 1)
        else:
            self.table_widget.removeRow(indexs[0].row())

    def get_all_data_list(self):
        data_list = []
        for row in range(self.table_widget.rowCount()):
            widget = self.table_widget.cellWidget(row, 0)
            if widget:
                data_list.append(self.get_widget_data(widget))
            else:
                print('widget is None')

        return data_list

    def get_row_data(self, row):
        widget = self.table_widget.cellWidget(row, 0)
        if widget:
            return self.get_widget_data(widget)
        else:
            raise Exception('widget is None')

    @staticmethod
    def get_widget_data(widget):
        if isinstance(widget, (QDoubleSpinBox, QSpinBox, BigIntSpinbox)):
            return widget.value()
        elif isinstance(widget, QLineEdit):
            return widget.text()
        elif isinstance(widget, QComboBox):
            return widget.currentData()
        else:
            raise Exception('暂时不支持表格插入别的控件类型')


class BigIntSpinbox(QAbstractSpinBox):
    # pylint: disable=invalid-name
    def __init__(self, parent=None):
        super(BigIntSpinbox, self).__init__(parent)
        self._singleStep = 1
        self._minimum = -18446744073709551616
        self._maximum = 18446744073709551615
        self.lineEdit = QLineEdit(self)
        self.lineEdit.textChanged.connect(self._value_changed)
        self.setLineEdit(self.lineEdit)
        self.lineEdit.setText(str(0))
        self._valid_text = "0"

    def _value_changed(self, text):
        def text_valid():
            try:
                value = int(text)
                return self._value_in_range(value)
            except Exception as unused_error:
                return False

        if text_valid():
            self._valid_text = text
        else:
            self.lineEdit.setText(self._valid_text)

    def setRange(self, min_num, max_num):
        self._minimum = min_num
        self._maximum = max_num

    def value(self):
        return int(self.lineEdit.text())

    def setValue(self, value):
        if self._value_in_range(value):
            self.lineEdit.setText(str(value))

    def _value_in_range(self, value):
        return self._minimum <= value <= self._maximum

    def stepBy(self, steps):
        self.setValue(self.value() + steps * self.singleStep())

    def stepEnabled(self):
        return self.StepEnabledFlag.StepUpEnabled | self.StepEnabledFlag.StepDownEnabled

    def singleStep(self):
        return self._singleStep


class ProtoWidget(QObject):
    # pyint: disable=too-many-branches, cell-var-from-loop
    def __init__(self, selectable_widget, widget, path, collection):
        super(ProtoWidget, self).__init__()
        self.selectable_widget = selectable_widget
        self.widget = widget
        self.path = path.copy()
        self.collection = collection

    def __str__(self):
        return "{}, {}, {}".format(self.path, self.widget, self.selectable_widget)

    def is_checked(self):
        if self.selectable_widget and hasattr(self.selectable_widget, 'isChecked'):
            return self.selectable_widget.isChecked()
        else:  # the widget is checked when one of its related widget is checked
            for related_widget in self.collection:
                if related_widget.is_checked():
                    return True
            return False

    def insert_value_to_message(self, proto_content):  # pylint: disable=too-many-branches
        field_name = self.path[-1]
        parent_field = proto_content
        for i in range(len(self.path) - 1):
            parent_field = getattr(parent_field, self.path[i])
        target_field = parent_field.DESCRIPTOR.fields_by_name[field_name]
        if target_field.type == FieldDescriptor.TYPE_MESSAGE:
            field = getattr(parent_field, field_name).add()
            for related_widget in self.collection:
                if related_widget.is_checked():
                    related_widget.insert_value_to_message(field)
        elif target_field.type in [FieldDescriptor.TYPE_INT64,
                                   FieldDescriptor.TYPE_UINT64,
                                   FieldDescriptor.TYPE_INT32,
                                   FieldDescriptor.TYPE_UINT32,
                                   FieldDescriptor.TYPE_FLOAT,
                                   FieldDescriptor.TYPE_DOUBLE]:
            if isinstance(self.widget, RepeatListWidget):
                for row in range(self.widget.table_widget.rowCount()):
                    value = self.widget.get_row_data(row)
                    set_value_to_field(parent_field, target_field, field_name, value)
            else:
                set_value_to_field(parent_field, target_field, field_name, self.widget.value())
        elif target_field.type == FieldDescriptor.TYPE_ENUM:
            if isinstance(self.widget, RepeatListWidget):
                for row in range(self.widget.table_widget.rowCount()):
                    value = self.widget.get_row_data(row)
                    set_value_to_field(parent_field, target_field, field_name, value)
            else:
                set_value_to_field(parent_field, target_field, field_name,
                                   target_field.enum_type.values_by_name[self.widget.currentText()].number)
        elif target_field.type == FieldDescriptor.TYPE_BOOL:
            if self.widget.currentText().upper() == "TRUE":
                set_value_to_field(parent_field, target_field, field_name, True)
            else:
                set_value_to_field(parent_field, target_field, field_name, False)
        elif target_field.type in [FieldDescriptor.TYPE_STRING,
                                   FieldDescriptor.TYPE_MESSAGE]:
            set_value_to_field(parent_field, target_field, field_name, self.widget.text())
        elif target_field.type == FieldDescriptor.TYPE_BYTES:
            set_value_to_field(parent_field, target_field, field_name, bytes.fromhex(self.widget.text()))
        return proto_content

    def set_value_to_widget(self, value):
        try:
            if issubclass(type(self.widget), QAbstractSpinBox):
                self.widget.setValue(value)
            elif issubclass(type(self.widget), QComboBox):
                if isinstance(value, str):
                    self.widget.setCurrentText(value)
                elif isinstance(value, int):
                    self.widget.setCurrentIndex(value)
                else:
                    print("data type error: {}".format(value))
            else:
                print(f"暂时不支持初始化这种控件1: {self.widget}")
        except Exception as e:
            logger.error(str(e) + "  value: {}  type: {}".format(value, type(value)), exc_info=True)

    def reset_widget(self):
        try:
            if issubclass(type(self.widget), QSpinBox):
                self.widget.setValue(0)
            elif issubclass(type(self.widget), QDoubleSpinBox):
                self.widget.setValue(0.)
            elif issubclass(type(self.widget), QLineEdit):
                self.widget.setText('')
            elif issubclass(type(self.widget), QComboBox):
                self.widget.setCurrentIndex(0)
            else:
                print('----------------------------------')
                print(self.selectable_widget.text(), self.path)
                print(self.widget)
                print("暂时不支持初始化这种控件2")
        except Exception as e:
            logger.error(str(e), exc_info=True)


def create_ui_for_proto(field, container, root, widget_list, groupbox_dict):  # pylint: disable=cell-var-from-loop
    sub_fields = field.DESCRIPTOR.fields
    sub_layout = container.layout()
    for i in range(len(sub_fields)):
        sub_field_name = sub_fields[i].name
        sub_field = getattr(field, sub_field_name)
        row = sub_layout.rowCount()
        if sub_fields[i].type != FieldDescriptor.TYPE_MESSAGE:
            if sub_fields[i].label == FieldDescriptor.LABEL_REPEATED:
                groupbox = EnableSelectGroupBox(sub_field_name)
                groupbox.setLayout(QVBoxLayout())
                sub_layout.addWidget(groupbox, row, 0, 1, 2)

                widget = RepeatListWidget(field_descriptor=sub_fields[i])
                groupbox.layout().addWidget(widget)
                path = root.copy()
                path.append(sub_field_name)
                groupbox_dict[str(path)] = groupbox
                widget_list.append(ProtoWidget(selectable_widget=groupbox, widget=widget, path=path, collection=[]))

            else:
                add_proto_widgets(field_name=sub_field_name, field_descriptor=sub_fields[i], container=container,
                                  path=root, widget_list=widget_list)

        else:
            path = root.copy()
            path.append(sub_field_name)

            if sub_fields[i].label == FieldDescriptor.LABEL_REPEATED:
                groupbox = RepeatGroupBox(text=sub_field_name)
                groupbox_dict[str(path)] = groupbox
                params = [sub_field.add(), groupbox, path.copy(), widget_list, groupbox_dict]
                groupbox.add_btn_clicked_signal.connect(lambda params=params: add_repeated_message(*params))
                add_repeated_message(*params)
            else:
                groupbox = MultipleSelectGroupBox(text=sub_field_name)
                groupbox_dict[str(path)] = groupbox
                create_ui_for_proto(sub_field, groupbox, path, widget_list, groupbox_dict)

            sub_layout.addWidget(groupbox, row, 0, 1, 2)


def add_proto_widgets(field_name, field_descriptor, container, path, widget_list):
    row = container.layout().rowCount()
    check_box = ProtoCheckBox(field_name)
    container.layout().addWidget(check_box, row, 0, 1, 1)
    widget = create_widget_for_field(field_descriptor)
    container.layout().addWidget(widget, row, 1, 1, 1)
    path = path.copy()
    path.append(field_name)
    widget_list.append(ProtoWidget(selectable_widget=check_box, widget=widget, path=path, collection=[]))


def add_repeated_message(field, container, path, widget_list, groupbox_dict):
    inner_groupbox = CommonGroupBox(text='')
    groupbox_dict[str(path)] = inner_groupbox
    QGridLayout(inner_groupbox)
    row = container.layout().rowCount()
    container.layout().addWidget(inner_groupbox, row, 0, 1, 2)
    widget_list.append(ProtoWidget(selectable_widget=None, widget=inner_groupbox, path=path, collection=[]))
    create_ui_for_proto(field, inner_groupbox, [], widget_list[-1].collection, groupbox_dict)


def set_value_to_field(parent_field, target_field, field_name, value):
    if target_field.label == FieldDescriptor.LABEL_REPEATED:
        field = getattr(parent_field, field_name)
        field.append(value)
    else:
        setattr(parent_field, field_name, value)


def create_widget_for_field(field):
    widget = None
    if field.type == FieldDescriptor.TYPE_ENUM:
        widget = QComboBox()
        for idx, enum_value in enumerate(field.enum_type.values):
            widget.addItem(enum_value.name, idx)
    elif field.type == FieldDescriptor.TYPE_BOOL:
        widget = QComboBox()
        widget.addItem("True", True)
        widget.addItem("False", False)
    elif field.type in [FieldDescriptor.TYPE_FLOAT,
                        FieldDescriptor.TYPE_DOUBLE]:
        widget = QDoubleSpinBox()
        widget.setDecimals(5)
        widget.setRange(-2000, 2000)
    elif field.type == FieldDescriptor.TYPE_INT32:
        widget = BigIntSpinbox()
        widget.setRange(-2 ** 31, 2 ** 31)
    elif field.type == FieldDescriptor.TYPE_INT64:
        widget = BigIntSpinbox()
        widget.setRange(-2 ** 63, 2 ** 63)
    elif field.type == FieldDescriptor.TYPE_UINT32:
        widget = BigIntSpinbox()
        widget.setRange(0, 2 ** 32)
    elif field.type == FieldDescriptor.TYPE_UINT64:
        widget = BigIntSpinbox()
        widget.setRange(0, 2 ** 64)
    elif field.type == FieldDescriptor.TYPE_STRING:
        widget = QLineEdit()
        widget.setPlaceholderText("string")
    elif field.type == FieldDescriptor.TYPE_BYTES:
        widget = HexDataLineEdit()
        reg_ex = QRegularExpression(REGEX_BYTES)
        validator = QRegularExpressionValidator(reg_ex)
        widget.setValidator(validator)
        widget.setPlaceholderText("hex")
    # pylint: disable=invalid-name
    if hasattr(widget, 'wheelEvent'):
        widget.wheelEvent = lambda event: None

    widget.setFixedHeight(CONTROL_HEIGHT)
    return widget
