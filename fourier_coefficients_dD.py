import numpy as np
import pennylane as qml
from pennylane.fourier import circuit_spectrum, coefficients
from functools import partial
from itertools import product


def fourier_coefficients_dD(circuit, w, x):

    d = len(x)

    # Obtain the frequencies of the circuit with this function
    freqs = circuit_spectrum(circuit)(w, x)

    # Degree of the fourier series for each variable
    degree = np.array([int(max(arr)) for arr in freqs.values()])

    # Number of integer values for the indices n_i = -degree_i,...,0,...,degree_i
    k = 2 * degree + 1

    # create generator for indices nvec = (n1, ..., nN), ranging from (-d1,...,-dN) to (d1,...,dN)
    n_ranges = [np.arange(deg, -deg - 1, -1) for deg in degree]
    nvecs = product(*n_ranges)

    # here we will collect the discretized values of function f
    f_discrete = np.zeros(shape=tuple(k))

    spacing = (2 * np.pi) / k
    f_inf = 0

    for nvec in nvecs:
        sampling_point = spacing * np.array(nvec)

        # fill discretized function array with value of f at inputs
        f_discrete[nvec] = circuit(w, sampling_point)
        f_inf = abs(f_discrete[nvec]) if abs(f_discrete[nvec]) > f_inf else f_inf

    coeffs = np.fft.fftn(f_discrete) / f_discrete.size


    # Now we transform the exponential coefficients into the coefficients for cos and sin expansion
    coeffs_final = []
    freq_final = []
    end = False
    f_RKHS = 0
    nvecs = product(*n_ranges)

    for nvec in nvecs:
        # We look for the coefficient that goes with the nvec frequencies
        c = coeffs
        for k in range(d):
            c = c[nvec[k]]
        
        # we calculate the cos and sin coefficients. We stop at 0 since the rest are repetitions of what is already calculated.
        if tuple(nvec) == tuple([0]*d):
            cos_coef = c
            sin_coef = 0
            end = True
        else:
            cos_coef = c + np.conj(c)
            sin_coef = 1j*(c - np.conj(c))
        
        coeffs_final.extend([np.real(cos_coef), np.real(sin_coef)])
        freq_final.append(list(nvec))
        f_RKHS += np.real(cos_coef)**2 + np.real(sin_coef)**2

        if end:
            break
    
    # Size of half the frequency space
    omega = len(list(nvecs)) + 1

    # RKHS norm of the function given by the circuit
    f_RKHS = np.sqrt(f_RKHS*omega)

    coeffs_final = np.round(coeffs_final, decimals=4)

    return freqs, freq_final, coeffs_final, f_inf, f_RKHS


# Example of the order of returned coefficients

# 'x0': [0, 1, 2]
# 'x1': [0, 1]

# [ 2,  1]
# [ 2,  0]
# [ 2, -1]
# [ 1,  1]
# [ 1,  0]
# [ 1, -1]
# [ 0,  1]
# [ 0,  0]
# [ 0, -1] (doesn't appear because same as [ 0,  1])
# [-1,  1] (doesn't appear because same as [ 1, -1])
# [-1,  0] (doesn't appear because same as [ 1,  0])
# [-1, -1] (doesn't appear because same as [ 1,  1])
# [-2,  1] (doesn't appear because same as [ 2, -1])
# [-2,  0] (doesn't appear because same as [ 2,  0])
# [-2, -1] (doesn't appear because same as [ 2,  1])


def fourier_coefficients_dD_old(circuit, w, x):

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
        real_freqs = []
        coeffs_final = []
        end = [False]
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
        for f in range((num_freqs-1)//2, -(num_freqs-1)//2 - 1, -1):
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

    # The coefficients returned are in decreasing order on the frequencies and increasing order on the features
    # freq_final specifies which combination of frequencies for each feature goes with the coefficients
    return freq_final, coeffs_final