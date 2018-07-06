#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os.path
import os

import numpy as np

from rayon.plot import *
from rayon.spectrum import *

IDs = ('SIRIUS_2018_05_30_01565',
       'SIRIUS_2018_05_30_01569',
       'SIRIUS_2018_05_30_01579',
       'SIRIUS_2018_05_31_01585',
       'SIRIUS_2018_05_31_01595',
       'SIRIUS_2018_05_31_01599',
       'SIRIUS_2018_06_01_01641',
       'SIRIUS_2018_06_01_01643',
       'SIRIUS_2018_06_01_01647',
       'SIRIUS_2018_06_01_01683',
       'SIRIUS_2018_06_01_01685',
       'SIRIUS_2018_06_01_01687',
       'SIRIUS_2018_06_01_01697',
       'SIRIUS_2018_06_01_01717',
       'SIRIUS_2018_06_01_01721',
       'SIRIUS_2018_06_02_01725',
       'SIRIUS_2018_06_02_01729',
       'SIRIUS_2018_06_02_01733',
       'SIRIUS_2018_06_02_01737',
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


dir_plot = 'PLOTS'
os.makedirs(dir_plot, exist_ok=True)


for ID in IDs:
    print(ID)
    # Load data 1D and 2D
    data_1D = load_data_1D(ID)
    data_2D = load_data_2D(ID)
    # Detect peaks
    peaks1D_idx = get_peaks_data_1D(data_1D)
    # Get Profiles
    I_qz = get_I_qz(ID, data_2D, peaks1D_idx)

    plot_peaks_data_1D(ID, data_1D, peaks1D_idx, save=True)
    plot_2D_map(ID, data_1D, data_2D, cmap='plasma', save=True)
    plot_2D_map(ID, data_1D, data_2D, cmap='gray', save=True)
    plot_I_qz_peaks(ID, data_1D, I_qz, peaks1D_idx, save=True)
    plot_I_q_norm(ID, data_1D, data_2D, save=True)
    plot_3D(data_1D, data_2D, ID, save=True)




