from functools import reduce
import numpy as np

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