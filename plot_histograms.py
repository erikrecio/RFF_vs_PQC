import matplotlib.pyplot as plt
from datetime import datetime
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
import time


bins_hist = 100
mypath = "Data/3. Circuit 1, 1D, 100.000/"

csv_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for csv_name in csv_names:

    csv = pd.read_csv(mypath + csv_name)
    names = ["Infiniy norm", "RKHS norm", "RKHS over Infinity"]
    data = [csv["Inf. Norm"], csv["RKHS norm"], csv["RKHS/Inf"]]


    for name, data in zip(names, data):
        min_bin = min(data)
        max_bin = max(data)
        width_bin = (max_bin-min_bin)/(bins_hist-1)
        bins = np.arange(min_bin, max_bin + 3*width_bin/2, width_bin) if round(width_bin,8) != 0 else [max_bin - 0.5, max_bin + 0.5]

        plt.hist(data, bins=bins)
        plot_name = f'{name} of {csv_name[46:-4]}'
        plt.title(plot_name)
        plt.xlabel(name)
        plt.xlim(left=0)
        file_name = f'{datetime.now().strftime("%d-%m-%Y %H-%M-%S")} - {plot_name}'
        plt.savefig(os.path.join(os.path.dirname(__file__), f'Plots/plot_histograms/{file_name}.png'))
        plt.clf()
        time.sleep(1) 