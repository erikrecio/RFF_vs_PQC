import numpy as np
import pennylane as qml
from pennylane.fourier import circuit_spectrum, coefficients
from functools import partial

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