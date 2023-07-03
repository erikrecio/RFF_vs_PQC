import matplotlib.pyplot as plt
from datetime import datetime
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
import time
import seaborn as sns


mypath = "Data/13.2 10q, 2D, Lp=10, increasing Lx/"
num_csv = 5
labels_remove = []
# labels_data = [
#     "Lp = 1",
#     "Lp = 2",
#     "Lp = 3",
#     "Lp = 4",
#     "Lp = 5",
#     "Lp = 6",
#     "Lp = 7",
#     "Lp = 8",
#     "Lp = 9",
#     "Lp = 10",
# ]

labels_data = [
    "Lx=1",
    "Lx=2",
    "Lx=3",
    "Lx=4",
    "Lx=5",
    # "Lx=6",
    # "Lx=7",
    # "Lx=8",
    # "Lx=9",
    # "Lx=10",
]

# labels_data = [
#     "n=2",
#     "n=3",
#     "n=4",
#     "n=5",
#     "n=6",
#     "n=7",
#     "n=8",
#     "n=9",
#     "n=10",
#     "n=11",
#     "n=12",
#     "n=13",
#     "n=14",
# ]


csv_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# csv_names = [f for i, f in enumerate(csv_names) if i not in labels_remove]
# labels_data = [l for i, l in enumerate(labels_data) if i not in labels_remove]

abs_max_inf = 0
abs_max_rkhs = 0
abs_max_rkhs_inf = 0

data_inf = {}
data_rkhs = {}
data_inf_rkhs = {}

for i, csv_name in enumerate(csv_names):
    
    if i%(len(labels_data)//num_csv)==0 and i not in labels_remove:
    
        csv = pd.read_csv(mypath + csv_name)

        max = csv.max()
        abs_max_inf = max[0] if abs_max_inf < max[0] else abs_max_inf
        abs_max_rkhs = max[1] if abs_max_rkhs < max[1] else abs_max_rkhs
        abs_max_rkhs_inf = max[2] if abs_max_rkhs_inf < max[2] else abs_max_rkhs_inf

        names = ["Infiniy norm", "RKHS norm", "RKHS over Infinity"]
        data_inf[labels_data[i]] = list(csv["Inf. Norm"])
        data_rkhs[labels_data[i]] = list(csv["RKHS norm"])
        data_inf_rkhs[labels_data[i]] = list(csv["RKHS/Inf"])


right_limit = [1.12*abs_max_inf, 1.12*abs_max_rkhs, 1.12*abs_max_rkhs_inf]
names = ["Infiniy norm", "RKHS norm", "RKHS over Infinity"]
datas = [pd.DataFrame(data_inf), pd.DataFrame(data_rkhs), pd.DataFrame(data_inf_rkhs)]

for j, (name, data) in enumerate(zip(names, datas)):

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