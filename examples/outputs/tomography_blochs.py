from mpl_toolkits.mplot3d import Axes3D
import functools as ft
import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt
from qiskit.visualization import (
    plot_state_city,
    plot_bloch_multivector,
    plot_state_paulivec,
    plot_state_hinton,
    plot_state_qsphere
)

# Simulated receiver qubit tomography

# message 00 observations
ghz_bloch_vectors_2_0 = np.array([[-0.03125, 0.07421875, 0.029296875], [0.025390625, 0.0234375, -0.001953125], [-0.037109375, 0.01171875, 0.01953125], [0.037109375, 0.005859375, 0.009765625], [0.0, 0.005859375, -0.01171875], [0.009765625, -0.052734375, 0.064453125], [0.029296875, -0.05078125, 0.0078125], [-0.015625, -0.037109375, -0.046875], [-0.064453125, 0.015625, 0.01953125], [-0.013671875, -0.037109375, -0.0078125], [0.001953125, -0.03515625, 0.029296875], [0.017578125, 0.068359375, 0.001953125], [-0.001953125, 0.001953125, 0.076171875], [0.041015625, 0.044921875, 0.05859375], [-0.03125, -0.017578125, -0.00390625], [0.033203125, 0.0, 0.048828125], [0.083984375, 0.009765625, 0.009765625], [-0.0234375, 0.00390625, -0.01171875], [0.083984375, -0.0625, 0.017578125], [-0.01953125, -0.013671875, 0.021484375], [0.01171875, -0.021484375, 0.013671875]])

# message 01 observations
ghz_bloch_vectors_2_1 = np.array([[-0.03125, 0.017578125, 0.01953125], [0.06640625, 0.015625, 0.01953125], [0.021484375, 0.0234375, -0.01171875], [0.00390625, -0.015625, -0.068359375], [0.015625, -0.033203125, 0.03515625], [-0.017578125, 0.005859375, 0.009765625], [-0.009765625, 0.0390625, -0.01171875], [0.0859375, 0.041015625, 0.029296875], [0.01953125, -0.03125, 0.005859375], [0.04296875, 0.00390625, -0.009765625], [-0.025390625, -0.03515625, 0.037109375], [0.021484375, -0.015625, 0.029296875], [0.00390625, -0.01953125, 0.0390625], [-0.0234375, 0.00390625, -0.009765625], [-0.017578125, -0.01953125, -0.046875], [0.015625, 0.0078125, -0.041015625], [-0.0078125, 0.029296875, 0.01171875], [0.04296875, 0.0390625, -0.0234375], [-0.00390625, 0.015625, -0.041015625], [0.029296875, 0.017578125, -0.005859375], [0.03125, 0.0546875, -0.01953125]])

# message 10 observations
ghz_bloch_vectors_2_2 = np.array([[0.05078125, -0.009765625, -0.0234375], [-0.068359375, -0.046875, -0.015625], [0.029296875, 0.041015625, 0.01953125], [-0.015625, -0.060546875, 0.0078125], [-0.009765625, -0.00390625, -0.05078125], [-0.01953125, -0.037109375, 0.044921875], [-0.017578125, -0.009765625, -0.029296875], [-0.005859375, 0.0, -0.021484375], [-0.005859375, 0.05078125, -0.037109375], [0.04296875, 0.064453125, 0.046875], [-0.044921875, 0.00390625, -0.005859375], [0.013671875, 0.015625, -0.01171875], [0.0859375, 0.037109375, 0.005859375], [-0.05078125, -0.001953125, -0.021484375], [-0.0078125, -0.001953125, 0.017578125], [-0.0390625, 0.0234375, 0.005859375], [0.015625, 0.091796875, -0.001953125], [0.046875, -0.001953125, 0.009765625], [-0.01171875, -0.04296875, 0.0], [0.037109375, 0.009765625, 0.001953125], [0.033203125, 0.037109375, 0.021484375]])

