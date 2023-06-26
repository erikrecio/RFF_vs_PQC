#%%
import pennylane as qml
from circuits import *
from main import main


for layers in range(1,2):
    print(layers)

    folder_name = "Testing multiprocessing"
    dim_x = 2
    n_qubits = layers*dim_x
    multicpu = True

    circuit_class = Simple_circuit_marked # Simple_circuit_marked, Circuit_with_weights, Circuit_n
    circuit = circuit_class(n_qubits, dim_x, layers)

    weights_samples = 10000**(1/circuit.dim_w)
    weights_search = "random"  # random, grid
    bins_hist = 100


    dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
    main(weights_samples, weights_search, bins_hist, circuit, dev, folder_name, multicpu)


#%%
from fourier_coefficients_dD import *

L = 4
dim_x = 3
n_qubits = L*dim_x

circuit_class = Circuit_1 # Simple_circuit_marked, Circuit_with_weights, Circuit_n
circuit = circuit_class(n_qubits, dim_x)

w = np.random.uniform(low=-np.pi, high=np.pi, size=(circuit.dim_w))
# w = [0, 0, 0]
dev = qml.device('lightning.qubit', wires=circuit.n_qubits)

a = fourier_coefficients_dD(qml.QNode(circuit.circuit, dev), w, circuit.dim_x)
print(a)

b = fourier_coefficients_dD_not_so_old(qml.QNode(circuit.circuit, dev), w, circuit.dim_x)
print(b)

print(a[1]/b[4])

#%%
import pennylane as qml
from circuits import *
from main import main


for dim_x in range(2,11):
    print(dim_x)
    
    folder_name = "8. Layers = 2, increasing dim_x and n"
    layers = 2 #n_qubits//dim_x
    n_qubits = layers*dim_x
    multicpu = False

    circuit_class = Circuit_3 # Simple_circuit_marked, Circuit_with_weights, Circuit_n
    circuit = circuit_class(n_qubits, dim_x, layers)

    weights_samples = 10000**(1/circuit.dim_w)
    weights_search = "random"  # random, grid
    bins_hist = 100


    dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
    main(weights_samples, weights_search, bins_hist, circuit, dev, folder_name, multicpu)

#%%
import time

et = 3600
print(f'total = {time.strftime("%d %H:%M:%S", time.gmtime(et))}')
