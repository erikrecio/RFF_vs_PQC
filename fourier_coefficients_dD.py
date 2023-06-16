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
    pos_coeffs = sin_cos_transf(d, coeffs, freqs) # Transform the coefficients into the sine-cosine expansion

    return pos_freqs, np.round(pos_coeffs, decimals=4)



# Recursive function. Finds all the possible combinations of the frequencies
# given all the features and calculates the sine-cosine coefficients
def sin_cos_transf(d, coeffs, freqs, pos=[], pos_done=[], pos_coeffs = [], last_i=-1, end=False):
    current_i = last_i + 1
    if current_i == d:
        
        if tuple(pos) not in pos_done:
            
            coeff_search = coeffs
            for k in range(d):
                coeff_search = coeff_search[pos[k]]
                
            c = coeff_search

            if tuple(pos) == tuple([0]*d):
                cos_coef = c
                sin_coef = 0
                end = True
            else:
                cos_coef = c + np.conj(c)
                sin_coef = 1j*(c - np.conj(c))
            
            pos_coeffs.extend([np.real(cos_coef), np.real(sin_coef)])

            minus_pos = []
            for j in pos:
                minus_pos.append(-j)

            pos_done.extend([tuple(pos), tuple(minus_pos)])

        del pos[-1]
    else:
        num_freqs = len(freqs[list(freqs)[current_i]])
        for f in range(-(num_freqs-1)//2, (num_freqs-1)//2 + 1):
            pos.append(f)
            sin_cos_transf(d, coeffs, freqs, pos, pos_done, pos_coeffs, current_i, end)
        try:
            del pos[-1]
        except Exception:
            pass

    # The coefficients returned are in increasing order with respect to the frequencies and order of features.
    return pos_coeffs


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





def sin_cos_transf2(d, coeffs, freqs, pos=[], pos_done=[], pos_coeffs = [], last_i=-1):
    current_i = last_i + 1
    if current_i == d:
        
        if tuple(pos) not in pos_done:
            
            coeff_search = coeffs
            for k in range(d):
                coeff_search = coeff_search[pos[k]]
                
            c = coeff_search

            if tuple(pos) == tuple([0]*d):
                cos_coef = c
                sin_coef = 0
            else:
                cos_coef = c + np.conj(c)
                sin_coef = 1j*(c - np.conj(c))
            
            pos_coeffs.extend([np.real(cos_coef), np.real(sin_coef)])

            minus_pos = []
            for j in pos:
                minus_pos.append(-j)

            pos_done.extend([tuple(pos), tuple(minus_pos)])

        del pos[-1]
    else:
        num_freqs = len(freqs[list(freqs)[current_i]])
        for f in range(-(num_freqs-1)//2, (num_freqs-1)//2 + 1):
            pos.append(f)
            sin_cos_transf(d, coeffs, freqs, pos, pos_done, pos_coeffs, last_i=current_i)
        try:
            del pos[-1]
        except Exception:
            pass

    # The coefficients returned are in increasing order with respect to the frequencies and order of features.
    return pos_coeffs