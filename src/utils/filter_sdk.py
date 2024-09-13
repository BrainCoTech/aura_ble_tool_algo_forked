from scipy import signal
import numpy as np
import math


# Filter design
# https://zhuanlan.zhihu.com/p/51097798

# Filter parameter generation
# http://www-users.cs.york.ac.uk/~fisher/mkfilter/trad.html

# Create coefficients for 2nd order notch filter
def notch_params(notch_freq, sample_rate, quality_factor=30):
    b, a = signal.iirnotch(notch_freq, quality_factor, sample_rate)
    return b, a


def butter_band_pass_params(lowcut, highcut, sample_rate, order=4):
    nyq = 0.5 * sample_rate
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='bandpass')
    return b, a


def butter_low_pass_params(cutoff, sample_rate, order=4):
    nyq = 0.5 * sample_rate
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_high_pass_params(cutoff, sample_rate, order=4):
    nyq = 0.5 * sample_rate
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def butter_band_stop_params(lowcut, highcut, sample_rate, order=4):
    b, a = signal.butter(order, [lowcut / (0.5 * sample_rate), highcut / (0.5 * sample_rate)], 'bandstop')
    return b, a


def filter_with_params(data, params):
    return signal.filtfilt(params[0], params[1], data)


_spike_kernel = [-1, 2, -1]


def spike_filter_upward(data, strength=1):
    if len(data) < 3:
        return data
    std = np.std(np.array(data))
    print("STD:" + str(std))
    filtered = data.copy()
    filtered[0] = 0
    filtered[len(data) - 1] = 0

    for i in range(1, len(data) - 1):
        val = data[i - 1] * _spike_kernel[0] + data[i] * _spike_kernel[1] + data[i + 1] * _spike_kernel[2]
        if val < strength * std:
            filtered[i] = 0
        else:
            filtered[i] = val

    return filtered


def spike_filter_downward(data, strength=1):
    if len(data) < 3:
        return data
    std = np.std(np.array(data))

    filtered = data.copy()
    filtered[0] = 0
    filtered[len(data) - 1] = 0

    for i in range(1, len(data) - 1):
        val = -data[i - 1] * _spike_kernel[0] - data[i] * _spike_kernel[1] - data[i + 1] * _spike_kernel[2]

        if val < strength * std:
            filtered[i] = 0
        else:
            filtered[i] = val

    return filtered


# C implementation of filters
class BWBandPassFilter:
    n = 0
    A = None
    d1 = None
    d2 = None
    d3 = None
    d4 = None
    w0 = None
    w1 = None
    w2 = None
    w3 = None
    w4 = None

    def __init__(self, order, sample_rate, fl, fu):
        if order % 4 != 0:
            print("ERROR:Order has to be multiple of 4")
            return

        if fu <= fl:
            print("ERROR:Lower half-power frequency is smaller than higher half-power frequency")
            return

        self.n = int(order / 4)
        self.A = [0.0] * self.n
        self.d1 = [0.0] * self.n
        self.d2 = [0.0] * self.n
        self.d3 = [0.0] * self.n
        self.d4 = [0.0] * self.n

        self.w0 = [0.0] * self.n
        self.w1 = [0.0] * self.n
        self.w2 = [0.0] * self.n
        self.w3 = [0.0] * self.n
        self.w4 = [0.0] * self.n

        a = math.cos(math.pi * (fu + fl) / sample_rate) / math.cos(math.pi * (fu - fl) / sample_rate)
        a2 = a * a
        b = math.tan(math.pi * (fu - fl) / sample_rate)
        b2 = b * b

        for i in range(self.n):
            r = math.sin(math.pi * (2.0 * i + 1.0) / (4.0 * self.n))
            s = b2 + 2.0 * b * r + 1.0
            self.A[i] = b2 / s
            self.d1[i] = 4.0 * a * (1.0 + b * r) / s
            self.d2[i] = 2.0 * (b2 - 2.0 * a2 - 1.0) / s
            self.d3[i] = 4.0 * a * (1.0 - b * r) / s
            self.d4[i] = -(b2 - 2.0 * b * r + 1.0) / s

    def filter(self, x):
        for i in range(self.n):
            self.w0[i] = self.d1[i] * self.w1[i] + self.d2[i] * self.w2[i] + self.d3[i] * self.w3[i] + self.d4[i] * \
                         self.w4[i] + x
            x = self.A[i] * (self.w0[i] - 2.0 * self.w2[i] + self.w4[i])
            self.w4[i] = self.w3[i]
            self.w3[i] = self.w2[i]
            self.w2[i] = self.w1[i]
            self.w1[i] = self.w0[i]
        return x


