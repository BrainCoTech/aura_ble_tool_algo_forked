from loguru import logger

from ..config.settings import PROTO_CONFIG

HEADER = PROTO_CONFIG["header"]
HEADER_VERSION = PROTO_CONFIG["header_version"]
PROTO_CLASS = PROTO_CONFIG["proto_class"]


class BrainCoPacket(object):
    def __init__(self):
        self.magic_numbers = []
        self.project_id = None
        self.flag = None
        self.header_version = None
        self.payload_version = None
        self.source_id = None
        self.destination_id = None
        self.reserved = None
        self.checksum = None
        self.payload_length = []
        self.payload = b''
        self.packet_crc16 = []

    def calculate_payload_length(self):
        try:
            length = int.from_bytes(self.payload_length, byteorder='little')
            return length
        except Exception as e:
            logger.error(str(e), exc_info=True)

    def calculate_packet_crc16(self):
        """
        Calculate the crc 16 of the current packet and return
        Returns: bytes

        """
        try:
            buffer = self.cur_buffer()
            crc = crc16(buffer).to_bytes(2, byteorder='little')
            return crc
        except Exception as e:
            logger.error(e, exc_info=True)

    def cur_buffer(self):
        if self.header_version == 1:
            buffer = b''.join(i for i in self.magic_numbers) \
                     + self.header_version.to_bytes(1, byteorder='little') \
                     + self.__project_id_bytes() \
                     + self.payload_version.to_bytes(1, byteorder='little') \
                     + len(self.payload).to_bytes(2, byteorder='little') \
                     + self.payload
        elif self.header_version == 2:
            buffer = b''.join(i for i in self.magic_numbers) \
                     + self.header_version.to_bytes(1, byteorder='little') \
                     + self.__project_id_bytes() \
                     + self.payload_version.to_bytes(1, byteorder='little') \
                     + len(self.payload).to_bytes(2, byteorder='little') \
                     + self.source_id.to_bytes(1, byteorder='little') \
                     + self.destination_id.to_bytes(1, byteorder='little') \
                     + self.flag.to_bytes(1, byteorder='little') \
                     + self.payload
        else:
            raise TypeError("header version {} is not supported".format(self.header_version))
        return buffer

    def __project_id_bytes(self):
        # 兼容新旧协议
        project_id = HEADER.get("project_id", None)
        if project_id is None:
            return b''
        else:
            return project_id.to_bytes(1, byteorder='little')

    def __str__(self):
        return "{}".format(self.payload)


class ToolPacket(BrainCoPacket):
    def __init__(self, payload, source_id=None, destination_id=None, flag=None):
        super(ToolPacket, self).__init__()
        self.payload = payload
        self.header_version = HEADER_VERSION
        self.source_id = source_id
        self.destination_id = destination_id
        self.flag = flag

        for param_key, param_value in HEADER.items():
            if not hasattr(self, param_key):
                raise AttributeError(f"{self.__class__.__name__} has no attribute '{param_key}'")
            setattr(self, param_key, param_value)

    def encode(self):
        """
        Encode the current packet and return the resulting data
        Returns: bytes

        """

        cur_buffer = self.cur_buffer()
        packet_crc16 = crc16(cur_buffer).to_bytes(2, byteorder='little')
        buffer_encode = cur_buffer + packet_crc16
        return buffer_encode

    def __str__(self):
        hex_str = " ".join([f"{i:02X}" for i in self.encode()])
        return f"source: {self.source_id} -> destination: {self.destination_id}, bytes: {self.encode()} hex: {hex_str}"


def crc16(data: bytes):
    data = bytearray(data)
    poly = 0xA001
    crc = 0xFFFF
    for b in data:
        crc ^= (0xFF & b)
        for _ in range(0, 8):
            if crc & 0x0001:
                crc = ((crc >> 1) & 0xFFFF) ^ poly
            else:
                crc = ((crc >> 1) & 0xFFFF)
    return crc

