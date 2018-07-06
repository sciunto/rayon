#!/usr/bin/env python


import os.path
import numpy as np

from scipy.signal import find_peaks, peak_prominences

dir_raw_data = 'RAW-DATA'


def load_data_1D(ID):
    """
    Load 1D spectrum from raw data.


    Column 0: qxy
    Column 1: I
    """
    data = np.loadtxt(os.path.join(dir_raw_data, ID + '_1D.dat')).T
    data = data[:, ::-1]
    return data


def load_data_2D(ID):
    """
    Load 1D spectrum from raw data.


    Column 0: qxy
    Column 1: I
    """
    data = np.loadtxt(os.path.join(dir_raw_data, ID + '_1D.mat')).T
    return data[::-1, ::-1]


def load_metadata(ID):
    """
    Load metadata.

    0: delta
    1: ys
    2: zs
    3: xtal2perp
    4: alphax
    5: gamma
    6: xs
    6: energydcm
    7: current
    8: mon2
    9: surfacepressure
    10: areapermolecule
    11: qxy
    12: mon4
    13: pilatusroi1
    14: braggdcm
    15: integration_time
    16: sensors_rel_timestamps
    17: sensorsTimestamps
    """
    data = np.loadtxt(os.path.join(dir_raw_data, ID + '.dat'), skiprows=1)
    return data.T


def get_peaks_data_1D(data_1D):
    """
    Return peak positions on a 1D spectrum.

    Peaks are marked by their index (ie channel number)

    """
    prominence = .05
    peaks_idx = find_peaks(data_1D[1] / data_1D[1].max(), height=None, threshold=None, distance=None,
                           prominence=prominence, width=None, wlen=None, rel_height=0.5)
    return peaks_idx[0]


def channel2qz(ID, channel):
    """
    Convert the channels to qz.

    TOFIX: this supposes that channel # 0 -> 0 radian.
    """
    wavelength = 0.155  # nm, see logbook
    deg_per_channel = 0.012957  # Let's trust the logbook
    rad_per_channel = np.deg2rad(deg_per_channel)

    offset_angle = load_metadata(ID)[5].mean()  # Degree
    offset_angle = np.deg2rad(offset_angle)

    return 2 * np.pi / wavelength * \
            np.sin(channel * rad_per_channel + offset_angle)


def get_I_qz(ID, data_2D, indices):
    """
    Return I(qz) at a given qxy identified by the indices.

    Return
    ------
    (qz, (I_peak1, I_peak2, ...))

    """
    intensities = [data_2D[:, idx] for idx in indices]
    qz = channel2qz(ID, np.arange(len(intensities[0])))
    return qz, intensities


