import numpy as np
import pennylane as qml
from fourier_coefficients_1D import fourier_coefficients_1D
from fourier_coefficients_dD import *

dev = qml.device('default.qubit', wires=2)

@qml.qnode(dev)
def simple_circuit_marked(w, x):
    qml.RX(x[0], wires=0, id="x0")
    qml.RY(x[0], wires=1, id="x0")
    qml.CNOT(wires=[1, 0])
    return qml.expval(qml.PauliZ(0))

@qml.qnode(dev)
def circuit_with_weights(w, x):
    qml.RX(x[0], wires=0, id="x0")
    qml.RY(x[1], wires=1, id="x1")
    qml.CNOT(wires=[1, 0])

    qml.Rot(*w[0], wires=0)
    qml.Rot(*w[1], wires=1)
    qml.CNOT(wires=[1, 0])

    qml.RX(x[0], wires=0, id="x0")
    # qml.RY(x[1], wires=1, id="x1")
    qml.RX(x[2], wires=0, id="x2")
    qml.CNOT(wires=[1, 0])

    return qml.expval(qml.PauliZ(0))




weights = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])




# freqs, coeffs = fourier_coefficients_1D(simple_circuit_marked, weights, [0.1])

# print(freqs, coeffs)
# print()
# print("next")
# print()

# freqs, coeffs = fourier_coefficients_1D(circuit_with_weights, weights, [0.1])
# print(freqs, coeffs)





# freqs1, coeffs1 = fourier_coefficients_1D(simple_circuit_marked, weights, [0.1])
# print(freqs1, coeffs1)

a = fourier_coefficients_dD_old(simple_circuit_marked, weights, [0.1])
print(a)

a = fourier_coefficients_dD(simple_circuit_marked, weights, [0.1])
print(a)



a = fourier_coefficients_dD_old(circuit_with_weights, weights, [0.1, 0.2, 0.3])
print(a)

a = fourier_coefficients_dD(circuit_with_weights, weights, [0.1, 0.2, 0.3])
print(a)