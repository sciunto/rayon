#!/usr/bin/env python


import os.path
import numpy as np

from scipy.signal import find_peaks, peak_prominences

benchmark_ID = 'SIRIUS_2018_06_01_01643'
dir_raw_data = 'RAW-DATA'
dir_plot = 'PLOTS'

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
    return data[:, ::-1]


def get_peaks_data_1D(data_1D):
    """
    Return peak positions on a 1D spectrum.

    Peaks are marked by their index (ie channel number)

    """
    prominence = .05
    peaks_idx = find_peaks(data_1D[1] / data_1D[1].max(), height=None, threshold=None, distance=None,
                           prominence=prominence, width=None, wlen=None, rel_height=0.5)
    return peaks_idx[0]


def channel2qz(channel):
    """
    Convert the channels to qz.

    TOFIX: this supposes that channel # 0 -> 0 radian.
    """
    wavelength = 0.155  # nm, see logbook
    deg_per_channel = 0.012957  # Let's trust the logbook
    rad_per_channel = np.deg2rad(deg_per_channel)

    return 2 * np.pi / wavelength * np.sin(channel * rad_per_channel)


def get_I_qz(data_2D, indices):
    """
    Return I(qz) at a given qxy identified by the indices.

    Return
    ------
    (qz, (I_peak1, I_peak2, ...))

    """
    intensities = [data_2D[:, idx] for idx in indices]
    qz = channel2qz(np.arange(len(intensities[0])))
    return qz, intensities