# message 11 observations
ghz_bloch_vectors_2_3 = np.array([[-0.05078125, -0.013671875, -0.009765625], [-0.00390625, 0.005859375, -0.013671875], [-0.0234375, -0.03515625, -0.041015625], [0.04296875, 0.041015625, 0.033203125], [0.009765625, -0.02734375, -0.005859375], [-0.00390625, -0.02734375, -0.029296875], [-0.0234375, 0.048828125, 0.015625], [-0.03125, 0.041015625, -0.017578125], [-0.00390625, -0.0234375, 0.01171875], [-0.041015625, 0.0234375, -0.005859375], [-0.0390625, -0.037109375, -0.029296875], [-0.00390625, -0.01171875, 0.03125], [-0.080078125, 0.0, -0.01953125], [-0.05859375, 0.021484375, 0.021484375], [-0.037109375, -0.048828125, -0.0625], [-0.005859375, 0.046875, -0.009765625], [0.025390625, -0.029296875, 0.03515625], [-0.01171875, -0.021484375, -0.02734375], [0.037109375, -0.01171875, -0.091796875], [0.013671875, -0.01171875, -0.041015625], [0.0, 0.0, -0.009765625]])

# message 000 observations
ghz_bloch_vectors_3_0 = np.array([[-0.01953125, -0.0078125, -0.017578125], [0.005859375, -0.015625, 0.056640625], [0.046875, 0.015625, 0.01171875], [0.044921875, -0.05859375, 0.005859375], [-0.0234375, 0.021484375, 0.0078125], [-0.068359375, 0.029296875, -0.072265625], [-0.052734375, -0.056640625, -0.0234375], [-0.02734375, -0.00390625, -0.021484375], [-0.009765625, 0.033203125, -0.01953125], [-0.0390625, -0.01953125, -0.013671875], [0.06640625, 0.02734375, -0.04296875], [-0.048828125, 0.025390625, 0.015625], [0.052734375, -0.01171875, 0.005859375], [0.046875, -0.0078125, 0.0234375], [0.0078125, 0.03125, -0.0703125], [-0.005859375, -0.02734375, 0.01171875], [-0.037109375, 0.00390625, -0.05078125], [-0.0078125, -0.009765625, 0.005859375], [-0.04296875, -0.029296875, 0.013671875], [-0.037109375, 0.025390625, 0.009765625], [-0.041015625, -0.009765625, 0.00390625]])

# message 001 observations
ghz_bloch_vectors_3_1 = np.array([[-0.00390625, -0.068359375, -0.0546875], [0.0234375, 0.001953125, 0.009765625], [0.01953125, -0.021484375, 0.029296875], [0.017578125, 0.044921875, -0.017578125], [0.013671875, 0.04296875, -0.015625], [0.021484375, -0.02734375, 0.0234375], [-0.0078125, -0.048828125, 0.01953125], [0.0390625, 0.0234375, 0.015625], [0.013671875, -0.041015625, 0.017578125], [-0.052734375, -0.060546875, -0.00390625], [0.0078125, 0.0234375, -0.03515625], [0.02734375, 0.025390625, 0.021484375], [-0.015625, 0.025390625, -0.046875], [-0.005859375, 0.0234375, -0.0234375], [-0.005859375, -0.05078125, 0.005859375], [-0.033203125, -0.00390625, 0.052734375], [-0.005859375, 0.06640625, 0.033203125], [-0.046875, 0.01171875, -0.041015625], [0.033203125, -0.0078125, 0.015625], [0.044921875, -0.00390625, 0.0], [-0.025390625, -0.037109375, -0.021484375]])

