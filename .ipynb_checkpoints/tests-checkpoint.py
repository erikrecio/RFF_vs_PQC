#%%
import pennylane as qml
from circuits import *
from main import main


for layers_x in range(9,11):
    print(layers_x)

    folder_name = f"05. Circuit 1, 2L qubits, 2D, increasing L"
    dim_x = 2
    # layers_x = 2
    layers_p = 1
    n_qubits = layers_x*dim_x
    circuit_class = Circuit_1 # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big
    
    circuit = circuit_class(n_qubits, dim_x, layers_x, layers_p)
    weights_samples = 10000**(1/circuit.dim_w)
    weights_search = "random"  # random, grid
    bins_hist = 100
    num_cpus = 160

    dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
    main(weights_samples, weights_search, bins_hist, circuit, dev, folder_name, num_cpus)