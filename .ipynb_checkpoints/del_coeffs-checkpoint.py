import matplotlib.pyplot as plt
from datetime import datetime
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
import time
import seaborn as sns

mypath = "Data/22. PLOT 3 - Lx=1, Lp=5, increasing dim_x and n/"

csv_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i, csv_name in enumerate(csv_names):
    print(csv_name)
    
    if i!=0:
        data = pd.read_csv(mypath + csv_name)

        del data["coeffs"]
        del data["freq_final"]

        data.to_csv(f'{mypath}/{csv_name}', index=False)
    