# message 010 observations
ghz_bloch_vectors_3_2 = np.array([[0.060546875, -0.08203125, 0.095703125], [-0.0078125, -0.0078125, -0.017578125], [0.05078125, 0.009765625, -0.025390625], [-0.037109375, 0.013671875, -0.017578125], [0.037109375, -0.0234375, 0.03515625], [0.01953125, 0.02734375, -0.029296875], [-0.01171875, -0.033203125, 0.015625], [-0.025390625, 0.0078125, 0.0234375], [0.03125, 0.005859375, 0.00390625], [-0.033203125, 0.009765625, -0.021484375], [0.017578125, -0.0078125, 0.0234375], [0.009765625, 0.025390625, 0.03515625], [0.041015625, 0.01171875, 0.00390625], [-0.044921875, -0.013671875, -0.017578125], [-0.0234375, -0.005859375, -0.02734375], [-0.01171875, 0.017578125, -0.037109375], [-0.03515625, 0.009765625, -0.03515625], [0.00390625, -0.015625, 0.0234375], [0.064453125, 0.005859375, 0.048828125], [0.03125, -0.005859375, 0.0234375], [-0.03515625, 0.021484375, 0.056640625]])

# message 011 observations
ghz_bloch_vectors_3_3 = np.array([[0.02734375, -0.048828125, -0.01171875], [-0.015625, -0.03125, -0.03515625], [-0.03125, 0.0546875, 0.017578125], [0.001953125, 0.068359375, -0.0234375], [-0.056640625, -0.015625, -0.0390625], [-0.005859375, -0.001953125, 0.0], [-0.03125, 0.005859375, -0.01171875], [-0.02734375, -0.001953125, -0.03515625], [0.001953125, -0.0390625, -0.04296875], [0.021484375, -0.015625, 0.0078125], [0.044921875, -0.033203125, -0.021484375], [0.00390625, 0.072265625, 0.017578125], [-0.033203125, -0.03515625, 0.025390625], [-0.015625, 0.001953125, -0.009765625], [0.015625, -0.033203125, -0.0390625], [-0.00390625, 0.00390625, -0.037109375], [0.0, -0.033203125, -0.017578125], [-0.017578125, 0.02734375, -0.009765625], [0.03125, -0.029296875, -0.0546875], [-0.005859375, -0.01953125, -0.0078125], [0.005859375, -0.00390625, 0.029296875]])

# message 100 observations
ghz_bloch_vectors_3_4 = np.array([[0.025390625, 0.013671875, 0.07421875], [0.013671875, 0.01171875, -0.0546875], [-0.009765625, 0.005859375, -0.02734375], [0.005859375, -0.009765625, -0.017578125], [-0.021484375, -0.025390625, -0.052734375], [-0.00390625, -0.0078125, -0.0078125], [-0.001953125, -0.056640625, 0.0234375], [0.03125, 0.08984375, -0.033203125], [0.046875, -0.041015625, -0.005859375], [-0.037109375, 0.017578125, -0.056640625], [0.001953125, 0.033203125, -0.009765625], [-0.046875, 0.0, -0.041015625], [0.037109375, -0.001953125, -0.0078125], [0.015625, -0.033203125, 0.02734375], [-0.01171875, -0.03515625, -0.021484375], [0.021484375, 0.05078125, 0.001953125], [0.00390625, 0.001953125, 0.048828125], [0.052734375, -0.025390625, 0.103515625], [0.005859375, -0.0546875, 0.001953125], [-0.037109375, 0.025390625, -0.029296875], [0.03125, -0.01171875, -0.005859375]])

# message 101 observations
ghz_bloch_vectors_3_5 = np.array([[0.015625, 0.017578125, 0.029296875], [0.033203125, 0.0546875, -0.009765625], [0.013671875, -0.009765625, 0.041015625], [-0.001953125, 0.0078125, -0.02734375], [0.0, -0.009765625, -0.01171875], [0.017578125, 0.01953125, -0.029296875], [0.087890625, 0.025390625, -0.08203125], [-0.06640625, -0.001953125, 0.04296875], [-0.048828125, 0.00390625, 0.04296875], [0.0078125, -0.037109375, -0.0234375], [-0.021484375, 0.04296875, 0.013671875], [-0.017578125, -0.01953125, -0.009765625], [-0.021484375, 0.041015625, -0.013671875], [0.052734375, 0.017578125, 0.0390625], [-0.033203125, 0.021484375, 0.025390625], [-0.099609375, -0.013671875, 0.033203125], [-0.02734375, 0.005859375, -0.0234375], [-0.005859375, -0.017578125, 0.015625], [0.0390625, 0.009765625, 0.029296875], [-0.029296875, -0.0234375, -0.009765625], [-0.060546875, -0.01953125, -0.01953125]])

