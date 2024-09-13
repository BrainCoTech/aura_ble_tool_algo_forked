import datetime
from loguru import logger
from PySide6.QtWidgets import QDialog, QPushButton, QLabel, QRadioButton, QLineEdit, QTimeEdit, QGridLayout, \
    QDateTimeEdit, QWidget
from PySide6.QtCore import Qt, Signal, QTimer, QTime


class DataLoggerDialog(QDialog):
    # pylint: disable=invalid-name
    start_signal = Signal(str)
    stop_signal = Signal()

    def __init__(self, parent=None):
        super(DataLoggerDialog, self).__init__(parent)
        self.setMinimumWidth(400)
        self.setWindowTitle("data logger")
        self.setStyleSheet('''font: 11pt''')
        self.timer_label = QLabel("00:00:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet('''font: 30pt''')
        self.timer_radiobutton = QRadioButton("countdown")
        self.timer_timeedit = QTimeEdit()
        self.timer_timeedit.setDisplayFormat("HH:mm:ss")
        self.timer_timeedit.setCurrentSection(QDateTimeEdit.Section.SecondSection)
        self.label_lineedit = QLineEdit()
        self.start_button = QPushButton("start")
        self.start_button.clicked.connect(self.on_clicked_start)
        self.stop_button = QPushButton("stop")
        self.stop_button.clicked.connect(self.on_clicked_stop)
        self.path_label = QLabel()
        self.path_label.setStyleSheet('font-size: 10px')

        self.setLayout(QGridLayout())
        # pylint: disable=no-member
        self.layout().addWidget(self.timer_label, 0, 0, 1, 2)
        self.layout().addWidget(self.timer_radiobutton, 1, 0, 1, 1)
        self.layout().addWidget(self.timer_timeedit, 1, 1, 1, 1)
        self.layout().addWidget(self.label_lineedit, 2, 0, 1, 2)
        self.layout().addWidget(self.start_button, 3, 0, 1, 1)
        self.layout().addWidget(self.stop_button, 3, 1, 1, 1)
        self.layout().addWidget(self.path_label, 4, 0, 1, 2)

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_timeout)
        self.timer.setInterval(100)

        self.data_duration = 0
        self.stop_button.setEnabled(False)
        self.start_time = datetime.datetime.now()

    def translate_ui(self):
        self.stop_button.setText(self.tr("stop"))
        self.start_button.setText(self.tr("start"))

    def on_timer_timeout(self):
        now = datetime.datetime.now()
        duration = (now - self.start_time).seconds
        m, s = divmod(duration, 60)
        h, m = divmod(m, 60)
        self.timer_label.setText('{:02d}:{:02d}:{:02d}'.format(h, m, s))
        if self.data_duration and duration >= self.data_duration:
            self.on_clicked_stop()

    def on_clicked_start(self):
        self.start_signal.emit(self.label_lineedit.text())
        self.timer.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.start_time = datetime.datetime.now()
        duration = self.timer_timeedit.time()
        if self.timer_radiobutton.isChecked() and duration != QTime(0, 0, 0):
            self.data_duration = datetime.timedelta(hours=duration.hour(),
                                                    minutes=duration.minute(),
                                                    seconds=duration.second()).seconds
            logger.info("timer duration: {}".format(self.data_duration))

    def on_clicked_stop(self):
        self.timer.stop()
        self.stop_signal.emit()
        self.data_duration = 0
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = DataLoggerDialog()
    win.show()
    sys.exit(app.exec_())
