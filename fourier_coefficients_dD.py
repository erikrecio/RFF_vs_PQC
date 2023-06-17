import numpy as np
import pennylane as qml
from pennylane.fourier import circuit_spectrum, coefficients
from functools import partial

def fourier_coefficients_dD(circuit, w, x):

    d = len(x)

    # Obtain the frequencies of the circuit with this function
    freqs = circuit_spectrum(circuit)(w, x)

    degree = []
    pos_freqs = {}
    for var, fs in freqs.items():
        num_freqs = (len(freqs[var])-1)//2
        
        pos_freqs[var] = fs[num_freqs:] # Keep only the positive frequencies
        degree.append(num_freqs) # Degree of the fourier series for each variable

    coeffs = coefficients(partial(circuit, w), d, degree) # Calculate the fourier coefficients for the exponential expansion
    freq_coeffs, pos_coeffs = sin_cos_transf(d, coeffs, freqs) # Transform the coefficients into the sine-cosine expansion (pos_coeffs) Also returns the frequencies for each coefficient (freq_coeffs).

    return pos_freqs, freq_coeffs, np.round(pos_coeffs, decimals=4)



# Recursive function. Finds all the possible combinations of the frequencies
# given all the features and calculates the sine-cosine coefficients
def sin_cos_transf(d, coeffs, freqs, pos=None, real_freqs=None, coeffs_final=None, freq_final=None, last_i=-1, end=None):
    
    if pos == None:
        pos = []
    if real_freqs == None:
        real_freqs = []
    if coeffs_final == None:
        coeffs_final = []
    if end == None:
        end = [False]
    if freq_final == None:
        freq_final = []

    current_i = last_i + 1
    if current_i == d:
            
        coeff_search = coeffs
        for k in range(d):
            coeff_search = coeff_search[pos[k]]
            
        c = coeff_search

        if tuple(pos) == tuple([0]*d):
            cos_coef = c
            sin_coef = 0
            end[0] = True
        else:
            cos_coef = c + np.conj(c)
            sin_coef = 1j*(c - np.conj(c))
        
        coeffs_final.extend([np.real(cos_coef), np.real(sin_coef)])
        freq_final.append(real_freqs.copy())

        del pos[-1]
        del real_freqs[-1]
    else:
        num_freqs = len(freqs[list(freqs)[current_i]])
        for f in range(-(num_freqs-1)//2, (num_freqs-1)//2 + 1):
            pos.append(f)
            real_freqs.append(freqs[list(freqs)[current_i]][f+(num_freqs-1)//2])

            sin_cos_transf(d, coeffs, freqs, pos, real_freqs, coeffs_final, freq_final, current_i, end)

            if end[0]:
                break
        try:
            del pos[-1]
            del real_freqs[-1]
        except Exception:
            pass

    # The coefficients returned are in increasing order with respect to the frequencies and order of features
    # freq_final specifies which combination of frequencies for each feature goes with the coefficients
    return freq_final, coeffs_final


# Example of the order of returned coefficients

# 'x0': [0, 1, 2]
# 'x1': [0, 1]

# [-2, -1]
# [-2,  0]
# [-2,  1]
# [-1, -1]
# [-1,  0]
# [-1,  1]
# [ 0, -1]
# [ 0,  0]
# [ 0,  1] (doesn't appear because same as [ 0, -1])
# [ 1, -1] (doesn't appear because same as [-1,  1])
# [ 1,  0] (doesn't appear because same as [-1,  0])
# [ 1,  1] (doesn't appear because same as [-1, -1])
# [ 2, -1] (doesn't appear because same as [-2,  1])
# [ 2,  0] (doesn't appear because same as [-2,  0])
# [ 2,  1] (doesn't appear because same as [-2, -1])