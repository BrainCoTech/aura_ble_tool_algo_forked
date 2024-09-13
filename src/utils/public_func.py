import json
import time

import numpy as np
from scipy import fftpack

from PySide6.QtCore import QByteArray, QBuffer
from PySide6.QtGui import QImage, QPixmap


def to_base64(file_path, fmt="png"):
    image = QImage(file_path)
    data = QByteArray()
    buffer = QBuffer(data)
    image.save(buffer, fmt)
    return str(data.toBase64())[2:-1]


def get_pixmap(data_base64, fmt='png'):
    data = QByteArray().fromBase64(data_base64.encode())
    image = QImage()
    image.loadFromData(data, fmt)
    pix = QPixmap.fromImage(image)
    return pix


def save_data_to_file(file_name, data_dict):
    with open(file_name, 'a', encoding="utf-8") as file:
        data_dict["time"] = time.time()
        json.dump(data_dict, file)
        file.write("\n")


def check_received_sn(last_sn, new_sn, label):
    if (new_sn <= last_sn) and (last_sn != -1):
        if new_sn == last_sn:
            return "************ duplicate {} sn {} found ************".format(label, last_sn)
        else:
            return "************ invalid {} sn {} found ************".format(label, last_sn)
    elif new_sn > 1 + last_sn and last_sn != -1:
        return "************ missed {} sn count: {}, last sn: {}".format(label, new_sn - last_sn - 1, last_sn)
    else:
        return ''


def trim_data(buffer, axis, size):
    if not isinstance(buffer, np.ndarray):
        buffer = np.array(buffer)
    if buffer.shape[axis] >= size:
        buffer = np.delete(buffer, [i for i in range(buffer.shape[axis] - size)], axis)
    return buffer


def calculate_fft(data, rate):
    sig_freq = fftpack.fftfreq(len(data), d=1.0 / rate)
    sig_fft = fftpack.fft(data)
    sig_fft = abs(sig_fft) / (rate / 2)
    pidxs = np.where((sig_freq > 0) & (sig_freq < 80))
    return sig_freq[pidxs], sig_fft[pidxs]
