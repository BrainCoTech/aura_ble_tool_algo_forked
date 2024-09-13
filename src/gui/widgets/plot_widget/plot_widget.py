__all__ = ["PlotQTWidget", "PlotWidgetWith2Y", "SingleCurvesInOnePlot", "MultiCurvesInOnePlot"]

import numpy as np
from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QMenu, QMenuBar
from pyqtgraph import PlotWidget, ViewBox, PlotCurveItem, LegendItem, mkPen

from .info_text_widget import InfoTextEdit
from .update_curves_dialog import UpdateCurvesDialog
from ....utils.filter_sdk import BWBandStopFilter, BWBandPassFilter
from ....utils.images import SETTINGS_IMG_BASE64, SETTINGS_IMG_1_BASE64
from ....utils.public_func import get_pixmap, calculate_fft


class PlotBase(PlotWidget):
    def __init__(self, title, show_grid=True):
        super(PlotBase, self).__init__(title=title)
        self.setBackground('k')
        self.title = title
        self.show_grid = show_grid

        if show_grid:
            self.showGrid(x=True, y=True, alpha=0.7)

        self.getAxis('left').setTextPen(mkPen(color="w"))
        self.getAxis('bottom').setTextPen(mkPen(color="w"))

        # self.setXRange(0, 500, padding=0)  # 通过 padding=0 可设置x轴0点和y轴0点重合

        # 设置刻度文本字体大小
        # font = QFont()
        # font.setBold(True)
        # font.setPointSize(9)
        # self.getAxis('left').setTickFont(font)

        self.curve_list = []

    def add_legend(self):
        if self.curve_list:
            legend = LegendItem((80, 60), offset=(70, 20))
            legend.setParentItem(self.plotItem)

            for idx, curve in enumerate(self.curve_list):
                legend.addItem(self.curve_list[idx], curve.name())

    def update_xy(self, x_values, y_values):
        if not len(self.curve_list):
            return

        for idx, curve in enumerate(self.curve_list):
            if y_values.ndim == 1:
                curve.setData(x_values, y_values)
            else:
                curve.setData(x_values[idx], y_values[idx])

    def copy(self):
        raise NotImplemented("Not implemented in subclass")


# 带左右两个Y轴
class PlotWidgetWith2Y(PlotBase):

    def __init__(self, title, label1, label2, range1=None, range2=None):
        super(PlotWidgetWith2Y, self).__init__(title=title, show_grid=True)
        self.label1 = label1
        self.label2 = label2
        self.range1 = range1
        self.range2 = range2

        p1_item = self.plotItem
        p2_item = ViewBox()
        p1_item.showAxis('right')
        p1_item.scene().addItem(p2_item)
        p1_item.getAxis('right').linkToView(p2_item)
        p2_item.setXLink(p1_item)
        self.getAxis('left').setLabel(label1, color="#ff0000")
        p1_item.getAxis('right').setLabel(label2, color="#0000ff")
        self.curve1 = p1_item.plot(pen=mkPen(color=QColor(255, 0, 0)), name=label1)
        self.curve2 = PlotCurveItem(pen=mkPen(color=QColor(0, 255, 255)), name=label2)
        p2_item.addItem(self.curve2)
        self.plot_widgets = [p1_item, p2_item]
        self.update_plot_size()
        p1_item.getViewBox().sigResized.connect(self.update_plot_size)

        if range1:
            self.setYRange(*range1)
        if range2:
            p2_item.setYRange(*range2)

        self.curve_list = [self.curve1, self.curve2]
        self.add_legend()

    def update_plot_size(self):
        self.plot_widgets[1].setGeometry(self.plot_widgets[0].getViewBox().sceneBoundingRect())
        self.plot_widgets[1].linkedViewChanged(self.plot_widgets[0].getViewBox(), self.plot_widgets[1].XAxis)

    def copy(self):
        instance = PlotWidgetWith2Y(self.title, self.label1, self.label2, self.range1, self.range2)
        return instance


class SingleCurvesInOnePlot(PlotBase):
    def __init__(self, title):
        super(SingleCurvesInOnePlot, self).__init__(title, show_grid=True)

        self.curve = self.plot(pen=mkPen(color=QColor(0, 0, 255)))
        self.curve_list = [self.curve]

    def copy(self):
        instance = SingleCurvesInOnePlot(self.title)
        return instance


class MultiCurvesInOnePlot(PlotBase):
    def __init__(self, title, labels, colors):
        super(MultiCurvesInOnePlot, self).__init__(title=title, show_grid=True)
        self.labels = labels
        self.colors = colors

        self.checkboxes = []
        for label, color, unused_col in zip(labels, colors, range(len(labels))):
            curve = self.plot(pen=mkPen(color=color), name=label)
            self.curve_list.append(curve)
        self.add_legend()

    def copy(self):
        instance = MultiCurvesInOnePlot(self.title, self.labels, self.colors)
        return instance


