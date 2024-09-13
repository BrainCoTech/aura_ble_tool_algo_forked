import asyncio
import pprint
from enum import IntEnum
from threading import Thread
from typing import Callable

from bleak import BleakClient, BleakScanner
from loguru import logger

from .base import DeviceBase, DeviceStatus


_SCAN_TIMEOUT_S = 3


MANUFACTURER = "Manufacturer"
MODEL_NUMBER = "Model Number"
SERIAL_NUMBER = "Serial Number"
HARDWARE_REVISION = "Hardware Version"
FIRMWARE_REVISION = "Firmware Version"
BATTERY = "Battery"

DEFAULT_UUID = {
    MANUFACTURER: "00002a29-0000-1000-8000-00805f9b34fb",
    MODEL_NUMBER: "00002a24-0000-1000-8000-00805f9b34fb",
    HARDWARE_REVISION: "00002a27-0000-1000-8000-00805f9b34fb",
    FIRMWARE_REVISION: "00002a26-0000-1000-8000-00805f9b34fb",
    SERIAL_NUMBER: "00002a25-0000-1000-8000-00805f9b34fb",
    BATTERY: "00002a19-0000-1000-8000-00805f9b34fb"}


class BleStatus(IntEnum):
    ENABLED = 0
    ENABLED_FAILED = 1
    STOPPED = 2


