import os
import sys

from PySide6.QtCore import QEvent, Qt
from loguru import logger
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from src.utils.path import APP_ROOT_PATH
from src.config.settings import PROTO_CONFIG, TOOL_CONFIG
from src.config.register_proto import register_proto_class, list_proto_class


def register_proto():
    _PROTO_PATH_STRUCTURE = PROTO_CONFIG["proto_path_structure"]
    _PACK_TYPE = "-F"
    if getattr(sys, 'frozen', False):  # 打包
        if _PACK_TYPE == '-D':
            proto_path = os.path.realpath(os.path.join(APP_ROOT_PATH, *_PROTO_PATH_STRUCTURE[1]))
        else:
            exe_temp_path = sys._MEIPASS  # TEMP
            proto_path = os.path.realpath(os.path.join(exe_temp_path, *_PROTO_PATH_STRUCTURE[1]))
    elif __file__:  # 非打包
        proto_path = os.path.join(APP_ROOT_PATH, *_PROTO_PATH_STRUCTURE[0], *_PROTO_PATH_STRUCTURE[1])

    print("PROTO_PYTHON_PATH:", proto_path)
    sys.path.append(proto_path)

    # 递归添加所有proto文件夹
    for root, dirs, files in os.walk(proto_path):
        for _dir in dirs:
            sys.path.append(os.path.join(root, _dir))

    if not os.path.exists(proto_path):
        raise FileNotFoundError(f"proto_path : {proto_path} not exists")
    register_proto_class(proto_path)
    print(list_proto_class())


class MyApplication(QApplication):

    def notify(self, receiver, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape:
            return True
        return super(MyApplication, self).notify(receiver, event)


register_proto()

from src.gui.gui import Gui
from src.utils.loguru_settings import setup_loguru


if __name__ == "__main__":
    setup_loguru(log_folder_path="log")
    logger.info("============================== Programme Start ==============================")
    app = MyApplication(sys.argv)

    apply_stylesheet(app, "dark_teal.xml")
    stylesheet = app.styleSheet()
    with open(os.path.join(APP_ROOT_PATH, "custom.css")) as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    win = Gui()
    win.show()
    result = app.exec()
    logger.info("============================== Programme End ==============================")
    sys.exit(result)
