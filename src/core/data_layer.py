# -*- coding: utf-8 -*-
from typing import Optional

import numpy as np
from PySide6.QtCore import QObject

from src.config.register_proto import get_proto_class
from src.config.settings import BASIC
from src.core.data_handler import ParseNode, NodeData
from src.utils.public_func import trim_data


WINDOW_IN_SECOND = BASIC["window_in_seconds"]

# IMU_SR_ENUM = get_proto_class("ImuData").sample_rate.DESCRIPTOR.enum_type.values_by_number


class ImuData(object):
    last_sn = -1

    def __init__(self, sample_rate: int, acc_data: list, gyro_data: list, euler_data: list, sequence_number=0):
        self.sample_rate = sample_rate
        self.sequence_number = sequence_number
        self.acc_data = acc_data
        self.gyro_data = gyro_data
        self.euler_data = euler_data


class AccData(object):
    last_sn = -1

    def __init__(self, sample_rate: int, acc_data, sequence_number=0):
        self.sample_rate = sample_rate
        self.sequence_number = sequence_number
        self.acc_data = acc_data


class PpgAlgoData(object):
    def __init__(self, report):
        self.op_mode = report.op_mode
        self.hr = report.hr
        self.hr_confidence = report.hr_conf
        self.rr = report.rr
        self.rr_confidence = report.rr_conf
        self.activity = report.activity
        self.r = report.r
        self.spo2_confidence = report.spo2_conf
        self.spo2 = report.spo2
        self.spo2_progress = report.spo2_progress
        self.spo2_low_signal_quality_flag = report.spo2_lsq_flag
        self.spo2_motion_flag = report.spo2_mt_flag
        self.spo2_low_pi_flag = report.spo2_lp_flag
        self.spo2_unreliable_r_flag = report.spo2_ur_flag
        self.spo2_state = report.spo2_state
        self.scd_state = report.scd_state


class PpgRawData(object):
    def __init__(self, report):
        self.raw_green1 = report.green1
        self.raw_green2 = report.green2
        self.raw_ir = report.ir
        self.raw_red = report.red


class PpgAccData(object):
    def __init__(self, report):
        self.x = report.x
        self.y = report.y
        self.z = report.z


class PpgData(object):
    last_sn = -1

    def __init__(self, report_rate: int, algo_data: Optional[list] = None, raw_data: Optional[list] = None, mode: Optional[str] = None, sequence_number=0):
        self.sample_rate = report_rate
        self.sequence_number = sequence_number
        self.mode = mode

        self.alog_data = algo_data
        self.raw_data = raw_data

        self.hr_list = []
        self.hr_conf_list = []
        self.rr_list = []
        self.rr_conf_list = []
        self.spo2_list = []
        self.spo2_conf_list = []
        if self.alog_data is not None:
            for data in self.alog_data:
                self.hr_list.append(data.hr)
                self.hr_conf_list.append(data.hr_confidence)
                self.rr_list.append(data.rr)
                self.rr_conf_list.append(data.rr_confidence)
                self.spo2_list.append(data.spo2)
                self.spo2_conf_list.append(data.spo2_confidence)
        self.ppg_raw_green1_list = []
        self.ppg_raw_green2_list = []
        self.ppg_raw_ir_list = []
        self.ppg_raw_red_list = []
        if self.raw_data is not None:
            for data in self.raw_data:
                self.ppg_raw_green1_list.append(data.raw_green1)
                self.ppg_raw_green2_list.append(data.raw_green2)
                self.ppg_raw_ir_list.append(data.raw_ir)
                self.ppg_raw_red_list.append(data.raw_red)


