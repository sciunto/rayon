#!/usr/bin/env python


import os.path
import numpy as np

from scipy.signal import find_peaks
from lmfit import Model

dir_raw_data = 'RAW-DATA'
dir_proc = 'PROC-DATA'


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
    prominence = 0.05
    peaks_idx = find_peaks(data_1D[1] / data_1D[1].max(), height=None, threshold=None, distance=None,
                           prominence=prominence, width=None, wlen=None, rel_height=0.5)
    return peaks_idx[0]


def channel2qz(ID, channel):
    """
    Convert the channels to qz.
    channel #0 radian --> position of dodecanol peak
    """
    wavelength = 0.155  # nm, see logbook
    deg_per_channel = 0.012957  # Let's trust the logbook
    rad_per_channel = np.deg2rad(deg_per_channel)

    # Get the offset angle by averaging all the gamma angles.
    offset_angle = load_metadata(ID)[5].mean()  # Degree
    offset_angle = np.deg2rad(offset_angle)

    # position of dodecanol peak
    channel0 = 635

    return 2 * np.pi / wavelength * \
           np.sin((channel0-channel[::-1]) * rad_per_channel + offset_angle)


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


def gaussian(x, amp, cen, width):
    """width = FWHM of the gaussian centered at position cen"""
    return amp * np.exp(-4*np.log(2)*(x-cen)**2 / width**2)


def bigaussian(x, amp1, cen1, width1, amp2, cen2, width2):
    gauss1 = amp1 * np.exp(-4*np.log(2)*(x-cen1)**2 / width1**2)
    gauss2 = amp2 * np.exp(-4*np.log(2)*(x-cen2)**2 / width2**2)        
    return gauss1 + gauss2


def line(x, slope, intercept):
    """a line background"""
    return slope*x + intercept


def fit_peak(data_1D, indx0):
    """
    Gaussian fit of the peak centered around the index indx0
    obtained from the array get_peaks_data_1D

    Return
    ------
    position, width and amplitude of the peak
    """
    interval_inf = indx0 - 13  # number of channels=13x2 to cover the peak range
    if interval_inf < 0:
        interval_inf = 0
    interval_sup = indx0 + 13
    if interval_sup > len(data_1D[0])-1:
        interval_sup = len(data_1D[0])-1

    x = data_1D[0, interval_inf:interval_sup]
    y = data_1D[1, interval_inf:interval_sup]
    cen = data_1D[0, indx0]
    slope = (data_1D[1, interval_sup] - data_1D[1, interval_inf]) / (data_1D[0, interval_sup] - data_1D[0, interval_inf])
    intercept = data_1D[1, interval_inf]
    y_to_fit = y - line(x - data_1D[0, interval_inf], slope, intercept)

    mod = Model(gaussian) + Model(line)
    pars = mod.make_params(amp=10., cen=cen, width=0.05, slope=0., intercept=10.)
    result = mod.fit(y_to_fit, pars, x=x)

    print(result.best_values['cen'], abs(result.best_values['width']), result.best_values['amp'])

#    print(result.fit_report())
    import matplotlib.pyplot as plt
    plt.plot(x,y,'ro')
    plt.plot(x, result.best_fit+line(x-data_1D[0,interval_inf],slope,intercept))
    plt.xlabel('q_xy')
    plt.ylabel('I / max(I)')
    plt.show()

    return result.best_values['cen'], abs(result.best_values['width']), result.best_values['amp']


def fit_peaks_spectrum(ID, data_1D, indices, save=False):
    """
    Fit of all the peaks detected (by their channel indices) in the q_xy diagram

    Return
    ------
    array with position, width and amplitude of the peaks detected
    """
    list_fitparam = []
         
    for indx0 in indices:
        cen, width, amplitude = fit_peak(data_1D, indx0)
        list_fitparam.append([cen, width, amplitude])

    array_fitparam = np.array(list_fitparam).reshape(len(indices), 3)

    if save:
        datpath = os.path.join(dir_proc, ID + '-peaks-fit.txt')
        np.savetxt(datpath, array_fitparam, fmt='%.3e %.3e %.3e')

    return array_fitparam


def fit_2peaks(ID, data_1D, indx1, indx2, save=False):
    """
    Gaussian fit of two closed peaks centered around the index1 and indx2  (indx1-indx2 < 15)
    obtained from the array get_peaks_data_1D

    Return
    ------
    position, width and amplitude of the 2 peaks
    """
    
    if indx1 > indx2: 
        indxmax = indx1
        indxmin = indx2
    else:
        indxmax = indx2
        indxmin = indx1 
        
    interval_inf = indxmin - 13  # number of channels=13x2 to cover the peak range
    if interval_inf < 0:
        interval_inf = 0
    interval_sup = indxmax + 13
    if interval_sup > len(data_1D[0])-1:
        interval_sup = len(data_1D[0])-1

    x = data_1D[0, interval_inf:interval_sup]
    y = data_1D[1, interval_inf:interval_sup]
    cen1 = data_1D[0, indx1]
    cen2 = data_1D[0, indx2]   
    print(cen1, cen2)
    slope = (data_1D[1, interval_sup] - data_1D[1, interval_inf]) / (data_1D[0, interval_sup] - data_1D[0, interval_inf])
    intercept = data_1D[1, interval_inf]
    y_to_fit = y - line(x - data_1D[0, interval_inf], slope, intercept)

    mod = Model(bigaussian)+ Model(line)
    pars = mod.make_params(amp1=10., cen1=cen1, width1=0.02, amp2=10., cen2=cen2, width2=0.02, slope=0., intercept=10.)
    result = mod.fit(y_to_fit, pars, x=x)

##    print(result.fit_report())
    import matplotlib.pyplot as plt
    plt.plot(x,y,'ro')
    plt.plot(x, result.best_fit + line(x-data_1D[0,interval_inf],slope,intercept))
    plt.xlabel('q_xy')
    plt.ylabel('I / max(I)')
    plt.show()

    return (result.best_values['cen1'], abs(result.best_values['width1']), result.best_values['amp1'], 
           result.best_values['cen2'], abs(result.best_values['width2']), result.best_values['amp2'])