# message 110 observations
ghz_bloch_vectors_3_6 = np.array([[0.0390625, 0.044921875, 0.0078125], [-0.076171875, 0.013671875, 0.01171875], [-0.0390625, -0.052734375, -0.01171875], [-0.056640625, 0.037109375, -0.013671875], [0.015625, 0.01953125, 0.02734375], [-0.025390625, -0.0078125, 0.037109375], [-0.033203125, -0.0078125, -0.00390625], [-0.05078125, -0.041015625, 0.048828125], [-0.03125, -0.076171875, 0.00390625], [0.015625, -0.0234375, -0.03515625], [0.01953125, -0.009765625, -0.041015625], [-0.017578125, 0.00390625, 0.01171875], [-0.01953125, 0.013671875, -0.00390625], [0.01953125, 0.02734375, 0.03125], [-0.015625, 0.037109375, -0.04296875], [0.00390625, 0.009765625, -0.03125], [0.0234375, -0.021484375, -0.0234375], [0.078125, 0.0, -0.064453125], [0.0390625, -0.01953125, 0.03125], [0.05078125, -0.025390625, -0.01171875], [0.041015625, -0.009765625, -0.044921875]])

# message 111 observations
ghz_bloch_vectors_3_7 = np.array([[-0.01171875, 0.0, -0.05859375], [0.009765625, -0.056640625, 0.001953125], [-0.015625, -0.00390625, 0.00390625], [0.037109375, 0.005859375, -0.03515625], [-0.005859375, 0.0703125, 0.001953125], [-0.056640625, 0.01171875, 0.017578125], [-0.078125, 0.021484375, -0.02734375], [0.013671875, -0.015625, 0.044921875], [-0.05859375, -0.044921875, 0.03125], [-0.005859375, 0.044921875, 0.04296875], [-0.001953125, -0.03515625, 0.017578125], [0.021484375, -0.017578125, -0.00390625], [-0.0078125, -0.041015625, 0.009765625], [-0.005859375, 0.0234375, 0.029296875], [-0.01171875, 0.005859375, 0.001953125], [-0.037109375, -0.041015625, -0.013671875], [-0.001953125, 0.00390625, -0.04296875], [0.009765625, -0.052734375, 0.017578125], [-0.01953125, -0.005859375, 0.02734375], [-0.015625, 0.037109375, -0.0078125], [-0.033203125, -0.033203125, -0.033203125]])

# ghz-like message 00 observations
ghz_like_bloch_vectors_2_0 = np.array([[0.046875, 0.048828125, 0.02734375], [0.015625, 0.017578125, 0.001953125], [0.01171875, -0.015625, -0.017578125], [-0.01171875, 0.009765625, -0.01953125], [0.0, 0.009765625, 0.021484375], [0.08203125, 0.001953125, 0.00390625], [0.015625, -0.029296875, -0.046875], [-0.021484375, -0.001953125, 0.01171875], [0.060546875, -0.013671875, 0.005859375], [0.04296875, 0.01171875, 0.06640625], [0.044921875, -0.044921875, 0.064453125], [-0.01953125, 0.029296875, -0.009765625], [0.015625, -0.001953125, 0.025390625], [-0.05078125, -0.017578125, -0.017578125], [0.037109375, 0.01953125, -0.001953125], [0.03125, -0.01953125, 0.013671875], [0.037109375, 0.01171875, 0.001953125], [0.017578125, 0.07421875, 0.009765625], [-0.03125, 0.03515625, 0.037109375], [-0.015625, 0.017578125, -0.048828125], [0.0078125, 0.021484375, 0.017578125]])

