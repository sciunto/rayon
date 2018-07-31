#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import os.path
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import rayon.spectrum as rspc
import rayon.plot as rpl

dir_proc = 'PROC-DATA'
dir_raw_data = 'RAW-DATA'

def load_data_peaks1D(ID):
    """
    Load 1D spectrum from file ID-peaks-1D.txt 
    Column 0: qxy
    Column 1: I
    """
    data = np.loadtxt(os.path.join(dir_proc, ID + '-peaks-1D.txt'))
#    data = data[:, ::-1]
    return data


def get_peaks_data_1D_b(data_1D):
    """
    Return peak positions on a 1D spectrum.

    Peaks are marked by their index (ie channel number)

    """
    prominence=0.05
    peaks_idx = find_peaks(data_1D[:,1] / data_1D[:,1].max(), height=None, threshold=None, distance=None,
                           prominence=prominence, width=None, wlen=None, rel_height=0.5)
    return peaks_idx[0]


def plot_spectrum_indx(data_1D, peaks1D_idx):
    """
    Plot the 1D spectrum as a function of the channels 
    positions of detected peaks are marked
    """
    indx = np.arange(0, len(data_1D[:,1]))
    plt.figure(figsize=(10, 5))
    plt.semilogy(indx, data_1D[:,1] / data_1D[:,1].max())
    plt.xlabel('channel')
    
    for peak_idx in peaks1D_idx:
        print(peak_idx)
        plt.axvline(x=peak_idx, color='red')
    
    plt.show()



ID = 'SIRIUS_2018_06_01_01717'

data_1D = rspc.load_data_1D(ID)
peaks1D_idx = rspc.get_peaks_data_1D(data_1D)
rpl.plot_peaks_data_1D(ID, data_1D, peaks1D_idx, save=True)
# file SIRIUS_2018_06_02_01739-peaks-1D.txt, but some peaks are not detected in peaks1D_idx !

# working on filename-peaks-1D.txt
data_peak1D = load_data_peaks1D(ID)
peaks1D_idx = get_peaks_data_1D_b(data_peak1D)
plot_spectrum_indx(data_peak1D, peaks1D_idx)

# adding peaks "TO ENTER BY HAND" with the number of the channel 
peaks_to_add = np.array([20,27,123,183])

peaks1D_idx_compl = np.sort(np.append(peaks1D_idx,peaks_to_add)) ##1717
plot_spectrum_indx(data_peak1D, peaks1D_idx_compl)

peaks1D_idx_tofit = np.sort(np.append(peaks1D_idx,peaks_to_add))
##peaks1D_idx_tofit = peaks1D_idx

rspc.fit_peaks_spectrum(ID, data_1D, peaks1D_idx_tofit,save=True)

# two closed peaks to fit by bigaussian
rspc.fit_2peaks(ID, data_1D, 21, 27)
rspc.fit_2peaks(ID, data_1D, 123, 127)
