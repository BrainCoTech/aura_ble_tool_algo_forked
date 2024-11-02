# -*- coding: utf-8 -*-
from typing import Optional

import numpy as np
from PySide6.QtCore import QObject, Signal

from src.config.register_proto import get_proto_class
from src.config.settings import BASIC
from src.core.data_handler import ParseNode, NodeData
from src.utils.public_func import trim_data, save_data_to_file, check_received_sn

WINDOW_IN_SECOND = BASIC["window_in_seconds"]

IMU_SR_ENUM = get_proto_class("ImuData").sample_rate.DESCRIPTOR.enum_type.values_by_number
PPG_SR_ENUM = get_proto_class("PpgData").report_rate.DESCRIPTOR.enum_type.values_by_number


class ImuData(object):
    last_sn = -1

    def __init__(self, sample_rate: int, acc_data: list, gyro_data: list, sequence_number=0):
        self.sample_rate = sample_rate
        self.sequence_number = sequence_number
        self.acc_data = acc_data
        self.gyro_data = gyro_data


class AccData(object):
    last_sn = -1

    def __init__(self, sample_rate: int, acc_data, sequence_number=0):
        self.sample_rate = sample_rate
        self.sequence_number = sequence_number
        self.acc_data = acc_data
#
#
# class PpgAlgoData(object):
#     def __init__(self, report):
#         self.op_mode = report.op_mode
#         self.hr = report.hr
#         self.hr_confidence = report.hr_conf
#         self.rr = report.rr
#         self.rr_confidence = report.rr_conf
#         self.activity = report.activity
#         self.r = report.r
#         self.spo2_confidence = report.spo2_conf
#         self.spo2 = report.spo2
#         self.spo2_progress = report.spo2_progress
#         self.spo2_low_signal_quality_flag = report.spo2_lsq_flag
#         self.spo2_motion_flag = report.spo2_mt_flag
#         self.spo2_low_pi_flag = report.spo2_lp_flag
#         self.spo2_unreliable_r_flag = report.spo2_ur_flag
#         self.spo2_state = report.spo2_state
#         self.scd_state = report.scd_state


class PpgHrResData(object):
    def __init__(self, hr: int, hr_conf: int, wear_state: int):
        self.hr = hr
        self.hr_conf = hr_conf
        self.wear_state = wear_state


class PpgHrvResData(object):
    def __init__(self, rr_arr: list, rr_conf: int):
        self.rr_arr = rr_arr
        self.rr_conf = rr_conf


class PpgRawData(object):
    def __init__(self, report_raw):
        self.raw_green1 = report_raw.green1
        self.raw_green2 = report_raw.green2
        self.raw_ir = report_raw.ir
        self.raw_red = report_raw.red


