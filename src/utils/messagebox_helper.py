

from loguru import logger
from PySide6.QtWidgets import QMessageBox


class MessageBoxHelper(QMessageBox):
    def __init__(self, parent=None):
        super(MessageBoxHelper, self).__init__(parent)
        self.parent = parent
        self.MsgOkRole = 0

    def show_info_box(self, info):
        logger.info(info)
        msg = QMessageBox(self.parent)
        msg.setWindowTitle(self.tr("Message"))
        msg.setText(info)
        msg.setIcon(QMessageBox.Information)
        yes_btn = msg.addButton(QMessageBox.Yes)
        yes_btn.setText(self.tr('OK'))
        msg.exec_()

    def show_question_box(self, info):
        logger.info(info)
        msg = QMessageBox(self.parent)
        msg.setWindowTitle(self.tr("Question"))
        msg.setText(info)
        msg.setIcon(QMessageBox.Question)
        yes_btn = msg.addButton(QMessageBox.Yes)
        cancel_btn = msg.addButton(QMessageBox.Cancel)

        yes_btn.setText(self.tr('Confirm'))
        cancel_btn.setText(self.tr('Cancel'))
        msg.setDefaultButton(yes_btn)
        return msg.exec_()

    def show_error_box(self, info, error=None):
        logger.exception("\n" + info)
        msg = QMessageBox(self.parent)
        msg.setWindowTitle(self.tr("Error"))
        msg.setText(info)
        msg.setIcon(QMessageBox.Critical)
        yes_btn = msg.addButton(QMessageBox.Yes)
        yes_btn.setText(self.tr('Confirm'))
        msg.exec_()

    def show_warning_box(self, info):
        logger.warning(info)
        msg = QMessageBox(self.parent)
        msg.setWindowTitle(self.tr("Warning"))
        msg.setText(info)
        msg.setIcon(QMessageBox.Warning)
        yes_btn = msg.addButton(QMessageBox.Yes)
        yes_btn.setText(self.tr('Confirm'))
        msg.exec_()

    def show_save_question_box(self, info):
        logger.info(info)
        msg = QMessageBox(self.parent, )
        msg.setWindowTitle(self.tr("Question"))
        msg.setText(info)
        msg.setIcon(QMessageBox.Question)
        cancel_btn = msg.addButton(QMessageBox.Cancel)
        yes_btn = msg.addButton(QMessageBox.Yes)
        no_btn = msg.addButton(QMessageBox.No)

        cancel_btn.setText(self.tr('Cancel'))
        yes_btn.setText(self.tr('Yes'))
        no_btn.setText(self.tr('No'))
        msg.setDefaultButton(yes_btn)
        return msg.exec_()

