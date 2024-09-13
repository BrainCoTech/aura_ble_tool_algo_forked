# -*- coding: utf-8 -*-
from enum import IntEnum


class DeviceStatus(IntEnum):
    CONNECTED = 0
    DISCONNECTED = 1


class DeviceBase(object):
    device = None

    def __init__(self):
        pass

    def connect_to_device(self, *args, **kwargs):
        pass

    def disconnect_to_device(self, *args, **kwargs):
        pass

    def send_data_to_device(self, *args, **kwargs):
        pass

    def check_device_is_connected(self):
        pass
