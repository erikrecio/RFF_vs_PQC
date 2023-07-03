import numpy as np
import pennylane as qml
from pennylane.fourier import circuit_spectrum, coefficients
from functools import partial
from itertools import product
from scipy.special import binom


def fourier_coefficients_dD(circuit, w, d):

    # Obtain the frequencies of the circuit with this function
    x = [0]*d
    freqs = circuit_spectrum(circuit)(w, x)

    # Degree of the fourier series for each variable
    degree = np.array([int(max(arr)) for arr in freqs.values()])

    # Number of integer values for the indices n_i = -degree_i,...,0,...,degree_i
    k = 2 * degree + 1

    # Create generator for indices nvec = (n1, ..., nN), ranging from (-d1,...,-dN) to (d1,...,dN)
    n_ranges = [np.arange(deg, -deg - 1, -1) for deg in degree]
    nvecs = product(*n_ranges)

    # Here we will collect the discretized values of function f
    f_discrete = np.zeros(shape=tuple(k))

    spacing = (2 * np.pi) / k
    f_inf = 0

    for nvec in nvecs:
        sampling_point = spacing * np.array(nvec)

        # Fill discretized function array with value of f at inputs
        f_discrete[nvec] = circuit(w, sampling_point)
        f_inf = abs(f_discrete[nvec]) if abs(f_discrete[nvec]) > f_inf else f_inf

    coeffs = np.fft.fftn(f_discrete) / f_discrete.size


    # Now we transform the exponential coefficients into the coefficients for cos and sin expansion
    # coeffs_final = []
    # freq_final = []
    end = False
    f_RKHS_flat = 0
    f_RKHS_tree = 0
    norm_pascal = 0
    nvecs = product(*n_ranges)

    for nvec in nvecs:
        # We take the coefficient that goes with the nvec frequencies
        c = coeffs[nvec]
        
        # We calculate the cos and sin coefficients. We stop at 0 since the rest are repetitions of what is already calculated.
        if tuple(nvec) == tuple([0]*d):
            cos_coef = np.real(c)
            sin_coef = 0
            end = True
        else:
            cos_coef = np.real(c + np.conj(c))
            sin_coef = np.real(1j*(c - np.conj(c)))
        
        # coeffs_final.extend([cos_coef, sin_coef]) # coefficients and frequencies, not needed for now
        # freq_final.append(list(nvec))
        f_RKHS_flat += cos_coef**2 + sin_coef**2

        # Calculation of the RKHS norm with a different sampling strategy, tree sampling in this case
        pascal_coef = 1
        for i, w in enumerate(nvec):
            pascal_coef *= binom(2*degree[i], w+degree[i])

        # print(f"nvec = {nvec}, pascal_coef = {pascal_coef}")
        f_RKHS_tree += (cos_coef/pascal_coef)**2 + (sin_coef/pascal_coef)**2
        norm_pascal += pascal_coef**2  #np.sqrt((np.linalg.norm(pascal_coef.flatten())**2 + pascal_coef[x]**2)/2)

        if end:
            break
    
    # Size of half the frequency space
    omega = len(list(nvecs)) + 1
    # print(f"omega = {omega}, norm_pascal**2 = {norm_pascal}")
    # RKHS norm of the function given by the circuit
    f_RKHS_flat = np.sqrt(f_RKHS_flat*omega)
    f_RKHS_tree = np.sqrt(f_RKHS_tree*norm_pascal)

    f_RKHS_flat_inf_omega = f_RKHS_flat/f_inf/np.sqrt(2*omega)
    f_RKHS_tree_inf_omega = f_RKHS_tree/f_inf/np.sqrt(2**(4*sum(degree))+1)
    # coeffs_final = np.round(coeffs_final, decimals=4)

    return f_inf, f_RKHS_flat, f_RKHS_flat_inf_omega, f_RKHS_tree, f_RKHS_tree_inf_omega #freqs, freq_final, coeffs_final,

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



def fourier_coefficients_dD_not_so_old(circuit, w, d):

    # Obtain the frequencies of the circuit with this function
    x = [0]*d
    freqs = circuit_spectrum(circuit)(w, x)

    # Degree of the fourier series for each variable
    degree = np.array([int(max(arr)) for arr in freqs.values()])

    # Number of integer values for the indices n_i = -degree_i,...,0,...,degree_i
    k = 2 * degree + 1

    # Create generator for indices nvec = (n1, ..., nN), ranging from (-d1,...,-dN) to (d1,...,dN)
    n_ranges = [np.arange(deg, -deg - 1, -1) for deg in degree]
    nvecs = product(*n_ranges)

    # Here we will collect the discretized values of function f
    f_discrete = np.zeros(shape=tuple(k))
    pascal_coefs = np.ones(shape=tuple(k))

    spacing = (2 * np.pi) / k
    f_inf = 0

    for nvec in nvecs:
        sampling_point = spacing * np.array(nvec)

        # Fill discretized function array with value of f at inputs
        f_discrete[nvec] = circuit(w, sampling_point)
        f_inf = abs(f_discrete[nvec]) if abs(f_discrete[nvec]) > f_inf else f_inf

    coeffs = (np.fft.fftn(f_discrete) / f_discrete.size).flatten()

    f_RKHS = np.sqrt(2*np.linalg.norm(coeffs)**2 - np.real(coeffs[0])**2)*np.sqrt((len(coeffs)+1)/2)

    return f_inf, f_RKHS


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