#%%
from circuits import *

dim_x = 1
layers_x = 4
layers_p = 1
n_qubits = layers_x #layers_x*dim_x
circuit_class =  Circuit_1 # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big

circuit_object = circuit_class(n_qubits, dim_x, layers_x, layers_p)
dev = qml.device("qiskit.aer", wires = circuit_object.n_qubits)
w = np.random.uniform(size=(circuit_object.dim_w))
x = np.random.uniform(size=(circuit_object.dim_x))
qml.QNode(circuit_object.circuit, dev)(w, x)


print(w[-1])
dev._circuit.draw(output ="mpl", interactive = True)



# %%
from circuits import *
from fourier_coefficients_dD import fourier_coefficients_dD
dim_x = 2
layers_x = 2
layers_p = 1
n_qubits = layers_x*dim_x
circuit_class =  Circuit_big # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big

circuit_object = circuit_class(n_qubits, dim_x, layers_x, layers_p)
dev = qml.device('lightning.qubit', wires=circuit_object.n_qubits)
w = np.random.uniform(size=(circuit_object.dim_w))
x = np.random.uniform(size=(circuit_object.dim_x))
qnode = qml.QNode(circuit_object.circuit, dev)

a = fourier_coefficients_dD(qnode, w, x) #f_inf, f_RKHS_flat, f_RKHS_flat_inf_omega, f_RKHS_tree, f_RKHS_tree_inf_omega

print(a)

# %%
