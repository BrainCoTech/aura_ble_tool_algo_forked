import pprint
from queue import SimpleQueue, Empty
from threading import Thread
from typing import Callable

from loguru import logger

from ..core.tool_packet import BrainCoPacket, HEADER_VERSION, HEADER


class ParserThread(Thread):
    """Parse raw data to BrainCoPacket."""
    def __init__(self):
        super(ParserThread, self).__init__()
        self.setDaemon(True)

        self._unparsed_buffer = SimpleQueue()
        self._parsed_packets = SimpleQueue()  # 已解析队列, 一个元素就是一个 packet

        self._current_packet = BrainCoPacket()
        self._current_item_index = 0

        if HEADER_VERSION == 1:
            self._item_parsers = [self._read_magic_numbers,
                                  self._read_header_version,
                                  self._read_payload_version,
                                  self._read_payload_length,
                                  self._read_payload,
                                  self._read_packet_crc16]
        elif HEADER_VERSION == 2:
            self._item_parsers = [self._read_magic_numbers,
                                  self._read_header_version,
                                  self._read_payload_version,
                                  self._read_payload_length,
                                  self._read_source_id,
                                  self._read_destination_id,
                                  self._read_flag,
                                  self._read_payload,
                                  self._read_packet_crc16]

        if HEADER.get("project_id", None) is not None:
            self._item_parsers.insert(2, self._read_project_id)

    def get_parsed_packet(self):
        try:
            packet = self._parsed_packets.get(timeout=0.2)
            return packet
        except Empty:
            return None

    def on_received_new_data(self, data):
        try:
            self._unparsed_buffer.put(data)
        except Exception as error:
            logger.error(str(error), exc_info=True)

    def run(self):
        while True:
            try:
                data = self._unparsed_buffer.get(block=True)
                self._data_handler(data)
            except Exception as error:
                import traceback
                traceback.print_exc()
                logger.error(str(error), exc_info=True)

    def _data_handler(self, data):
        buffer = []
        for i in range(len(data)):
            buffer.append("{:02X}".format(data[i]))
        logger.debug("in.data = {}".format(" ".join(buffer)))
        self._item_parsers[self._current_item_index](data)

    def _read_magic_numbers(self, data):
        magic_numbers = HEADER['magic_numbers']
        for i in range(len(data)):
            numbers_len = len(self._current_packet.magic_numbers)
            valid_magic_number = magic_numbers[numbers_len]
            recv_magic_number_bytes = data[i].to_bytes(1, byteorder="little")
            if recv_magic_number_bytes == valid_magic_number:
                self._current_packet.magic_numbers.append(recv_magic_number_bytes)
                if len(self._current_packet.magic_numbers) == len(magic_numbers):
                    logger.debug("magic numbers: {}".format(self._current_packet.magic_numbers))
                    self._read_next_item(data[i:])
                    break
            else:
                self._current_packet.magic_numbers.clear()

    def _read_project_id(self, data):
        self._current_packet.project_id = data[0]
        logger.debug("project id: {}".format(self._current_packet.project_id))
        self._read_next_item(data)

    def _read_flag(self, data):
        self._current_packet.flag = data[0]
        logger.debug("flag: {}".format(self._current_packet.flag))
        self._read_next_item(data)

    def _read_header_version(self, data):
        self._current_packet.header_version = data[0]
        logger.debug("header_version: {}".format(self._current_packet.header_version))
        self._read_next_item(data)

    def _read_payload_version(self, data):
        self._current_packet.payload_version = data[0]
        logger.debug("payload_version: {}".format(self._current_packet.payload_version))
        self._read_next_item(data)

    def _read_source_id(self, data):
        self._current_packet.source_id = data[0]
        logger.debug("source_id: {}".format(self._current_packet.source_id))
        self._read_next_item(data)

    def _read_destination_id(self, data):
        self._current_packet.destination_id = data[0]
        logger.debug("destination_id: {}".format(self._current_packet.destination_id))
        self._read_next_item(data)

    def _read_reserved_bit(self, data):
        self._current_packet.reserved = data[0]
        logger.debug("reserved: {}".format(self._current_packet.reserved))
        self._read_next_item(data)

    def _read_payload_length(self, data):
        for i in range(len(data)):
            self._current_packet.payload_length.append(data[i])
            if len(self._current_packet.payload_length) == HEADER['payload_length']:
                logger.debug("payload_length: {}".format(int.from_bytes(self._current_packet.payload_length,
                                                                        byteorder='little')))
                self._read_next_item(data[i:])
                break

    def _read_payload(self, data):
        for i in range(len(data)):
            self._current_packet.payload += data[i].to_bytes(1, byteorder='little')
            calculate_payload_length = self._current_packet.calculate_payload_length()
            if len(self._current_packet.payload) == calculate_payload_length:
                logger.debug("payload: {}".format(self._current_packet.payload))
                self._read_next_item(data[i:])
                break

    def _read_packet_crc16(self, data):
        calculated_crc = self._current_packet.calculate_packet_crc16()
        for i in range(len(data)):
            if data[i] == calculated_crc[len(self._current_packet.packet_crc16)]:
                self._current_packet.packet_crc16.append(data[i])
                if len(self._current_packet.packet_crc16) == HEADER['packet_crc16']:
                    logger.debug("packet_crc16: {}".format(self._current_packet.packet_crc16))
                    self._parsed_packets.put(self._current_packet)
                    self._read_next_item(data[i:])
                    break
            else:
                logger.warning("crc failed!")
                self._read_next_item(data[i:])
                break

    def _read_next_item(self, data):
        self._current_item_index += 1
        if self._current_item_index >= len(self._item_parsers):
            self._current_packet = BrainCoPacket()
            self._current_item_index = 0
        if len(data) > 1:
            self._data_handler(data[1:])


class DataParserHandler(object):
    def __init__(self, recv_parsed_packet_func: Callable[[BrainCoPacket], None]):
        self.recv_parsed_packet_func = recv_parsed_packet_func
        self._message_parser = ParserThread()
        self._message_parser.start()
        self._message_thread = Thread(target=self._get_parsed_message, daemon=True)
        self._message_thread.start()
        self._connected = False

        self.recv_total_bytes = []

    def _get_parsed_message(self):
        while True:
            try:
                packet = self._message_parser.get_parsed_packet()
                if packet is not None:
                    self.recv_parsed_packet_func(packet)
            except Exception as error:
                import traceback
                traceback.print_exc()
                logger.error(str(error), exc_info=True)

    def on_received_message(self, data: bytes):
        # 接收到从硬件传过来的原始数据
        self._message_parser.on_received_new_data(data)


if __name__ == '__main__':

    parser = ParserThread()
    parser.start()

    parser.on_received_new_data(data=b'BRNC\x01\x03\x01\t\x00J\x07\n\x05\r\x00\x00 Ah\xe0')

    import time
    time.sleep(5)