class DataLayer(QObject):

    def __init__(self, data_manage_handler):
        super().__init__()
        self.data_manage_handler = data_manage_handler

        # IMU sensor
        self._imu_buffer = {"acc": [[], [], []],
                            "gyro": [[], [], []],
                            "eular": [[], [], []]}

        self._ppg_algo_buffer = {
            "hr": [],
            "hr_conf": [],
            "rr": [],
            "rr_conf": [],
            "spo2": [],
            "spo2_conf": []
        }
        self._ppg_raw_buffer = {
            "green1": [],
            "green2": [],
            "ir": [],
            "red": [],
        }

        # imu
        parse_node = ParseNode(["SensorApp", "imu_data"], ["seq_num", "sample_rate", "acc_raw_data", "gyro_raw_data", "eular_raw_data", "port", "acc_coefficient", "gyro_coefficient"])
        self.data_manage_handler.register_parsed_callback_func(parse_node, self._on_imu_data)

        # ppg
        parse_node = ParseNode(["SensorApp", "ppg_data"], ["seq_num", "report_rate", "mode", "report", "seg_finished"])
        self.data_manage_handler.register_parsed_callback_func(parse_node, self._on_ppg_data)

    @property
    def imu_buffer(self):
        return self._imu_buffer

    @property
    def ppg_algo_buffer(self):
        return self._ppg_algo_buffer

    @property
    def ppg_raw_buffer(self):
        return self._ppg_raw_buffer

    def _on_imu_data(self, node_data: NodeData):
        seq_num = node_data.get_value("seq_num")
        sample_rate = node_data.get_value("sample_rate")
        acc_raw = node_data.get_value("acc_raw_data")
        gyro_raw = node_data.get_value("gyro_raw_data")
        eular_raw = node_data.get_value("eular_raw_data")
        port = node_data.get_value("port")
        acc_coefficient = node_data.get_value("acc_coefficient")
        gyro_coefficient = node_data.get_value("gyro_coefficient")

        if IMU_SR_ENUM[sample_rate].name.split("_")[-1] in ["UNUSED", "OFF"]:
            return

        acc_data_list = parse_imu_data(acc_raw, acc_coefficient)
        gyro_data_list = parse_imu_data(gyro_raw, gyro_coefficient)
        eular_data_list = parse_eular_data(eular_raw)
        convert_sample_rate = convert_sr(IMU_SR_ENUM, sample_rate)

        imu_data_class = ImuData(sample_rate, acc_data_list, gyro_data_list, eular_data_list, seq_num)

        self._imu_buffer["acc"] = trim_data(np.concatenate([self._imu_buffer['acc'], imu_data_class.acc_data], 1), 1, WINDOW_IN_SECOND * convert_sample_rate)
        self._imu_buffer["gyro"] = trim_data(np.concatenate([self._imu_buffer['gyro'], imu_data_class.gyro_data], 1), 1, WINDOW_IN_SECOND * convert_sample_rate)
        self._imu_buffer["eular"] = trim_data(np.concatenate([self._imu_buffer['eular'], imu_data_class.euler_data], 1), 1, WINDOW_IN_SECOND * convert_sample_rate)

    def _on_ppg_data(self, node_data: NodeData):
        seq_num = node_data.get_value("seq_num")
        report_rate = node_data.get_value("report_rate")
        mode = node_data.get_value("mode")
        report = node_data.get_value("report")
        seg_finished = node_data.get_value("seg_finished")

        if PPG_SR_ENUM[report_rate].name.split("_")[-1] in ["INVALID", "OFF"]:
            return

        convert_sample_rate = convert_sr(PPG_SR_ENUM, report_rate)

        raw_data_list = []
        algo_data_list = []
        for raw in report.raw:
            raw_data_list.append(PpgRawData(raw))

        for algo in report.algo:
            algo_data_list.append(PpgAlgoData(algo))

        ppg_data_class = PpgData(report_rate=convert_sample_rate,
                                 algo_data=algo_data_list,
                                 raw_data=raw_data_list)

        if len(ppg_data_class.alog_data):
            self._ppg_algo_buffer['hr'] = trim_data(np.concatenate([self._ppg_algo_buffer['hr'], ppg_data_class.hr_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)
            self._ppg_algo_buffer['hr_conf'] = trim_data(np.concatenate([self._ppg_algo_buffer['hr_conf'], ppg_data_class.hr_conf_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)
            self._ppg_algo_buffer['rr'] = trim_data(np.concatenate([self._ppg_algo_buffer['rr'], ppg_data_class.rr_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)
            self._ppg_algo_buffer['rr_conf'] = trim_data(np.concatenate([self._ppg_algo_buffer['rr_conf'], ppg_data_class.rr_conf_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)
            self._ppg_algo_buffer['spo2'] = trim_data(np.concatenate([self._ppg_algo_buffer['spo2'], ppg_data_class.spo2_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)
            self._ppg_algo_buffer['spo2_conf'] = trim_data(np.concatenate([self._ppg_algo_buffer['spo2_conf'], ppg_data_class.spo2_conf_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)

        if len(ppg_data_class.raw_data):
            self._ppg_raw_buffer['green1'] = trim_data(np.concatenate([self._ppg_raw_buffer['green1'], ppg_data_class.ppg_raw_green1_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)
            self._ppg_raw_buffer['green2'] = trim_data(np.concatenate([self._ppg_raw_buffer['green2'], ppg_data_class.ppg_raw_green2_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)
            self._ppg_raw_buffer['ir'] = trim_data(np.concatenate([self._ppg_raw_buffer['ir'], ppg_data_class.ppg_raw_ir_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)
            self._ppg_raw_buffer['red'] = trim_data(np.concatenate([self._ppg_raw_buffer['red'], ppg_data_class.ppg_raw_red_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)


def parse_eular_data(data_list):
    data = [[], [], []]
    for i in range(len(data_list)):
        col = i % 3
        value = data_list[i]
        data[col].append(value)
    return data


def parse_imu_data(data_bytes, sensitivity):
    data = [[], [], []]
    for i in range(len(data_bytes) // 2):
        col = i % 3
        value = int.from_bytes(data_bytes[i * 2:i * 2 + 2], byteorder='little', signed=True)
        value = value / sensitivity
        data[col].append(value)
    return data


def parse_acc_data(data_bytes, sensitivity):
    data = [[], [], []]
    for i in range(len(data_bytes) // 2):
        col = i % 3
        value = int.from_bytes(data_bytes[i * 2:i * 2 + 2], byteorder='little', signed=True)
        value = value / sensitivity
        data[col].append(value)
    return data


def convert_sr(sr_enum, sr):
    try:
        return int(sr_enum[sr].name.split("_")[-1])
    except Exception as e:
        raise e


