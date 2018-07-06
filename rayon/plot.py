#!/usr/bin/env python

import os.path
import scipy
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from .spectrum import channel2qz

benchmark_ID = 'SIRIUS_2018_06_01_01643'
dir_raw_data = 'RAW-DATA'
dir_plot = 'PLOTS'
dir_processed_data = 'PROC-DATA'


def plot_peaks_data_1D(ID, data_1D, peaks1D_idx, save=False):
    plt.figure(figsize=(10, 5))
    plt.plot(data_1D[0], data_1D[1] / data_1D[1].max())
    plt.xlabel('q_xy')
    plt.ylabel('I / max(I)')
    plt.title(ID)
    for peak_idx in peaks1D_idx:
        plt.plot(data_1D[0][peak_idx], data_1D[1][peak_idx] / data_1D[1].max(), 'o')

    if save:
        figpath = os.path.join(dir_plot, ID + '-peaks-1D.png')
        plt.savefig(figpath)
        plt.close()


def plot_I_qz_peaks(ID, data_1D, I_qz, peaks1D_idx, save=False):

    plt.figure(figsize=(10, 5))

    plt.xlabel('q_z')
    plt.ylabel('I')
    plt.title(ID)
    for num, intensity in enumerate(I_qz[1]):
        qz_peak = data_1D[0][peaks1D_idx[num]]
        qz_peak = np.round(qz_peak, 2)
        plt.plot(I_qz[0], intensity, label=qz_peak)
    plt.legend()

    if save:
        figpath = os.path.join(dir_plot, ID + '-I_qz_peaks.png')
        plt.savefig(figpath)
        plt.close()


def plot_2D_map(ID, data_1D, data_2D, cmap='viridis', save=False):

    plt.figure(figsize=(10, 5))
    qz = channel2qz(np.arange(data_2D.shape[0]))
    extent = [data_1D[0][0], data_1D[0][-1], qz.min(), qz.max()]

    plt.title(benchmark_ID)
    plt.xlabel('q_xy')
    plt.ylabel('q_z')
    plt.imshow(data_2D, cmap=cmap, origin='lower', extent=extent)

    if save:
        figpath = os.path.join(dir_plot, ID + '-2D-map-' + cmap + '.png')
        plt.savefig(figpath)
        plt.close()


def plot_3D(data_1D, data_2D, ID, save=False):
    fig = plt.figure(figsize=(20, 20))
    ax = fig.gca(projection='3d')

    X = data_1D[0]
    Y = channel2qz(np.arange(data_2D.shape[0]))
    X, Y = np.meshgrid(X, Y)

    ax.plot_surface(X, Y, data_2D)
    ax.set_xlabel('q_xy')
    ax.set_ylabel('q_z')
    ax.set_zlabel('I')
    plt.title(ID)

    if save:
        figpath = os.path.join(dir_plot, ID + '-3D.png')
        plt.savefig(figpath)
        plt.close()


def plot_I_q_norm(ID, data_1D, data_2D, save=False):

    plt.figure(figsize=(10, 5))
    X = data_1D[0]
    Y = channel2qz(np.arange(data_2D.shape[0]))
    X, Y = np.meshgrid(X, Y)

    norm = np.sqrt(X**2 + Y**2)

    plt.ylabel('I')
    plt.xlabel('sqrt(q_xy^2 + q_z^2)')
    plt.plot(norm.ravel(), data_2D.ravel(), '.')

    if save:
        figpath = os.path.join(dir_plot, ID + '-q_norm.png')
        plt.savefig(figpath)
        plt.close()
