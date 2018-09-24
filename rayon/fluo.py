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
    Ratio between intensity of K-line of potassium (channel=548) 
    and the intensity of the elastic peak (E=8keV, channel=1330)
    """
    try:
        ratio = data[548] / data[1330]
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


def plot_variation_KCl(ID, intensity, time, save=False):
    """
    Plot the variation of intensity of K-line of potassium as a function of time 
    """
    plt.figure(figsize=(10, 5))
    plt.plot(time/60., intensity, 'r.')
    plt.xlabel('t (mn)')
    plt.ylabel('I (K/I$_0$)')    
    plt.title(ID + '---' + today) 
    
    if save:
        figpath = os.path.join(dir_plot, ID + '-fluoK.png')
        datpath = os.path.join(dir_proc, ID + '-fluoK.txt')
        plt.savefig(figpath)
        plt.close()  
    

