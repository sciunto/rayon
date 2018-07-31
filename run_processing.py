#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os.path
import os

import numpy as np

import rayon.plot as rpl
import rayon.spectrum as rspc


IDs = (
       'SIRIUS_2018_05_30_01565',
       'SIRIUS_2018_05_30_01567',
       'SIRIUS_2018_05_30_01569',
       'SIRIUS_2018_05_30_01571',
       'SIRIUS_2018_05_30_01573',
       'SIRIUS_2018_05_30_01575',
       'SIRIUS_2018_05_30_01579',
       'SIRIUS_2018_05_31_01585',
       'SIRIUS_2018_05_31_01587',
#       'SIRIUS_2018_05_31_01591', Missing metadata!
       'SIRIUS_2018_05_31_01593',
       'SIRIUS_2018_05_31_01595',
       'SIRIUS_2018_05_31_01597',
       'SIRIUS_2018_05_31_01599',
       'SIRIUS_2018_05_31_01601',
       'SIRIUS_2018_06_01_01641',
       'SIRIUS_2018_06_01_01643',
       'SIRIUS_2018_06_01_01647',
       'SIRIUS_2018_06_01_01649',
       'SIRIUS_2018_06_01_01654',
#       'SIRIUS_2018_06_01_01656',
       'SIRIUS_2018_06_01_01663',
       'SIRIUS_2018_06_01_01683',
       'SIRIUS_2018_06_01_01685',
       'SIRIUS_2018_06_01_01687',
       'SIRIUS_2018_06_01_01697',
       'SIRIUS_2018_06_01_01701',
       'SIRIUS_2018_06_01_01703',
       'SIRIUS_2018_06_01_01717',
       'SIRIUS_2018_06_01_01719',
       'SIRIUS_2018_06_01_01721',
       'SIRIUS_2018_06_02_01725',
       'SIRIUS_2018_06_02_01729',
       'SIRIUS_2018_06_02_01733',
       'SIRIUS_2018_06_02_01735',
       'SIRIUS_2018_06_02_01737',
       'SIRIUS_2018_06_02_01739',
       'SIRIUS_2018_06_02_01741',
       'SIRIUS_2018_06_02_01761',
       'SIRIUS_2018_06_02_01773',
       'SIRIUS_2018_06_02_01791',
       'SIRIUS_2018_06_03_01807',
       'SIRIUS_2018_06_03_01825',
       'SIRIUS_2018_06_03_01829',
       'SIRIUS_2018_06_03_01849',
       'SIRIUS_2018_06_03_01853',
       'SIRIUS_2018_06_03_01855',
       'SIRIUS_2018_06_03_01857',
      )



def task(ID):
    print(ID)
    # Load data 1D and 2D
    data_1D = rspc.load_data_1D(ID)
    data_2D = rspc.load_data_2D(ID)
    # Detect peaks
    peaks1D_idx = rspc.get_peaks_data_1D(data_1D)
 
    # Fit peaks detected
    rspc.fit_peaks_spectrum(ID, data_1D, peaks1D_idx,save=True)

    # Get Profiles
    I_qz = rspc.get_I_qz(ID, data_2D, peaks1D_idx)

    rpl.plot_peaks_data_1D(ID, data_1D, peaks1D_idx, save=True)
    rpl.plot_2D_map(ID, data_1D, data_2D, cmap='plasma', save=True)
    rpl.plot_2D_map(ID, data_1D, data_2D, cmap='gray', save=True)
    rpl.plot_I_qz_peaks(ID, data_1D, I_qz, peaks1D_idx, save=True)
    rpl.plot_I_q_norm(ID, data_1D, data_2D, save=True)
    rpl.plot_3D(data_1D, data_2D, ID, save=True)


for ID in IDs:
    task(ID)



