import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from functools import partial
import pennylane as qml
from multiprocessing import Pool
import pandas as pd

import os.path
import time
from datetime import datetime, timedelta
# from pytz import timezone
from backports.zoneinfo import ZoneInfo

from fourier_coefficients_dD import fourier_coefficients_dD


def main2(num_pars, weights_search, bins_hist, circuit, dev, folder_name, num_cpus, par_var):
    
    
    plots_labels = ["Inf. Norm", "Flat RKHS", "FlatRK over norm", "Tree RKHS", "TreeRK over norm"]
    
    if par_var==0:
        nvecs = np.random.uniform(low=-np.pi, high=np.pi, size=(num_pars, circuit.dim_w))
    else:
        rng = np.random.default_rng()
        rand_pars_var = rng.choice(circuit.dim_w, par_var, replace = False)
        fixed_nvec = np.random.uniform(low=-np.pi, high=np.pi, size=circuit.dim_w)
        
        nvecs = np.zeros(shape=(num_pars, circuit.dim_w))
        
        for i in range(num_pars):
            for j in range(circuit.dim_w):
                if j in rand_pars_var:
                    nvecs[i][j] = np.random.uniform(low=-np.pi, high=np.pi, size=1)
                else:
                    nvecs[i][j] = 0 #fixed_nvec[j]
        
    
    qnode = qml.QNode(circuit.circuit, dev)    
    start_time = time.time()

    args = [[qnode, nvec, circuit.dim_x] for nvec in nvecs]
    data = {}
    coeffs = {}
    with Pool(num_cpus) as pool:
        data["Inf. Norm"], data["Flat RKHS"], data["FlatRK over norm"], data["Tree RKHS"], data["TreeRK over norm"], _, data["freq_final"], data["coeffs"] = zip(*pool.starmap(fourier_coefficients_dD, args))            
    
    time_now = datetime.now(ZoneInfo("Europe/Madrid")).strftime("%Y-%m-%d %H-%M-%S")
    name = f"{circuit.name} - x={circuit.dim_x}, n={circuit.n_qubits}, Lx={circuit.layers_x}, Lp={circuit.layers_p}" #w={round(weights_samples**circuit.dim_w)}
    print(f"{time.time()-start_time}s - {name} - {time_now}")
    
    
    # Coeffs data management ###################################
    
    np_coeff = np.stack(data["coeffs"])

    col_names = []
    for nvec in data["freq_final"][0]:
        freqs = "("
        for i, n in enumerate(nvec):
            if i==0:
                freqs += f"{n}"
            else:
                freqs += f",{n}"
        freqs += ")"
        col_names.append(f"c{freqs}")
        col_names.append(f"s{freqs}")

    dic_coeffs = pd.DataFrame(np_coeff, columns=col_names)
    dic_means = dic_coeffs.mean(axis=0)
    dic_std = dic_coeffs.std(axis=0)
    
    # Save data ##################################################
    del data["coeffs"]
    if not os.path.isdir(f'Data/{folder_name}'):
        os.mkdir(f'Data/{folder_name}')
        
    data = pd.DataFrame(data)
    file_name = f'{time_now} - Norms_and_parameters of {name}'
    data.to_csv(f'Data/{folder_name}/{file_name}.csv', index=False)

    
    # Save plots #################################################
    
    if not os.path.isdir(f'Plots/{folder_name}'):
        os.mkdir(f'Plots/{folder_name}')
    
    plt.errorbar(dic_means.index, dic_means, dic_std, capsize=3, fmt="r--o", ecolor = "black")#, linestyle='None', marker='^')
    # plt.ylim(bottom=0)
    # plt.show()
    
    label = "Coeffs"
    plot_name = f'{label} of {name}'
    plt.title(plot_name)
    plt.xlabel(label)
    file_name = f'{time_now} - {plot_name}'
    plt.savefig(os.path.join(os.path.dirname(__file__), f'Plots/{folder_name}/{file_name}.png'))
    plt.clf()
    
    
    for label in plots_labels[2:3]:
        min_bin = min(data[label])
        max_bin = max(data[label])
        width_bin = (max_bin-min_bin)/(bins_hist-1)
        bins = np.arange(min_bin, max_bin + 3*width_bin/2, width_bin) if round(width_bin,8) != 0 else [max_bin - 0.05, max_bin + 0.05]

        plt.hist(data[label], bins=bins)
        plot_name = f'{label} of {name}'
        plt.title(plot_name)
        plt.xlabel(label)
        # if label == "Flat RKHS":
        #     plt.xlim(left=0, right=1)
        plt.xlim(left=0)
        file_name = f'{time_now} - {plot_name}'
        plt.savefig(os.path.join(os.path.dirname(__file__), f'Plots/{folder_name}/{file_name}.png'))
        plt.clf()