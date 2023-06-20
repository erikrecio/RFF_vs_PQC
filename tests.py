import numpy as np
import pennylane as qml
from fourier_coefficients_dD import *
import matplotlib.pyplot as plt
import os.path
from datetime import datetime

dev = qml.device('default.qubit', wires=2)

@qml.qnode(dev)
def simple_circuit_marked(w, x):
    qml.RX(x[0], wires=0, id="x0")
    qml.RY(x[0], wires=1, id="x0")
    qml.Rot(w[0], w[1], 0, wires=0)
    qml.CNOT(wires=[1, 0])
    return qml.expval(qml.PauliZ(0))

@qml.qnode(dev)
def circuit_with_weights(w, x):
    qml.RX(x[0], wires=0, id="x0")
    qml.RY(x[1], wires=1, id="x1")
    qml.CNOT(wires=[1, 0])

    qml.Rot(w[0], w[1], w[2], wires=0)
    qml.Rot(w[3], w[4], w[5], wires=1)
    qml.CNOT(wires=[1, 0])

    qml.RX(x[0], wires=0, id="x0")
    # qml.RY(x[1], wires=1, id="x1")
    qml.RX(x[2], wires=0, id="x2")
    qml.CNOT(wires=[1, 0])

    return qml.expval(qml.PauliZ(0))




weights = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])




# freqs, coeffs = fourier_coefficients_1D(simple_circuit_marked, weights, [0.1])

# print(freqs, coeffs)
# print()
# print("next")
# print()

# freqs, coeffs = fourier_coefficients_1D(circuit_with_weights, weights, [0.1])
# print(freqs, coeffs)





# freqs1, coeffs1 = fourier_coefficients_1D(simple_circuit_marked, weights, [0.1])
# print(freqs1, coeffs1)

# a = fourier_coefficients_dD_old(simple_circuit_marked, weights, [0.1])
# print(a)

# a = fourier_coefficients_dD(simple_circuit_marked, weights, 1)
# print(a)



# a = fourier_coefficients_dD_old(circuit_with_weights, weights, [0.1, 0.2, 0.3])
# print(a)

# a = fourier_coefficients_dD(circuit_with_weights, weights, 3)
# print(a)




weights_max = 2*np.pi
weights_min = -2*np.pi
weights_samples = 3
bins_hist = 10
circuit = circuit_with_weights

if circuit == simple_circuit_marked:
    dim_x = 1 # number of features, dimension of x
    dim_w = 2 # number of parameters
    circuit_name = "simple_circuit_marked"

elif circuit == circuit_with_weights:
    dim_x = 3 # number of features, dimension of x
    dim_w = 6 # number of parameters
    circuit_name = "circuit_with_weights"


weights_step = (weights_max - weights_min) / weights_samples
n_ranges = [np.arange(weights_min + weights_step/2, weights_max, weights_step) for _ in range(dim_w)]
nvecs = product(*n_ranges)

vec_f_inf = []
vec_f_RKHS = []
RKHS_over_inf = []
for i, nvec in enumerate(nvecs):
    _, _, _, f_inf, f_RKHS = fourier_coefficients_dD(circuit, nvec, dim_x)
    vec_f_inf.append(f_inf)
    vec_f_RKHS.append(f_RKHS)
    RKHS_over_inf.append(f_RKHS/f_inf)


min_bin = min(vec_f_inf)
max_bin = max(vec_f_inf)
width_bin = (max_bin-min_bin)/(bins_hist-1)
bins = np.arange(min_bin, max_bin + width_bin/2, width_bin) if width_bin != 0 else 1

plt.hist(vec_f_inf, bins=bins)
plt.title('Histogram of the Infinity norm')
plt.xlabel('Infinity norm')
file_name = f'{datetime.now().strftime("%d-%m-%Y %H-%M-%S")} - Infinity norm of {circuit_name} - weights_samples = {weights_samples}'
plt.savefig(os.path.join(os.path.dirname(__file__), f'Plots\\{file_name}.png'))
plt.clf() 



min_bin = min(vec_f_RKHS)
max_bin = max(vec_f_RKHS)
width_bin = (max_bin-min_bin)/(bins_hist-1)
bins = np.arange(min_bin, max_bin + width_bin/2, width_bin) if width_bin != 0 else 1

plt.hist(vec_f_RKHS, bins=bins)
plt.title('Histogram of the RKHS norm')
plt.xlabel('RKHS norm')
file_name = f'{datetime.now().strftime("%d-%m-%Y %H-%M-%S")} - RKHS norm of {circuit_name} - weights_samples = {weights_samples}'
plt.savefig(os.path.join(os.path.dirname(__file__), f'Plots\\{file_name}.png'))
plt.clf() 



min_bin = min(RKHS_over_inf)
max_bin = max(RKHS_over_inf)
width_bin = (max_bin-min_bin)/(bins_hist-1)
bins = np.arange(min_bin, max_bin + width_bin/2, width_bin) if width_bin != 0 else 1

plt.hist(RKHS_over_inf, bins=bins)
plt.title('Histogram of the RKHS norm over the Infinity Norm')
plt.xlabel('RKHS/Infinity')
file_name = f'{datetime.now().strftime("%d-%m-%Y %H-%M-%S")} - RKHS over Infinity of {circuit_name} - weights_samples = {weights_samples}'
plt.savefig(os.path.join(os.path.dirname(__file__), f'Plots\\{file_name}.png'))
plt.clf() 