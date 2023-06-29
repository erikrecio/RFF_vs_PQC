#%%
from circuits import *

dim_x = 1
layers_x = 4
layers_p = 1
n_qubits = layers_x #layers*dim_x
circuit_class =  Circuit_1 # Simple_circuit_marked, Circuit_with_weights, Circuit_n, Circuit_1qubit, Circuit_big

circuit_object = circuit_class(n_qubits, dim_x, layers_x, layers_p)
dev = qml.device("qiskit.aer", wires = circuit_object.n_qubits)
w = np.random.uniform(size=(circuit_object.dim_w))
x = np.random.uniform(size=(circuit_object.dim_x))
qml.QNode(circuit_object.circuit, dev)(w, x)


print(w[-1])
dev._circuit.draw(output ="mpl", interactive = True)



# %%
import numpy as np
a = nvecs = np.random.uniform(low=-np.pi, high=np.pi, size=(3**6, 6))
print(a)

# temp_nvecs = [0]*circuit.dim_w + temp_nvecs
# %%
