#!/usr/bin/env python


import os.path
import os
import numpy as np
import rayon.fluo as fluo


# KCl fluo data only!
IDs =('SIRIUS_Fluo_2018_05_30_01965',
      'SIRIUS_Fluo_2018_05_30_01966',
      'SIRIUS_Fluo_2018_05_30_01967',
      'SIRIUS_Fluo_2018_05_30_01968',
      'SIRIUS_Fluo_2018_05_30_01970',
      'SIRIUS_Fluo_2018_05_31_01971',    
 #     'SIRIUS_Fluo_2018_05_31_01974',
      'SIRIUS_Fluo_2018_06_01_01987',      
      'SIRIUS_Fluo_2018_06_01_01988',        
      'SIRIUS_Fluo_2018_06_01_01989',         
      'SIRIUS_Fluo_2018_06_02_01991',
      'SIRIUS_Fluo_2018_06_02_01992',      
      'SIRIUS_Fluo_2018_06_03_01999',
      'SIRIUS_Fluo_2018_06_03_02000',
      'SIRIUS_Fluo_2018_06_03_02002',
      )


def task(ID):
    data = fluo.load_data_fluo(ID)
    number_of_spectra = data.shape[0]
    time_of_each_spectrum = fluo.read_time(ID)

    intensity_K = np.zeros(number_of_spectra)
    time_all_spectra = np.zeros(number_of_spectra) 

    for i in range(number_of_spectra):
        intensity_K[i] = fluo.peak_ratio_K(data[i])
        time_all_spectra[i] = i*time_of_each_spectrum
    
    fluo.plot_variation_KCl(ID, intensity_K, time_all_spectra, save=True)


dir_plot = 'PLOTS'
os.makedirs(dir_plot, exist_ok=True)
dir_proc = 'PROC-DATA'
os.makedirs(dir_proc, exist_ok=True)

for ID in IDs: 
    print(ID)
    task(ID)
