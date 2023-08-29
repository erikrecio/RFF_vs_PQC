#%%
from os import listdir
from os.path import isfile, join
import pandas as pd
import matplotlib.pyplot as plt

# def means_std():
mypath = "Data/22. PLOT 3 - Lx=1, Lp=5, increasing dim_x and n/"

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


plt.scatter(range(2,11), mean_inf)
plt.show

#%%
from scipy.optimize import curve_fit
import numpy as np

x = range(2,11)
y = mean_rkhs
popt, pcov = curve_fit(lambda t, a, b, c: a * np.exp(b * t) + c, x, y)

a = popt[0]
b = popt[1]
c = popt[2]

x_fitted = np.linspace(np.min(x), np.max(x), 100)
y_fitted = a * np.exp(b * x_fitted) + c

plt.scatter(x, y, label = "Raw data")
plt.plot(x_fitted, y_fitted, 'k', label=f'Fitted curve: {round(a,2)}exp({round(b,2)}x){round(c,2)}')
plt.legend()
plt.show

#%%
plt.scatter(range(2,11), mean_inf_rkhs)
plt.show

# %%
from scipy.optimize import curve_fit
import numpy as np

x = range(2,11)
y = mean_rkhs
popt, pcov = curve_fit(lambda t, a, b, c: a*t*t + b*t + c, x, y)

a = popt[0]
b = popt[1]
c = popt[2]

x_fitted = np.linspace(np.min(x), np.max(x), 100)
y_fitted = a*x_fitted**2 + b*x_fitted + c

plt.scatter(x, y, label = "Raw data")
plt.plot(x_fitted, y_fitted, 'k', label=f'Fitted curve: {round(a,2)}x**2 + {round(b,2)}x + {round(c,2)}')
plt.legend()
plt.show