class PpgData(object):
    last_sn = -1

    def __init__(self, report_rate=None, hrv_data=None, hr_data=None, raw_data_list=None, mode=None, sequence_number=0):
        self.sample_rate = report_rate
        self.sequence_number = sequence_number
        self.mode = mode

        self.hr_data = hr_data
        self.hrv_data = hrv_data
        self.raw_data = raw_data_list

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
    _save_data_file_path = ""

    ppg_raw_signal = Signal(list)
    imu_raw_signal = Signal(list)

    def __init__(self, data_manage_handler):
        super().__init__()
        self.data_manage_handler = data_manage_handler

        # IMU sensor
        self._imu_buffer = {"acc": [[], [], []],
                            "gyro": [[], [], []]}

        self._ppg_algo_buffer = {
            "hr": [],
            "hr_conf": [],
            "rr": [],
            "rr_conf": [],
        }
        self._ppg_raw_buffer = {
            "green1": [],
            "green2": [],
            "ir": [],
            "red": [],
        }

        # imu
        parse_node = ParseNode(["AuraResp", "sensor_data", "imu_data"], ["seq_num", "sample_rate", "acc_data", "gyro_data"])
        self.data_manage_handler.register_parsed_callback_func(parse_node, self._on_imu_data)

        # ppg
        parse_node = ParseNode(["AuraResp", "sensor_data", "ppg_data"], ["seq_num", "report_rate", "mode", "report", "seg_fin"])
        self.data_manage_handler.register_parsed_callback_func(parse_node, self._on_ppg_data)

    def enable_save_data(self, file_path):
        self._save_data_file_path = file_path

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
        acc_raw = node_data.get_value("acc_data")
        gyro_raw = node_data.get_value("gyro_data")

        if IMU_SR_ENUM[sample_rate].name.split("_")[-1] in ["NONE"]:
            return

        acc_data_list = parse_acc_data(parse_imu_data(acc_raw))
        gyro_data_list = parse_gyro_data(parse_imu_data(gyro_raw))
        # convert_sample_rate = convert_imu_sr(IMU_SR_ENUM, sample_rate)
        convert_sample_rate = 25

        imu_data_class = ImuData(sample_rate, acc_data_list, gyro_data_list, seq_num)

        # print(len(acc_data_list[0]), len(acc_data_list[1]), len(acc_data_list[2]))
        # print(len(self._imu_buffer["acc"][0]), len(self._imu_buffer["acc"][1]), len(self._imu_buffer["acc"][2]))
        # print('------------------------------')

        self._imu_buffer["acc"] = trim_data(np.concatenate([self._imu_buffer['acc'], acc_data_list], 1), 1, WINDOW_IN_SECOND * convert_sample_rate)
        self._imu_buffer["gyro"] = trim_data(np.concatenate([self._imu_buffer['gyro'], gyro_data_list], 1), 1, WINDOW_IN_SECOND * convert_sample_rate)

        data_dict = {
            "seq_num": seq_num,
            "sample_rate": convert_sample_rate,
            "acc_data": acc_data_list,
            "gyro_data": gyro_data_list
        }
        if self._save_data_file_path:
            save_data_to_file("{}_imu.txt".format(self._save_data_file_path), data_dict)
        self.imu_raw_signal.emit([acc_data_list, gyro_data_list])

    def _on_ppg_data(self, node_data: NodeData):
        seq_num = node_data.get_value("seq_num")
        report_rate = node_data.get_value("report_rate")
        mode = node_data.get_value("mode")
        report = node_data.get_value("report")
        seg_fin = node_data.get_value("seg_fin")

        if PPG_SR_ENUM[report_rate].name.split("_")[-1] in ["NONE", "OFF"]:
            return

        convert_sample_rate = convert_ppg_sr(PPG_SR_ENUM, report_rate)

        raw_data_list = []
        for raw in report.raw:
            raw_data_list.append(PpgRawData(raw))

        hr_data = PpgHrResData(report.hr_res.hr, report.hr_res.hr_conf, report.hr_res.wear)
        hrv_data = PpgHrvResData(report.hrv_res.rr_arr, report.hrv_res.rr_conf)

        ppg_data_class = PpgData(report_rate=convert_sample_rate,
                                 hr_data=hr_data,
                                 hrv_data=hrv_data,
                                 raw_data_list=raw_data_list)

        self._ppg_algo_buffer['hr'].append(hr_data.hr)
        self._ppg_algo_buffer['hr_conf'].append(hr_data.hr_conf)
        self._ppg_algo_buffer['rr'].extend(hrv_data.rr_arr)
        self._ppg_algo_buffer['rr_conf'].append(hrv_data.rr_conf)
        for buffer in [self._ppg_algo_buffer['hr'], self._ppg_algo_buffer['hr_conf'], self._ppg_algo_buffer['rr'], self._ppg_algo_buffer['rr_conf']]:
            buffer = trim_data(buffer, 0, WINDOW_IN_SECOND * convert_sample_rate)

        data_dict = {
            "seq_num": seq_num,
            "sample_rate": convert_sample_rate,
            # "hr_data": {"hr": hr_data.hr, "hr_conf": hr_data.hr_conf, "wear_state": hr_data.wear_state},
            # "rr_data": {"rr": hrv_data.rr_arr, "rr_conf": hrv_data.rr_conf}
        }

        if len(ppg_data_class.raw_data):
            self._ppg_raw_buffer['green1'] = trim_data(np.concatenate([self._ppg_raw_buffer['green1'], ppg_data_class.ppg_raw_green1_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)
            self._ppg_raw_buffer['green2'] = trim_data(np.concatenate([self._ppg_raw_buffer['green2'], ppg_data_class.ppg_raw_green2_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)
            self._ppg_raw_buffer['ir'] = trim_data(np.concatenate([self._ppg_raw_buffer['ir'], ppg_data_class.ppg_raw_ir_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)
            self._ppg_raw_buffer['red'] = trim_data(np.concatenate([self._ppg_raw_buffer['red'], ppg_data_class.ppg_raw_red_list], 0), 0, WINDOW_IN_SECOND * convert_sample_rate)

            data_dict["raw_data"] = {"green1": ppg_data_class.ppg_raw_green1_list,
                                     # "green2": ppg_data_class.ppg_raw_green2_list,
                                     # "ir": ppg_data_class.ppg_raw_ir_list,
                                     # "red": ppg_data_class.ppg_raw_red_list,
                                     }

        if self._save_data_file_path:
            save_data_to_file("{}_ppg.txt".format(self._save_data_file_path), data_dict)
        self.ppg_raw_signal.emit(ppg_data_class.ppg_raw_green1_list)


def parse_acc_data(acc_data):
    ACCEL_FULL_SCALE = 8.0
    ACC_ADC_RANGE = 32768.0
    data = acc_data.copy()
    for i in range(len(acc_data)):
        for j in range(len(acc_data[i])):
            value = acc_data[i][j]
            value = value * ACCEL_FULL_SCALE / ACC_ADC_RANGE * 9.8  # g - > m/s^2
            data[i][j] = value
    return data


def parse_gyro_data(gyro_data):
    GYRO_FULL_SCALE = 2000.0
    GYRO_ADC_RANGE = 32768.0
    data = gyro_data.copy()
    for i in range(len(gyro_data)):
        for j in range(len(gyro_data[i])):
            value = gyro_data[i][j]
            value = value * GYRO_FULL_SCALE / GYRO_ADC_RANGE  # degree/s
            data[i][j] = value
    return data


def parse_imu_data(data_bytes):
    data = [[], [], []]
    for i in range(len(data_bytes) // 2):
        col = i % 3
        value = int.from_bytes(data_bytes[i * 2:i * 2 + 2], byteorder='little', signed=True)
        data[col].append(value)
    return data


def convert_imu_sr(sr_enum, sr):
    try:
        return int(sr_enum[sr].name.split("_")[-1][:-2])
    except Exception as e:
        raise e


def convert_ppg_sr(sr_enum, sr):
    try:
        return int(sr_enum[sr].name.split("_")[-1][2:-2])
    except Exception as e:
        raise e


