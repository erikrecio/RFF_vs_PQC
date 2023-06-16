import numpy as np
import pennylane as qml
from pennylane.fourier import circuit_spectrum, coefficients
from functools import partial

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
    qml.CNOT(wires=[1, 0])

    return qml.expval(qml.PauliZ(0))


def fourier_coefficients_1D(circuit, w, x):

    all_freqs = circuit_spectrum(circuit)(w, x)
    freqs = next(iter(all_freqs.values()))

    num_coeffs = (len(freqs)-1)//2
    coeffs = coefficients(partial(circuit, w), 1, num_coeffs)

    pos_freqs = freqs[num_coeffs:]
    pos_coeffs = []

    for i, c in enumerate(coeffs[:num_coeffs+1]):
        if i == 0:
            cos_coef = c
            sin_coef = 0
        else:
            cos_coef = c + np.conj(c)
            sin_coef = 1j*(c - np.conj(c))
        
        pos_coeffs.extend([np.real(cos_coef), np.real(sin_coef)])

    return pos_freqs, np.round(pos_coeffs, decimals=4)



weights = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])




# freqs, coeffs = fourier_coefficients_1D(simple_circuit_marked, weights, [0.1])

# print(freqs, coeffs)
# print()
# print("next")
# print()

# freqs, coeffs = fourier_coefficients_1D(circuit_with_weights, weights, [0.1])
# print(freqs, coeffs)









def fourier_coefficients_d_dim(circuit, w, x):

    d = len(x)

    freqs = circuit_spectrum(circuit)(w, x)
    num_coeffs = []
    pos_freqs = {}

    for var, fs in freqs.items():
        num_freqs = (len(freqs[var])-1)//2
        
        pos_freqs[var] = fs[num_freqs:]
        num_coeffs.append(num_freqs)

    coeffs = coefficients(partial(circuit, w), d, num_coeffs)
    

    




    print(freqs)
    print(np.round(coeffs, decimals=4))
    print(np.round(coeffs[0][-1], decimals=4))

    print(pos_freqs)


fourier_coefficients_d_dim(circuit_with_weights, weights, [0.3, 0.1])