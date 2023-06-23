import pennylane as qml
import numpy as np

class Simple_circuit_marked:

    name = "simple_circuit_marked"

    def __init__(self, n_qubits, dim_x):
        self.dim_x = 1
        self.dim_w = 2
        self.n_qubits = 2

    def circuit(self, w, x):
        qml.RX(x[0], wires=0, id="x0")
        qml.RY(x[0], wires=1, id="x0")
        qml.Rot(w[0], w[1], 0, wires=0)
        qml.CNOT(wires=[1, 0])
        return qml.expval(qml.PauliZ(0))


class Circuit_with_weights:

    name = "circuit_with_weights"

    def __init__(self, n_qubits, dim_x):
        self.dim_x = 3
        self.dim_w = 6
        self.n_qubits = 2

    def circuit(self, w, x):
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


class Circuit_1:

    name = "circuit_1"
    
    def __init__(self, n_qubits, dim_x):
        self.dim_x = dim_x
        self.dim_w = 3*n_qubits
        self.n_qubits = n_qubits

    def circuit(self, w, x):

        for i in range(self.n_qubits):
            qml.RX(x[i % self.dim_x], wires=i, id=f"x{i % self.dim_x}")

        for i in range(self.n_qubits):
            qml.Rot(w[i], w[i+1], w[i+2], wires=i)

        for i in range(self.n_qubits):
            if self.n_qubits-i-1 != 0:
                qml.CNOT(wires=[i,i+1])
            else:
                qml.CNOT(wires=[i,0])

        return qml.expval(qml.PauliZ(0))
