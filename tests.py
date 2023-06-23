import pennylane as qml
from circuits import *
from main import main

L = 2
dim_x = 2
circuit_class = Circuit_1 # Simple_circuit_marked, Circuit_with_weights, Circuit_n

weights_samples = 3
bins_hist = 20

n_qubits = L*dim_x
circuit = circuit_class(n_qubits, dim_x)
dev = qml.device('lightning.qubit', wires=circuit.n_qubits)

main(weights_samples, bins_hist, circuit, dev)