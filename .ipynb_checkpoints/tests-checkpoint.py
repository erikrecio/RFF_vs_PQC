#%%
import pennylane as qml
from circuits import *
from main import main

# Experiment 06

# for dim_x in range(5,11):
#     print(dim_x)

#     folder_name = f"06. Circuit 3, 10qubits, max L, increasing dim_x"
#     # dim_x = 2
#     n_qubits = 10 #layers_x*dim_x
#     layers_x = n_qubits//dim_x
#     layers_p = 1
    
#     circuit_class = Circuit_3 # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big
    
#     circuit = circuit_class(n_qubits, dim_x, layers_x, layers_p)
#     weights_samples = 10000**(1/circuit.dim_w)
#     weights_search = "random"  # random, grid
#     bins_hist = 100
#     num_cpus = 160

#     dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
#     main(weights_samples, weights_search, bins_hist, circuit, dev, folder_name, num_cpus)
    

# Experiment 07

for dim_x in range(2,11):
    print(dim_x)

    folder_name = f"07. Layers = 1, increasing dim_x and n"
    # dim_x = 2
    layers_x = 1
    layers_p = 1
    n_qubits = layers_x*dim_x
    circuit_class = Circuit_3 # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big
    
    circuit = circuit_class(n_qubits, dim_x, layers_x, layers_p)
    weights_samples = 10000**(1/circuit.dim_w)
    weights_search = "random"  # random, grid
    bins_hist = 100
    num_cpus = 160

    dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
    main(weights_samples, weights_search, bins_hist, circuit, dev, folder_name, num_cpus)
    

# Experiment 08

for dim_x in range(1,11):
    print(dim_x)

    folder_name = f"08. Layers = 2, increasing dim_x and n"
    # dim_x = 2
    layers_x = 2
    layers_p = 1
    n_qubits = layers_x*dim_x
    circuit_class = Circuit_3 # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big
    
    circuit = circuit_class(n_qubits, dim_x, layers_x, layers_p)
    weights_samples = 10000**(1/circuit.dim_w)
    weights_search = "random"  # random, grid
    bins_hist = 100
    num_cpus = 160

    dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
    main(weights_samples, weights_search, bins_hist, circuit, dev, folder_name, num_cpus)