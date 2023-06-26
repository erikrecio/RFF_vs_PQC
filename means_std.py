#%%
from os import listdir
from os.path import isfile, join
import pandas as pd
import matplotlib.pyplot as plt

# def means_std():
mypath = "Data/3. Circuit 1 1D 100.000/"

csv_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]

mean_inf = []
mean_rkhs = []
mean_inf_rkhs = []
for csv_name in csv_names:

    csv = pd.read_csv(mypath + csv_name)
    # names = ["Infiniy norm", "RKHS norm", "RKHS over Infinity"]
    # data = [csv["Inf. Norm"], csv["RKHS norm"], csv["RKHS/Inf"]]

    mean_inf.append(csv.mean()[0])
    mean_rkhs.append(csv.mean()[1])
    mean_inf_rkhs.append(csv.mean()[2])

    # print(csv_name[46:-4])
    # print(csv.mean()[0:3])
    # print(csv.std()[0:3])


plt.scatter(range(2,15), mean_inf)
plt.show

#%%
plt.scatter(range(2,15), mean_rkhs)
plt.show

#%%
plt.scatter(range(2,15), mean_inf_rkhs)
plt.show
