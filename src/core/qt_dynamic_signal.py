# -*- coding: utf-8 -*-
from typing import Callable

from PySide6.QtCore import QObject, Signal


class DynamicSignal(QObject):
    def __init__(self):
        super().__init__()
        self.real_signal = None

    def emit_signal(self, *args):
        if self.real_signal is None:
            raise Exception("real_signal not found, please bind signal first")
        self.real_signal.emit(*args)


class DynamicSignaCollection(object):
    signals = dict()

    def update(self, name: str, signal: DynamicSignal, slot: Callable):
        self.signals[name] = (signal, slot)

    def get(self, name: str):
        return self.signals.get(name, None)

    def remove(self, name: str):
        self.signals.pop(name, None)

    def clear(self):
        self.signals.clear()


dynamic_signal_collection = DynamicSignaCollection()


def bind_signal(signal_name: str, slot: Callable, data_type: tuple):
    class_dynamic_signal = getattr(DynamicSignal, signal_name, None)
    if class_dynamic_signal is not None:
        # 如果已经绑定过了，就绑定新的slot， 绑定之前先断开之前的slot
        # 1. 获取之前的signal和slot
        dynamic_signal, old_slot = dynamic_signal_collection.get(signal_name)
        # 2. 断开之前的slot
        dynamic_signal.real_signal.disconnect(old_slot)
        # 3. 绑定新的slot
        dynamic_signal.real_signal.connect(slot)
    else:
        # 如果没有绑定过，就绑定新的signal和slot
        signal = Signal(*data_type)
        setattr(DynamicSignal, signal_name, signal)

        dynamic_signal = DynamicSignal()
        dynamic_signal.real_signal = getattr(dynamic_signal, signal_name)
        dynamic_signal.real_signal.connect(slot)

    dynamic_signal_collection.update(signal_name, dynamic_signal, slot)
    return dynamic_signal