# ghz-like message 01 observations
ghz_like_bloch_vectors_2_1 = np.array([[0.015625, -0.04296875, -0.046875], [0.033203125, 0.06640625, -0.029296875], [0.056640625, 0.001953125, 0.00390625], [0.017578125, -0.052734375, -0.001953125], [0.001953125, 0.08984375, -0.015625], [-0.005859375, 0.033203125, 0.021484375], [-0.01953125, 0.009765625, -0.03515625], [-0.013671875, -0.029296875, 0.0546875], [-0.01171875, -0.029296875, 0.021484375], [0.013671875, 0.0, -0.05078125], [0.03125, -0.048828125, -0.0078125], [0.005859375, 0.00390625, -0.01953125], [0.0078125, -0.001953125, 0.046875], [0.0390625, 0.015625, 0.001953125], [0.064453125, -0.01953125, 0.01171875], [0.02734375, 0.01171875, -0.044921875], [0.0234375, -0.009765625, -0.005859375], [-0.01171875, 0.052734375, 0.025390625], [-0.021484375, 0.005859375, -0.0078125], [0.037109375, -0.013671875, -0.048828125], [-0.041015625, 0.0234375, -0.01953125]])

# ghz-like message 10 observations
ghz_like_bloch_vectors_2_2 = np.array([[-0.046875, -0.025390625, 0.0], [-0.021484375, 0.033203125, 0.009765625], [-0.01171875, 0.00390625, 0.00390625], [-0.017578125, -0.025390625, -0.01171875], [-0.01953125, -0.03125, 0.00390625], [0.060546875, 0.005859375, 0.0078125], [0.001953125, -0.037109375, 0.001953125], [-0.017578125, -0.025390625, -0.01953125], [-0.03515625, -0.046875, -0.01171875], [0.0234375, 0.01171875, -0.0078125], [-0.0078125, 0.029296875, 0.06640625], [0.0234375, -0.009765625, 0.005859375], [0.017578125, -0.046875, -0.025390625], [0.02734375, 0.041015625, -0.01953125], [0.01953125, -0.015625, -0.001953125], [0.0859375, 0.013671875, -0.013671875], [-0.0078125, -0.037109375, -0.056640625], [-0.005859375, -0.052734375, -0.013671875], [-0.0234375, 0.00390625, -0.013671875], [-0.0703125, 0.00390625, -0.037109375], [0.01953125, 0.021484375, -0.0078125]])

# ghz-like message 11 observations
ghz_like_bloch_vectors_2_3 = np.array([[-0.080078125, -0.041015625, 0.04296875], [-0.025390625, 0.001953125, 0.0234375], [0.02734375, 0.001953125, 0.017578125], [-0.021484375, -0.005859375, 0.0], [0.03125, 0.013671875, -0.03515625], [0.001953125, 0.001953125, 0.0], [-0.05078125, 0.03515625, 0.005859375], [-0.046875, -0.01171875, -0.001953125], [0.00390625, 0.041015625, -0.01953125], [-0.013671875, -0.013671875, 0.029296875], [-0.0390625, 0.0546875, -0.05859375], [0.013671875, 0.0, -0.005859375], [-0.0390625, -0.03125, 0.037109375], [0.021484375, -0.015625, 0.001953125], [0.046875, 0.01953125, -0.02734375], [0.001953125, -0.0390625, 0.029296875], [-0.03515625, -0.015625, -0.009765625], [0.01953125, -0.017578125, -0.052734375], [0.029296875, -0.080078125, -0.046875], [-0.0390625, 0.001953125, -0.029296875], [-0.001953125, -0.0390625, 0.08203125]])

# Real server qubit tomography