class BleHandler(DeviceBase):
    _on_ble_status = None
    _on_dev_status = None
    _on_scan_result = None
    _on_get_ble_info = None
    _on_recv_data = None

    def __init__(self, service_uuid, tx_uuid, rx_uuid):
        super().__init__()
        self._service_uuid = service_uuid
        self._tx_uuid = tx_uuid
        self._rx_uuid = rx_uuid

        self._event_loop = asyncio.new_event_loop()
        self._thread = Thread(target=self._start_event_loop)
        self._thread.setDaemon(True)
        self._thread.start()

    def check_device_is_connected(self):
        if isinstance(self.device, BleakClient):
            return self.device.is_connected
        return False

    def set_callbacks(self, on_recv_data=None, on_ble_status=None, on_dev_status=None,
                      on_scan_result=None, on_get_ble_info=None):
        """
        Set callbacks for ble handler.
        Args:
            on_recv_data: Set callback for receiving data.
            on_ble_status: Set callback for ble status.
            on_dev_status: Set callback for device status.
            on_scan_result: Set callback for scan result.
            on_get_ble_info: Set callback for ble info.

        Returns:

        """
        if on_recv_data:
            self._on_recv_data = on_recv_data
        if on_ble_status:
            self._on_ble_status = on_ble_status
        if on_dev_status:
            self._on_dev_status = on_dev_status
        if on_scan_result:
            self._on_scan_result = on_scan_result
        if on_get_ble_info:
            self._on_get_ble_info = on_get_ble_info

    def _start_event_loop(self):
        asyncio.set_event_loop(self._event_loop)
        self._event_loop.run_forever()

    def _disconnection_callback(self, client: BleakClient):
        logger.info('disconnect callback')
        if self._on_dev_status:
            self._on_dev_status(DeviceStatus.DISCONNECTED, "")
        self.device = None

    def _notify_nus_callback(self, sender, data):
        if self._on_recv_data:
            self._on_recv_data(data)

    async def _scan(self):
        try:
            devices = await BleakScanner.discover(timeout=_SCAN_TIMEOUT_S)

            discover_devices = []
            for dev in devices:
                if dev.name and self._service_uuid in dev.metadata["uuids"]:
                    discover_devices.append(dev)
            if self._on_scan_result:
                self._on_scan_result(discover_devices)
        except Exception as error:
            logger.error(str(error), exc_info=True)
            if self._on_ble_status:
                self._on_ble_status(BleStatus.ENABLED_FAILED, str(error))

    async def _connect(self, address):
        msg = ""
        try:
            logger.info("target device: {}".format(address))
            device = BleakClient(address, disconnected_callback=self._disconnection_callback)
            status = await device.connect()
        except (asyncio.TimeoutError, asyncio.CancelledError, Exception) as error:
            logger.error(str(error), exc_info=True)
            msg = str(error)
            status = False
            device = None

        if status:
            self.device = device
            self._read_default_device_info()
        if self._on_dev_status:
            self._on_dev_status(DeviceStatus.CONNECTED if status else DeviceStatus.DISCONNECTED, msg)

    async def _subscribe(self, rx_uuid, subscribe_callback):
        status = True
        msg = ""
        try:
            logger.info("start notify {}".format(rx_uuid))
            await self.device.start_notify(rx_uuid, self._notify_nus_callback)
        except (asyncio.TimeoutError, asyncio.CancelledError, Exception) as error:
            logger.error(str(error), exc_info=True)
            msg = str(error)
            status = False

        if subscribe_callback:
            subscribe_callback(status, msg)

    async def _unsubscribe(self, rx_uuid, unsubscribe_callback):
        unsubscribe_result = True
        unsubscribe_msg = ""
        try:
            await self.device.stop_notify(rx_uuid)
        except (asyncio.TimeoutError, asyncio.CancelledError, Exception) as error:
            logger.error(str(error), exc_info=True)
            unsubscribe_msg = str(error)
        finally:
            if unsubscribe_callback:
                unsubscribe_callback(unsubscribe_result, unsubscribe_msg)

    async def _read_gatt_char(self, uuid, cb):
        try:
            if self.device:
                value = bytes(await self.device.read_gatt_char(uuid))
                if cb:
                    cb(value)
        except Exception as error:
            logger.error(str(error), exc_info=True)

    async def _read_device_info(self, info_name, uuid):
        if self.device:
            value = bytes(await self.device.read_gatt_char(uuid))
            if self._on_get_ble_info:
                self._on_get_ble_info(info_name, value)

    async def _disconnect(self):
        if self.device:
            await self.device.disconnect()

    async def _write(self, bytes_to_write, tx_uuid):
        await self.device.write_gatt_char(tx_uuid, bytes_to_write)

    def _write_data(self, data: bytes, tx_uuid: str):
        if not self.device:
            return

        mtu = self.device.mtu_size - 3
        segment = len(data) // mtu
        if segment == 0:
            asyncio.run_coroutine_threadsafe(self._write(data, tx_uuid), self._event_loop)
        else:
            for i in range(segment):
                asyncio.run_coroutine_threadsafe(self._write(data[i * mtu:(i + 1) * mtu], tx_uuid),
                                                 self._event_loop)
            if len(data) % mtu:
                asyncio.run_coroutine_threadsafe(self._write(data[segment * mtu:], tx_uuid), self._event_loop)

    def scan(self):
        """Discover nearby BLE devices."""
        asyncio.run_coroutine_threadsafe(self._scan(), self._event_loop)

    def connect_to_device(self, address: str):
        """
        Connect to a BLE device.
        Args:
            address: str
                eg:
                    "00:00:00:00:00:00"

        Returns:

        """
        asyncio.run_coroutine_threadsafe(self._connect(address), self._event_loop)

    def disconnect_to_device(self):
        """Disconnect from a BLE device."""
        asyncio.run_coroutine_threadsafe(self._disconnect(), self._event_loop)

    def subscribe_to_rx_char(self, subscribe_callback=Callable[[bool, str], None]):
        """
        Subscribe to the RX characteristic of the connected BLE device.
        Args:
            subscribe_callback:

        Returns:

        """
        asyncio.run_coroutine_threadsafe(self._subscribe(self._rx_uuid, subscribe_callback), self._event_loop)

    def unsubscribe_to_rx_char(self, unsubscribe_callback=Callable[[bool, str], None]):
        """
        Unsubscribe to the RX characteristic of the connected BLE device.
        Args:
            unsubscribe_callback:

        Returns:

        """
        asyncio.run_coroutine_threadsafe(self._unsubscribe(self._rx_uuid, unsubscribe_callback), self._event_loop)

    def read_gatt_char_by_uuid(self, uuid: str, cb=Callable[[bytes], None]):
        """
        Read the GATT characteristic of the connected BLE device by UUID.
        Args:
            uuid: gatt characteristic uuid
            cb: callback

        Returns:

        """
        asyncio.run_coroutine_threadsafe(self._read_gatt_char(uuid, cb), self._event_loop)

    def _read_default_device_info(self):
        for k, uuid in DEFAULT_UUID.items():
            asyncio.run_coroutine_threadsafe(self._read_device_info(k, uuid), self._event_loop)

    def send_data_to_device(self, data: bytes):
        """
        Send data to the connected BLE device.
        Args:
            data:  bytes

        Returns:

        """
        self._write_data(data, self._tx_uuid)
