import matplotlib.pyplot as plt
from datetime import datetime
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
import time
import seaborn as sns


bins_hist = 100
mypath = "Data/03. Circuit_1 1D 100.000/"
omega = range(3, 16)

csv_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]

abs_max_inf = 0
abs_max_rkhs = 0
abs_max_rkhs_inf = 0

for csv_name in csv_names:
    csv = pd.read_csv(mypath + csv_name)
    abs_max_inf = csv.max()[0] if abs_max_inf < csv.max()[0] else abs_max_inf
    abs_max_rkhs = csv.max()[1] if abs_max_rkhs < csv.max()[1] else abs_max_rkhs
    abs_max_rkhs_inf = csv.max()[2] if abs_max_rkhs_inf < csv.max()[2] else abs_max_rkhs_inf
right_limit = [1.12*abs_max_inf, 1.12*abs_max_rkhs, 1.12*abs_max_rkhs_inf]

for i, csv_name in enumerate(csv_names):

    csv = pd.read_csv(mypath + csv_name)
    names = ["Infiniy norm", "RKHS norm", "RKHS over Infinity"]
    datas = [csv["Inf. Norm"], csv["RKHS norm"], csv["RKHS/Inf"]]


    for j, (name, data) in enumerate(zip(names, datas)):

        min_bin = min(data)
        max_bin = max(data)
        mean = data.mean()
        if name == "Infiniy norm":
            max_inf_norm = max_bin

        print(min_bin, max_bin, mean, max_inf_norm, omega[i], right_limit[j])

        width_bin = (max_bin-min_bin)/(bins_hist-1)
        bins = np.arange(min_bin, max_bin + 3*width_bin/2, width_bin) if round(width_bin,8) != 0 else [max_bin - 0.5, max_bin + 0.5]

        # plt.hist(data, bins=bins, density = True, stacked = True)
        sns.displot(data, kind="kde") #bins=bins, color='blue'
        
        plot_name = f'{name} of {csv_name[46:-4]}'
        plt.title(plot_name)
        plt.xlabel(name)
        plt.xlim(left=0, right=right_limit[j])
        file_name = f'{datetime.now().strftime("%d-%m-%Y %H-%M-%S")} - {plot_name}'
        plt.savefig(os.path.join(os.path.dirname(__file__), f'Plots/plot_histograms/{file_name}.png'), bbox_inches="tight")
        # plt.show()
        plt.clf()
        time.sleep(1)

        

    break