# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: aura_common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x61ura_common.proto\x12\x11tech.brainco.aura\">\n\nDeviceInfo\x12\x15\n\rserial_number\x18\x01 \x01(\t\x12\x19\n\x11\x66irmware_revision\x18\x03 \x01(\t\"v\n\x07ImuData\x12\x0f\n\x07seq_num\x18\x01 \x01(\r\x12\x35\n\x0bsample_rate\x18\x02 \x01(\x0e\x32 .tech.brainco.aura.ImuSampleRate\x12\x10\n\x08\x61\x63\x63_data\x18\x03 \x01(\x0c\x12\x11\n\tgyro_data\x18\x04 \x01(\x0c\"\t\n\x07GpsData*-\n\tSportMode\x12\x08\n\x04Walk\x10\x00\x12\n\n\x06Runing\x10\x01\x12\n\n\x06\x42iking\x10\x02*m\n\rActivityState\x12\x11\n\rActivity_NONE\x10\x00\x12\x11\n\rActivity_REST\x10\x01\x12\x11\n\rActivity_WALK\x10\x02\x12\x10\n\x0c\x41\x63tivity_RUN\x10\x03\x12\x11\n\rActivity_BIKE\x10\x04*\xcf\x01\n\rImuSampleRate\x12\x18\n\x14IMU_SAMPLE_RATE_NONE\x10\x00\x12\x18\n\x14IMU_SAMPLE_RATE_50HZ\x10\x32\x12\x19\n\x15IMU_SAMPLE_RATE_100HZ\x10\x64\x12\x1a\n\x15IMU_SAMPLE_RATE_200HZ\x10\xc8\x01\x12\x1a\n\x15IMU_SAMPLE_RATE_400HZ\x10\x90\x03\x12\x1a\n\x15IMU_SAMPLE_RATE_800HZ\x10\xa0\x06\x12\x1b\n\x16IMU_SAMPLE_RATE_1600HZ\x10\xc0\x0c*\x8c\x01\n\x0eReportInterval\x12\x18\n\x14REPORT_INTERVAL_NONE\x10\x00\x12\x16\n\x12REPORT_INTERVAL_1S\x10\x01\x12\x16\n\x12REPORT_INTERVAL_5S\x10\x05\x12\x17\n\x13REPORT_INTERVAL_10S\x10\n\x12\x17\n\x13REPORT_INTERVAL_30S\x10\x1e\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aura_common_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SPORTMODE._serialized_start=235
  _SPORTMODE._serialized_end=280
  _ACTIVITYSTATE._serialized_start=282
  _ACTIVITYSTATE._serialized_end=391
  _IMUSAMPLERATE._serialized_start=394
  _IMUSAMPLERATE._serialized_end=601
  _REPORTINTERVAL._serialized_start=604
  _REPORTINTERVAL._serialized_end=744
  _DEVICEINFO._serialized_start=40
  _DEVICEINFO._serialized_end=102
  _IMUDATA._serialized_start=104
  _IMUDATA._serialized_end=222
  _GPSDATA._serialized_start=224
  _GPSDATA._serialized_end=233
# @@protoc_insertion_point(module_scope)