# ghz-like message 00 observation
ghz_like_real_bloch_vectors_2_0 = np.array([[-0.373046875, 0.134765625, -0.138671875], [-0.47265625, 0.03515625, -0.1328125], [-0.328125, -0.091796875, -0.095703125], [-0.296875, -0.177734375, -0.1875], [-0.22265625, -0.279296875, -0.115234375], [-0.037109375, -0.341796875, -0.052734375], [0.0078125, -0.3203125, -0.068359375], [0.158203125, -0.306640625, -0.14453125], [0.310546875, -0.24609375, -0.080078125], [0.33203125, -0.25, -0.177734375], [0.388671875, -0.203125, -0.51953125], [0.486328125, -0.04296875, -0.19921875], [0.3984375, 0.05859375, -0.060546875], [0.287109375, 0.220703125, -0.17578125], [0.17578125, 0.37109375, 0.095703125], [-0.01171875, 0.326171875, 0.017578125], [-0.013671875, 0.341796875, 0.08984375], [-0.060546875, 0.169921875, -0.0234375], [-0.18359375, 0.19140625, 0.1171875], [-0.09375, 0.044921875, -0.083984375], [-0.396484375, 0.130859375, 0.021484375]])

cases = [
    # ghz_bloch_vectors_2_0,
    # ghz_bloch_vectors_2_1,
    # ghz_bloch_vectors_2_2,
    # ghz_bloch_vectors_2_3,
    # ghz_bloch_vectors_3_0,
    # ghz_bloch_vectors_3_1,
    # ghz_bloch_vectors_3_2,
    # ghz_bloch_vectors_3_3,
    # ghz_bloch_vectors_3_4,
    # ghz_bloch_vectors_3_5,
    # ghz_bloch_vectors_3_6,
    # ghz_bloch_vectors_3_7,
    # ghz_like_bloch_vectors_2_0,
    # ghz_like_bloch_vectors_2_1,
    # ghz_like_bloch_vectors_2_2,
    # ghz_like_bloch_vectors_2_3,
    ghz_like_real_bloch_vectors_2_0
]

for bloch_vectors in cases:

    # plot all observed vectors
    origin = [0], [0], [0]
    x, y, z = zip(*bloch_vectors)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(*origin, x, y, z)

    plt.title("Measurements sampled during tomography")
    plt.show()

    # sum all observed vectors
    x = ft.reduce(lambda pre, curr: pre + curr, x)
    y = ft.reduce(lambda pre, curr: pre + curr, y)
    z = ft.reduce(lambda pre, curr: pre + curr, z)

    # normalize bloch vector
    n = linalg.norm(np.array([x, y, z]))
    x = x/n
    y = y/n
    z = z/n

    I = np.array([[1, 0],
                  [0, 1]])

    X = np.array([[0, 1],
                  [1, 0]])

    Y = np.array([[0, np.complex(0, -1)],
                  [np.complex(0, 1), 0]])

    Z = np.array([[1, 0],
                  [0, -1]])

    density_matrix = I + x * X + y * Y + z * Z

    print("Density matrix:")
    print("I + {0:.3f} X + {1:.3f} Y + {2:.3f} Z".format(x, y, z))
    print(np.round(density_matrix, 3))

    print("Bloch vector:\nx: {0:.3f}\ny: {1:.3f}\nz: {2:.3f}".format(x, y, z))

    # plot bloch vector
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.quiver(*origin, x, y, z)

    # plot sphere
    u = np.linspace(0, 2 * np.pi, 13)
    v = np.linspace(0, np.pi, 7)

    x = 1 * np.outer(np.cos(u), np.sin(v))
    y = 1 * np.outer(np.sin(u), np.sin(v))
    z = 1 * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, rstride=1, cstride=1, color='w', shade=1, alpha=0.5)

    plt.title("Reconstructed Bloch vector")
    plt.show()

    city_fig = plot_state_city(density_matrix)
    city_fig.show()
    qsphere_fig = plot_state_qsphere(density_matrix)
    qsphere_fig.show()
    multi_fig = plot_bloch_multivector(density_matrix)
    multi_fig.show()
    paulivec_fig = plot_state_paulivec(density_matrix)
    paulivec_fig.show()
    hinton_fig = plot_state_hinton(density_matrix)
    hinton_fig.show()


