from collections import defaultdict
from typing import Callable

from loguru import logger

from ..config.register_proto import get_proto_class
from ..config.settings import PROTO_CONFIG
from ..core.data_prase import DataParserHandler
from ..core.tool_packet import BrainCoPacket

_PROTO_CLASS = PROTO_CONFIG["proto_class"]


class ParseNode(object):
    """
    Parse Packet Node
    """

    def __init__(self, node_path: list, specified_value: list):
        self.node_path = node_path
        self.specified_value = specified_value

    def __hash__(self):
        return hash(str(self.node_path) + str(self.specified_value))

    def __eq__(self, other):
        return str(self.node_path) + str(self.specified_value) == str(other.node_path) + str(other.specified_value)


class NodeData(object):
    """
    Parse Node Data
    """

    def set_value(self, key, value):
        setattr(self, key, value)

    def get_value(self, key):
        return getattr(self, key, None)

    def __str__(self):
        msg = "\nNodeData\n\t"
        for key in self.__dict__.keys():
            msg += f"{key}: {getattr(self, key)}\n\t"
        return msg


class ToolProtoDataManageHandler(object):
    """"""
    _register_node_collection = defaultdict(None)
    _register_node_collection_copy = defaultdict(None)

    _get_raw_packet_func = None

    def __init__(self):
        super(ToolProtoDataManageHandler, self).__init__()

        self._data_parser_handler = DataParserHandler(recv_parsed_packet_func=self._recv_parsed_packet)

    def on_received_device_raw_message(self, data: bytes):
        """
        Recv device raw message, then parse it.
        Args:
            data:

        Returns:

        """
        self._data_parser_handler.on_received_message(data)

    def _recv_parsed_packet(self, packet: BrainCoPacket):
        content = self.get_parsed_content(packet)

        # 1. 将原始的packet发送出去
        self._send_raw_packet(packet)

        # 2. 解析content并回调各个Node
        self._start_parse_content(content)

    def _send_raw_packet(self, packet):
        if self._get_raw_packet_func:
            self._get_raw_packet_func(packet)

    def _start_parse_content(self, content):
        # 先判断节点是否有更新
        if self._register_node_collection != self._register_node_collection_copy:
            # 如果有更新, 则更新节点
            self._register_node_collection = self._register_node_collection_copy.copy()
        for node in list(self._register_node_collection.keys()):
            func = self._register_node_collection[node]
            node_path = node.node_path
            specified_value = node.specified_value

            if content.DESCRIPTOR.name != node_path[0]:
                continue

            try:
                target_node = self.__get_node(node_path, content)
                if target_node is None:
                    logger.debug(f"target_node is None: {node_path}")
                    continue
                target_node_data = self.__get_target_node_data(target_node, specified_value)
            except Exception as e:
                import traceback
                traceback.print_exc()
                logger.error(str(e))
                continue
            if func is not None:
                func(target_node_data)

    def register_get_raw_packet_func(self, func=Callable[[NodeData], None]):
        self._get_raw_packet_func = func

    def register_parsed_callback_func(self, node: ParseNode, cb=Callable[[NodeData], None]):
        """
        Register parsed callback function.
        code:
            if your proto file is:
                message MotionData {
                    int32 motion_data = 1;
                }

            node = ParseNode(node_path=["MotionData"], specified_value=["motion_data"])
            self.register_parsed_callback_func(parse_node=node, callback=your_callback_func)

        Args:
            node:
            cb:

        Returns:

        """
        self._register_node_collection[node] = cb
        self._register_node_collection_copy[node] = cb

    def remove_parsed_callback(self, node: ParseNode):
        # 删除注册的节点, 请注意删除操作只会在下一次循环遍历时候生效
        self._register_node_collection_copy.pop(node)

    def clear_parsed_callback(self):
        self._register_node_collection_copy.clear()

    def get_parsed_content(self, packet: BrainCoPacket, enable_log=True):
        if packet.header_version == 1:
            proto_data_class_str = list(_PROTO_CLASS.values())[0][1]
        elif packet.header_version == 2:
            source_destination_id_str = f"{packet.destination_id},{packet.source_id}"
            proto_data_class_str = _PROTO_CLASS[source_destination_id_str][1]
        else:
            raise TypeError("header version {} is not supported".format(packet.header_version))

        content = get_proto_class(proto_data_class_str)()
        content.ParseFromString(packet.payload)
        if enable_log:
            logger.info("\n{}\n{}".format(proto_data_class_str, content))
        return content

    @staticmethod
    def __get_target_node_data(field, values):
        data = NodeData()
        for name in values:
            data.set_value(name, getattr(field, name))
        return data

    @staticmethod
    def __get_node(root: list, field=None):
        target_field_name = root[-1]
        parent_field = field
        for field_name in root[1:-1]:
            if parent_field.HasField(field_name):  # 判断是否有该字段
                parent_field = getattr(parent_field, field_name)
            else:
                return None
        if parent_field.HasField(target_field_name):
            target_node = getattr(parent_field, target_field_name)
            return target_node
        else:
            return None
