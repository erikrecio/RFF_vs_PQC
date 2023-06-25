#%%
from circuits import *

layers = 3
dim_x = 2
n_qubits = 10 #layers*dim_x
circuit_class = Circuit_3 # Simple_circuit_marked, Circuit_with_weights, Circuit_n

circuit_object = circuit_class(n_qubits, dim_x, layers)
dev = qml.device("qiskit.aer", wires = circuit_object.n_qubits)
w = np.random.uniform(size=(circuit_object.dim_w))
x = np.random.uniform(size=(circuit_object.dim_x))
qml.QNode(circuit_object.circuit, dev)(w, x)

dev._circuit.draw(output ="mpl", interactive = True)

# %%
import numpy as np
a = nvecs = np.random.uniform(low=-np.pi, high=np.pi, size=(3**6, 6))
print(a)

# temp_nvecs = [0]*circuit.dim_w + temp_nvecs
# %%
