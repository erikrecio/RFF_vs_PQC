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


def main(weights_samples, weights_search, bins_hist, circuit, dev, folder_name, num_cpus):

    nvecs = np.random.uniform(low=-np.pi, high=np.pi, size=(int(round(weights_samples**circuit.dim_w)), circuit.dim_w))
    
    qnode = qml.QNode(circuit.circuit, dev)    
    start_time = time.time()

    # if num_cpus > 1:
    args = [[qnode, nvec, circuit.dim_x] for nvec in nvecs]
    data = {}
    coeffs = {}
    with Pool(num_cpus) as pool:
        data["Inf. Norm"], data["Flat RKHS"], data["FlatRK over norm"], data["Tree RKHS"], data["TreeRK over norm"], _, coeffs["freq_final"], coeffs["coeffs"] = zip(*pool.starmap(fourier_coefficients_dD, args))            
    
    data = pd.DataFrame(data)

    time_now = datetime.now(ZoneInfo("Europe/Madrid")).strftime("%Y-%m-%d %H-%M-%S")
    name = f"{circuit.name} - x={circuit.dim_x}, n={circuit.n_qubits}, Lx={circuit.layers_x}, Lp={circuit.layers_p}" #w={round(weights_samples**circuit.dim_w)}
    
    print(f"{time.time()-start_time}s - {name} - {time_now}")

    # Save data ##################################################
    if not os.path.isdir(f'Data/{folder_name}'):
        os.mkdir(f'Data/{folder_name}')
        
    file_name = f'{time_now} - Norms_and_parameters of {name}'
    data.to_csv(f'Data/{folder_name}/{file_name}.csv')

    file_name = f'{time_now} - Coeffs_and_freqs of {name}'
    coeffs.to_csv(f'Data/{folder_name}/{file_name}.csv')
    

    # Save plots #################################################
    if not os.path.isdir(f'Plots/{folder_name}'):
        os.mkdir(f'Plots/{folder_name}')
    
    for label in data:
        min_bin = min(data[label])
        max_bin = max(data[label])
        width_bin = (max_bin-min_bin)/(bins_hist-1)
        bins = np.arange(min_bin, max_bin + 3*width_bin/2, width_bin) if round(width_bin,8) != 0 else [max_bin - 0.5, max_bin + 0.5]

        plt.hist(data[label], bins=bins)
        plot_name = f'{label} of {name}'
        plt.title(plot_name)
        plt.xlabel(label)
        plt.xlim(left=0)
        file_name = f'{time_now} - {plot_name}'
        plt.savefig(os.path.join(os.path.dirname(__file__), f'Plots/{folder_name}/{file_name}.png'))
        plt.clf()