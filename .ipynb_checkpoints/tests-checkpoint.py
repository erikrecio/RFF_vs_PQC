#%%
import pennylane as qml
from circuits import *
from main import main
from main2 import main2


# Experiment 23

for layers_p in range(1,11):
    print(layers_p)

    folder_name = f"23. PLOT 4 - Lx=1, n=dim_x=4, increasing Lp"
    dim_x = 4
    layers_x = 1
    #layers_p = 5
    n_qubits = layers_x*dim_x
    par_var = 0 #0 = max
    
    circuit_class = Circuit_big # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big, Circuit_one_p
    circuit = circuit_class(n_qubits, dim_x, layers_x, layers_p)
    num_pars = 10000
    weights_search = "random"  # random, grid
    bins_hist = 100
    num_cpus = 160

    dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
    main2(num_pars, weights_search, bins_hist, circuit, dev, folder_name, num_cpus, par_var)

    
# # Experiment 22

# for dim_x in range(2,11):
#     print(dim_x)

#     folder_name = f"22. PLOT 3 - Lx=1, Lp=5, increasing dim_x and n"
#     # dim_x = 1
#     layers_x = 1
#     layers_p = 5
#     n_qubits = layers_x*dim_x
#     par_var = 0 #0 = max
    
#     circuit_class = Circuit_big # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big, Circuit_one_p
#     circuit = circuit_class(n_qubits, dim_x, layers_x, layers_p)
#     num_pars = 10000
#     weights_search = "random"  # random, grid
#     bins_hist = 100
#     num_cpus = 160

#     dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
#     main2(num_pars, weights_search, bins_hist, circuit, dev, folder_name, num_cpus, par_var)

# # Experiment 21

# for layers_p in range(1,11):
#     print(layers_p)

#     folder_name = f"21. PLOT 2 - 1D, Lx=n=8, increasing Lp"
#     dim_x = 1
#     layers_x = 8
#     # layers_p = 1
#     n_qubits = layers_x*dim_x
#     par_var = 0 #0 = max
    
#     circuit_class = Circuit_big # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big, Circuit_one_p
#     circuit = circuit_class(n_qubits, dim_x, layers_x, layers_p)
#     num_pars = 10000
#     weights_search = "random"  # random, grid
#     bins_hist = 100
#     num_cpus = 160

#     dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
#     main2(num_pars, weights_search, bins_hist, circuit, dev, folder_name, num_cpus, par_var)


# # Experiment 19 and 20

# for layers_x in range(1,11):
#     print(layers_x)

#     folder_name = f"20. 2D, Lp=3, increasing Lx and n"
#     dim_x = 2
#     # layers_x = 2
#     layers_p = 3
#     n_qubits = layers_x*dim_x
#     circuit_class = Circuit_big # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big

#     circuit = circuit_class(n_qubits, dim_x, layers_x, layers_p)
#     weights_samples = 10000**(1/circuit.dim_w)
#     weights_search = "random"  # random, grid
#     bins_hist = 100
#     num_cpus = 160

#     dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
#     main(weights_samples, weights_search, bins_hist, circuit, dev, folder_name, num_cpus)

# Experiment 16

# for layers_x in range(2,11):
#     print(layers_x)

#     folder_name = f"16. 1D, Lp=1, increasing Lx and n"
#     dim_x = 1
#     # layers_x = 2
#     layers_p = 1
#     n_qubits = layers_x*dim_x
#     circuit_class = Circuit_big # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big

#     circuit = circuit_class(n_qubits, dim_x, layers_x, layers_p)
#     weights_samples = 10000**(1/circuit.dim_w)
#     weights_search = "random"  # random, grid
#     bins_hist = 100
#     num_cpus = 160

#     dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
#     main(weights_samples, weights_search, bins_hist, circuit, dev, folder_name, num_cpus)
    

# # Experiment 17

# for layers_x in range(2,11):
#     print(layers_x)

#     folder_name = f"17. 1D, Lp=5, increasing Lx and n"
#     dim_x = 1
#     # layers_x = 2
#     layers_p = 5
#     n_qubits = layers_x*dim_x
#     circuit_class = Circuit_big # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big

#     circuit = circuit_class(n_qubits, dim_x, layers_x, layers_p)
#     weights_samples = 10000**(1/circuit.dim_w)
#     weights_search = "random"  # random, grid
#     bins_hist = 100
#     num_cpus = 160

#     dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
#     main(weights_samples, weights_search, bins_hist, circuit, dev, folder_name, num_cpus)
    
    
# # Experiment 18

# for layers_p in range(1,11):
#     print(layers_p)

#     folder_name = f"18. 1D, Lx=5, n=5, increasing Lp"
#     dim_x = 1
#     layers_x = 5
#     # layers_p = 5
#     n_qubits = layers_x*dim_x
#     circuit_class = Circuit_big # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big

#     circuit = circuit_class(n_qubits, dim_x, layers_x, layers_p)
#     weights_samples = 10000**(1/circuit.dim_w)
#     weights_search = "random"  # random, grid
#     bins_hist = 100
#     num_cpus = 160

#     dev = qml.device('lightning.qubit', wires=circuit.n_qubits)
#     main(weights_samples, weights_search, bins_hist, circuit, dev, folder_name, num_cpus)