class PlotQTWidget(QWidget):
    instance_collection = []

    def __init__(self, sample_rate, plot: PlotBase, default_bs_cut_config=(4, 49, 51), parent=None):
        PlotQTWidget.instance_collection.append(self)

        super(PlotQTWidget, self).__init__(parent)
        self.sample_rate = sample_rate
        self.filters = []
        self.add_bs_filter(default_bs_cut_config[0], default_bs_cut_config[1], default_bs_cut_config[2])

        self.g_layout = QGridLayout()
        self.h_layout = QHBoxLayout()
        self.setLayout(self.g_layout)
        self.plot = plot

        self._info_text_edit = InfoTextEdit(title=self.plot.plotItem.titleLabel.text, parent=self)
        self._info_text_edit.setVisible(False)
        self.menu = QMenu(self.plot)
        self.menu.setIcon(QIcon(get_pixmap(SETTINGS_IMG_BASE64)))
        menubar = QMenuBar(self.plot)
        menubar.setStyleSheet("background-color:rgb(255, 255, 255);")
        # menubar.setMaximumWidth(40)
        menubar.addMenu(self.menu)
        self.h_layout.addWidget(self._info_text_edit)
        self.g_layout.addLayout(self.h_layout, 0, 0, 1, 1)
        self.g_layout.addWidget(menubar)
        self.g_layout.addWidget(self.plot)

        self.show_info_action = self.menu.addAction("Tips", self._on_info_edit_visible)
        self.show_info_action.setCheckable(True)
        self.show_info_action.setChecked(False)
        self.filter_enable_action = self.menu.addAction("Filter")
        self.filter_enable_action.setCheckable(True)
        self.filter_enable_action.setChecked(False)
        self.fft_enable_action = self.menu.addAction("FFT")
        self.fft_enable_action.setCheckable(True)
        self.fft_enable_action.setChecked(False)
        self.setting_curves_action = self.menu.addAction("Curves", self._on_reset_curves_dialog)

        self.append_info_to_edit(title="Amplitude", text_rgb=(160, 82, 45), text_wh=(100, 50))

        self.child_plot = plot.copy()

        self.update_curves_dialog = UpdateCurvesDialog(title=self.plot.plotItem.titleLabel.text,
                                                       curves=self.plot.curve_list,
                                                       parent=self)

    def translate_ui(self):
        self.show_info_action.setText(self.tr("Tips"))
        self.filter_enable_action.setText(self.tr("Filter"))
        self.fft_enable_action.setText(self.tr("FFT"))
        self.setting_curves_action.setText(self.tr("Curves"))
        self.update_curves_dialog.translate_ui()

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        if not self.child_plot.isVisible():
            self.child_plot.show()
        else:
            self.child_plot.raise_()

    def add_bs_filter(self, order, lowcut, highcut):
        bs = BWBandStopFilter(order, self.sample_rate, lowcut, highcut)
        self.filters.append(bs)

    def add_bp_filter(self, order, lowcut, highcut):
        bp = BWBandPassFilter(order, self.sample_rate, lowcut, highcut)
        self.filters.append(bp)

    def _on_info_edit_visible(self):
        self._info_text_edit.setVisible(not self._info_text_edit.isVisible())

    def _on_reset_curves_dialog(self):
        self.update_curves_dialog.move(self.mapToGlobal(self.rect().center()) - self.update_curves_dialog.rect().center())
        self.update_curves_dialog.show()

    def append_info_to_edit(self, title, text_rgb=None, text_wh=None):
        """

        Args:
            title:
            text_rgb:
            text_wh:

        Returns:

        """
        self._info_text_edit.append_info(title, text_rgb, text_wh)

    def _update_info_edit(self, title, text):
        self._info_text_edit.update_info(title, text)

    def update_data(self, y_values, x_values=None):
        if not isinstance(y_values, np.ndarray):
            y_values = np.array(y_values)

        # y_values的阶数必须是1或2
        if y_values.ndim > 2:
            raise Exception("不支持的数组维度")

        if x_values is None:
            # 多条曲线共用一条x轴，或者一条曲线用一条x轴
            # 所以无论y_values是一维还是二维数组，x_values都是一维数组
            if y_values.ndim == 1:
                x_values = np.arange(len(y_values))
            else:
                x_values = [np.arange(len(data)) for data in y_values]

        if self.show_info_action.isChecked():
            if y_values.size > 0:
                min_value = round(y_values.min(), 2)
                max_value = round(y_values.max(), 2)
                self._update_info_edit(title=f"Amplitude", text=f"[{min_value} ~ {max_value}]")

        if self.filter_enable_action.isChecked():
            if y_values.ndim == 1:
                for i, value in np.ndenumerate(y_values):
                    for _filter in self.filters:
                        value = _filter.filter(value)
                    y_values[i] = value
            else:
                for (i, j), value in np.ndenumerate(y_values):
                    for _filter in self.filters:
                        value = _filter.filter(value)
                    y_values[i][j] = value

        if self.fft_enable_action.isChecked():
            if y_values.ndim == 1:
                x_values, y_values = calculate_fft(y_values, self.sample_rate)
            else:
                freq, fft = [], []
                for data in y_values:
                    _freq, _fft = calculate_fft(data, self.sample_rate)
                    freq.append(_freq)
                    fft.append(_fft)
                x_values, y_values = freq, fft

            x_values = np.array(x_values)
            y_values = np.array(y_values)

        if self.child_plot.isVisible():
            self.child_plot.update_xy(x_values, y_values)
        else:
            self.plot.update_xy(x_values, y_values)
