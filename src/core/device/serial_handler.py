import time
from concurrent.futures import ThreadPoolExecutor
from enum import Enum, IntEnum
from threading import Thread

import serial
from loguru import logger

from ...core.device.base import DeviceBase, DeviceStatus


class SerialModeConstant(Enum):
    ascii = 1
    hex = 2


class SerialConfig(object):
    def __init__(self, port: str, baud_rate: int, bytesize: int, parity: str, stop_bits: int, timeout: float):
        self.port = port
        self.baud_rate = baud_rate
        self.bytesize = bytesize
        self.parity = parity
        self.stop_bits = stop_bits
        self.timeout = timeout


class SerialHandler(DeviceBase):
    _on_dev_status = None
    _on_recv_data = None

    _keep_running = True

    def __init__(self):
        super(SerialHandler, self).__init__()
        self._thread_pool = ThreadPoolExecutor(max_workers=1)

    def check_device_is_connected(self):
        if isinstance(self.device, serial.Serial):
            return self.device.is_open
        return False

    def set_callbacks(self, on_recv_data=None, on_dev_status=None):
        if on_recv_data:
            self._on_recv_data = on_recv_data
        if on_dev_status:
            self._on_dev_status = on_dev_status

    def run(self) -> None:
        while self._keep_running:
            if not self.check_device_is_connected():
                time.sleep(0.5)
                continue
            try:
                count = self.device.inWaiting()
                if count:
                    rec_datum = self.device.read(count)
                    if self._on_recv_data:
                        self._on_recv_data(rec_datum)
                else:
                    time.sleep(0.05)
            except serial.serialcli.SerialException as e:
                logger.error(str(e), exc_info=True)

    def connect_to_device(self, cfg: SerialConfig):
        try:
            device = serial.Serial()
            device.port = cfg.port
            device.baudrate = cfg.baud_rate
            device.bytesize = cfg.bytesize
            device.parity = cfg.parity
            device.stopbits = cfg.stop_bits
            device.timeout = cfg.timeout

            if not device.is_open:
                device.open()
            self.device = device
            self.device.flushInput()
            self.device.flushOutput()

            self._keep_running = True
            self._thread_pool.submit(self.run)

            if self._on_dev_status:
                self._on_dev_status(DeviceStatus.CONNECTED, "")

        except Exception as e:
            self.device = None
            self._keep_running = False
            raise Exception('connect serial error: ' + str(e))

    def disconnect_to_device(self):
        self._keep_running = False
        try:
            if self.device:
                self.device.close()
        except Exception as e:
            logger.error('disconnect serial error: ' + str(e), exc_info=True)
        finally:
            self.device = None
            if self._on_dev_status:
                self._on_dev_status(DeviceStatus.DISCONNECTED, "")

    def send_data_to_device(self, data):
        if not self.device:
            return
        if not isinstance(data, bytes):
            data = bytes(data, encoding='utf-8')
        logger.info("serial sent:" + str(data))
        self._raw_serial_writer(data)

    def _raw_serial_writer(self, data: bytes):
        try:
            self.device.write(data)
        except serial.SerialTimeoutException:
            logger.error("write timeout", exc_info=True)
