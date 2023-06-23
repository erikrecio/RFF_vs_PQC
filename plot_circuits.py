#%%
from circuits import *

L = 3
dim_x = 2
circuit_class = Circuit_1 # Simple_circuit_marked, Circuit_with_weights, Circuit_n

n_qubits = L*dim_x
circuit_object = circuit_class(n_qubits, dim_x)
dev = qml.device("qiskit.aer", wires = circuit_object.n_qubits)
w = np.random.uniform(size=(circuit_object.dim_w))
x = np.random.uniform(size=(circuit_object.dim_x))
qml.QNode(circuit_object.circuit, dev)(w, x)

dev._circuit.draw(output ="mpl", interactive = True)

# %%
print("\u03B8")

# temp_nvecs = [0]*circuit.dim_w + temp_nvecs
# %%
