import matplotlib.pyplot as plt
from datetime import datetime
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
import time
import seaborn as sns


mypath = "Data/00. Old/06. Circuit 3, 10qubits, max L, increasing dim_x/"
csv_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]


for i, csv_name in enumerate(csv_names):
    
    csv = pd.read_csv(mypath + csv_name)

    d = i+1
    L = 10//d
    omega = ((2*L+1)**d-1)/2 + 1
    a = csv["RKHS/Inf"]/np.sqrt(2*omega)
    csv["FlatRK over norm"] = a
    csv.to_csv(f'{mypath}/{csv_name}')

    
    

    # if i==0:
    #     break