from functools import reduce
import numpy as np
from copy import deepcopy

I = np.array([1, 0],
             [0, 1])

def correct_dimensionality(self, op, qubit):
    """
    Performs appropriate Kronecker tensor multiplication of the single qubit
    operator with identities in order to correct the dimensionality of the operator
    so that it may be applied to the full state.

    :param op: The single qubit operator to extend.
    :param qubit: The target qubit.
    :return: The operator extended to the correct size to operate on the full state.
    """
    return reduce(
        lambda state, d_qubit: np.kron(state, d_qubit),
        [(I if q != qubit else op) for q in range(self.num_qubits)]
    )

def vector_to_bitstring(vector):
    """
    Converts a vector representation of a state to a bitstring.

    :param vector: The state vector.
    :return:
    """
    num_qubits = np.log2(len(vector))
    bitstring = f'{0:0{num_qubits}b}'
    for i, row in enumerate(vector):
        if row[0] == 1:
            bitstring = f'{i:0{num_qubits}b}'
    return bitstring

def to_sum_of_basis_kets(vector):
    """
    Decomposes a sum of basis vectors into the constituent elements.
    :param vector: The vector representing the sum.
    :return: A list of the individual basis vectors.
    """
    basis_vector = []
    found_p_vectors = []
    found_n_vectors = []
    for i, row in enumerate(vector):
        if row[0] == 1 or row[0] == -1:
            new_vector = deepcopy(basis_vector)
            new_vector.append([1])
        basis_vector.append([0])
        for found in found_p_vectors:
            found.append([0])
        if row[0] > 0:
            found_p_vectors.append(new_vector)
        for found in found_n_vectors:
            found.append([0])
        if row[0] < 0:
            found_n_vectors.append(new_vector)
    for i in range(len(found_p_vectors)):
        found_p_vectors[i] = np.array(found_p_vectors[i])
    for j in range(len(found_n_vectors)):
        found_n_vectors[i] = np.array(found_n_vectors[j])
    return found_p_vectors, found_n_vectors