class BWBandStopFilter:
    n = 0
    A = None
    d1 = None
    d2 = None
    d3 = None
    d4 = None
    w0 = None
    w1 = None
    w2 = None
    w3 = None
    w4 = None
    r = 0.0
    s = 0.0

    def __init__(self, order, sample_rate, fl, fu):
        if order % 4 != 0:
            print("ERROR:Order has to be multiple of 4")
            return

        if fu <= fl:
            print("ERROR:Lower half-power frequency is smaller than higher half-power frequency")
            return

        self.n = int(order / 4)
        self.A = [0.0] * self.n
        self.d1 = [0.0] * self.n
        self.d2 = [0.0] * self.n
        self.d3 = [0.0] * self.n
        self.d4 = [0.0] * self.n

        self.w0 = [0.0] * self.n
        self.w1 = [0.0] * self.n
        self.w2 = [0.0] * self.n
        self.w3 = [0.0] * self.n
        self.w4 = [0.0] * self.n

        a = math.cos(math.pi * (fu + fl) / sample_rate) / math.cos(math.pi * (fu - fl) / sample_rate)
        a2 = a * a
        b = math.tan(math.pi * (fu - fl) / sample_rate)
        b2 = b * b

        self.r = 4.0 * a
        self.s = 4.0 * a2 + 2.0

        for i in range(self.n):
            r = math.sin(math.pi * (2.0 * i + 1.0) / (4.0 * self.n))
            s = b2 + 2.0 * b * r + 1.0
            self.A[i] = 1.0 / s
            self.d1[i] = 4.0 * a * (1.0 + b * r) / s
            self.d2[i] = 2.0 * (b2 - 2.0 * a2 - 1.0) / s
            self.d3[i] = 4.0 * a * (1.0 - b * r) / s
            self.d4[i] = -(b2 - 2.0 * b * r + 1.0) / s

    def filter(self, x):
        for i in range(self.n):
            self.w0[i] = self.d1[i] * self.w1[i] + self.d2[i] * self.w2[i] + self.d3[i] * self.w3[i] + self.d4[i] * \
                         self.w4[i] + x
            x = self.A[i] * (self.w0[i] - self.r * self.w1[i] + self.s * self.w2[i] - self.r * self.w3[i] + self.w4[i])
            self.w4[i] = self.w3[i]
            self.w3[i] = self.w2[i]
            self.w2[i] = self.w1[i]
            self.w1[i] = self.w0[i]
        return x


class BWLowPassFilter:
    n = 0
    A = None
    d1 = None
    d2 = None

    w0 = None
    w1 = None
    w2 = None

    def __init__(self, order, sample_rate, f):

        if order % 2 != 0:
            print("ERROR:Order has to be multiple of 2")
            return

        self.n = int(order / 2)
        self.A = [0.0] * self.n
        self.d1 = [0.0] * self.n
        self.d2 = [0.0] * self.n

        self.w0 = [0.0] * self.n
        self.w1 = [0.0] * self.n
        self.w2 = [0.0] * self.n

        a = math.tan(math.pi * f / sample_rate)
        a2 = a * a

        for i in range(self.n):
            r = math.sin(math.pi * (2.0 * i + 1.0) / (4.0 * self.n))
            s = a2 + 2.0 * a * r + 1.0
            self.A[i] = a2 / s
            self.d1[i] = 2.0 * (1.0 - a2) / s
            self.d2[i] = -(a2 - 2.0 * a * r + 1.0) / s

    def filter(self, x):
        for i in range(self.n):
            self.w0[i] = self.d1[i] * self.w1[i] + self.d2[i] * self.w2[i] + x
            x = self.A[i] * (self.w0[i] + 2.0 * self.w1[i] + self.w2[i])
            self.w2[i] = self.w1[i]
            self.w1[i] = self.w0[i]
        return x


if __name__ == '__main__':
    order = 4
    sample_rate = 250
    data = [1, 2, 3, 4, 5, 6]
    bs_filter = BWBandStopFilter(order, sample_rate, 49, 51)
    bp_filter = BWBandPassFilter(order, sample_rate, 2, 45)
    for j in range(len(data)):
        data[j] = bp_filter.filter(data[j])
    for k in range(len(data)):
        data[k] = bs_filter.filter(data[k])
