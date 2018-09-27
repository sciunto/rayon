import time
import os.path
import numpy as np

import matplotlib.pyplot as plt

dir_proc = 'PROC-DATA'
dir_raw_data = 'RAW-DATA'
dir_plot = 'PLOTS'


today = time.strftime("%Y-%m-%d")


def load_data_fluo(ID):
    """
    Load fluorescence spectrum from raw data.


    Column 0: qxy
    Column 1: I
    """
    data = np.loadtxt(os.path.join(dir_raw_data, ID + '_fluospectrum04.mat'))
    return data


def read_time(ID):
    """
    To extract the time acquisition of each fluorescence spectrum in the measurement set
    """
    data = np.loadtxt(os.path.join(dir_raw_data, ID + '.dat'), skiprows=1)
    time = data[0,6]
    return time


def peak_ratio_K(data):
    """
    Ratio between intensity of K-line of Potassium (channel=548)
    and the intensity of the elastic peak (E=8keV, channel=1321)
    """
    try:
        ratio = data[548] / data[1321]
    except (RuntimeError,ZeroDivisionError):
        ratio = 0.

    return ratio

def peak_ratio_Cl(data):
    """
    Ratio between intensity of K-line of Chlore (channel=438)
    and the intensity of the elastic peak (E=8keV, channel=1321)
    """
    try:
        ratio = data[438] / data[1321]
    except (RuntimeError,ZeroDivisionError):
        ratio = 0.

    return ratio


def plot_fluo_spectrum(ID, data, save=False):
    """
    Plot a spectrum of fluorescence with 2048 channels
    """
    plt.figure(figsize=(10, 5))
    plt.semilogy(data)
    plt.xlabel('channels')
    plt.ylabel('I')
    plt.title(ID + '---' + today)

    if save:
        figpath = os.path.join(dir_plot, ID + '-fluo.png')
        datpath = os.path.join(dir_proc, ID + '-fluo.txt')
        plt.savefig(figpath)
        plt.close()


def plot_variation_KCl(ID, intensity_K, intensity_Cl, time, save=False):
    """
    Plot the variation of intensity of K-line of potassium as a function of time
    """
    fig, axes = plt.subplots(nrows=2)
    ax = axes.ravel()
    #plt.figure(figsize=(10, 5))
    ax[0].plot(time/60., intensity_K, 'r.')
    ax[1].plot(time/60., intensity_Cl, 'g.')
    ax[1].set_xlabel('t (mn)')
    ax[0].set_ylabel('I ($I_K/I_0$)')
    ax[1].set_ylabel('I ($I_{Cl}/I_0$)')
    ax[0].set_title(ID + '---' + today)
    if save:
        figpath = os.path.join(dir_plot, ID + '-fluoKCl.png')
        datpath = os.path.join(dir_proc, ID + '-fluoKCl.txt')
        plt.savefig(figpath)
        plt.close()

