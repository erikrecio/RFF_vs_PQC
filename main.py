import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import pennylane as qml
# from multiprocessing import Pool

import os.path
import time
from datetime import datetime, timedelta

from fourier_coefficients_dD import fourier_coefficients_dD


def main(weights_samples, weights_search, bins_hist, circuit, dev, folder_name):

    weights_max = np.pi
    weights_min = -np.pi

    if weights_search == "grid":
        weights_step = (weights_max - weights_min) / weights_samples
        n_ranges = [np.arange(weights_min + weights_step/2, weights_max, weights_step) for _ in range(circuit.dim_w)]
        nvecs = product(*n_ranges)
    elif weights_search == "random":
        nvecs = np.random.uniform(low=-np.pi, high=np.pi, size=(int(weights_samples**circuit.dim_w), circuit.dim_w))

    # pool = Pool(4)
    # _, _, _, vec_f_inf, vec_f_RKHS = zip(*pool.map(partial(fourier_coefficients_dD, circuit=circuit, d=dim_x), nvecs))

    st = time.time()
    j = 1
    bool_first_time = True

    vec_f_inf = []
    vec_f_RKHS = []
    RKHS_over_inf = []
    temp_nvecs = []
    qnode = qml.QNode(circuit.circuit, dev)
    for i, nvec in enumerate(nvecs,0):
        f_inf, f_RKHS = fourier_coefficients_dD(qnode, nvec, circuit.dim_x)
        vec_f_inf.append(f_inf)
        vec_f_RKHS.append(f_RKHS)
        RKHS_over_inf.append(f_RKHS/f_inf)
        temp_nvecs.append(list(nvec))
        
        perc = (i+1)/int(weights_samples**circuit.dim_w)*100
        et = time.time() - st
        if bool_first_time and et > 20 or perc/j >= 10 or  et/60/j >= 10:
            print(f'{round(perc,2)} %, current = {time.strftime("%H:%M:%S", time.gmtime(et))}, total = {time.strftime("%d %H:%M:%S", time.gmtime(et/perc*100))}, left = {time.strftime("%H:%M:%S", time.gmtime(et/perc*100-et))}, finishes = {(datetime.now() + timedelta(seconds = et/perc*100-et)).strftime("%H-%M-%S %d-%m-%Y")}')
            j = j+1
            bool_first_time = False

    # Save data
    if not os.path.isdir(f'Data/{folder_name}'):
        os.mkdir(f'Data/{folder_name}')
    vec_f_inf = ["Inf. Norm"] + vec_f_inf
    vec_f_RKHS = ["RKHS norm"] + vec_f_RKHS
    RKHS_over_inf = ["RKHS/Inf"] + RKHS_over_inf
    temp_nvecs = [[f"theta_{i}" for i in range(circuit.dim_w)]] + temp_nvecs
    file_name = f'{datetime.now().strftime("%d-%m-%Y %H-%M-%S")} - Norms_and_parameters of {circuit.name} - w={round(weights_samples**circuit.dim_w)}, n={circuit.n_qubits}, L={circuit.layers}, x={circuit.dim_x}'
    np.savetxt(os.path.join(os.path.dirname(__file__), f'Data/{folder_name}/{file_name}.csv'), [[p[0], p[1], p[2], *p[3]] for p in zip(vec_f_inf, vec_f_RKHS, RKHS_over_inf, temp_nvecs)], delimiter=',', fmt='%s')
    vec_f_inf = vec_f_inf[1:]
    vec_f_RKHS = vec_f_RKHS[1:]
    RKHS_over_inf = RKHS_over_inf[1:]
    temp_nvecs = temp_nvecs[1:]

    # Save plots
    if not os.path.isdir(f'Plots/{folder_name}'):
        os.mkdir(f'Plots/{folder_name}')
    names = ["Infiniy norm", "RKHS norm", "RKHS over Infinity"]
    datas = [vec_f_inf, vec_f_RKHS, RKHS_over_inf]

    for name, data in zip(names, datas):
        min_bin = min(data)
        max_bin = max(data)
        width_bin = (max_bin-min_bin)/(bins_hist-1)
        bins = np.arange(min_bin, max_bin + 3*width_bin/2, width_bin) if round(width_bin,8) != 0 else [max_bin - 0.5, max_bin + 0.5]

        plt.hist(data, bins=bins)
        plot_name = f'{name} of {circuit.name} - w={round(weights_samples**circuit.dim_w)}, n={circuit.n_qubits}, L={circuit.layers}, x={circuit.dim_x}'
        plt.title(plot_name)
        plt.xlabel(name)
        plt.xlim(left=0)
        file_name = f'{datetime.now().strftime("%d-%m-%Y %H-%M-%S")} - {plot_name}'
        plt.savefig(os.path.join(os.path.dirname(__file__), f'Plots/{folder_name}/{file_name}.png'))
        plt.clf()