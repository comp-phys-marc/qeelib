import random
import tensorflow as tf
from functools import reduce
from .ket import ONE, ZERO

COMPLEX_ZERO = tf.dtypes.complex(0., 0.)
COMPLEX_ONE = tf.dtypes.complex(1., 0.)
COMPLEX_NEG_ONE = tf.dtypes.complex(-1., 0.)
COMPLEX_I = tf.dtypes.complex(0., 1.)
COMPLEX_NEG_I = tf.dtypes.complex(0., -1.)
COMPLEX_ONE_OVER_SQRT_TWO = tf.dtypes.complex(1/tf.math.sqrt(2.), 0.)
COMPLEX_NEG_ONE_OVER_SQRT_TWO = tf.dtypes.complex(-1/tf.math.sqrt(2.), 0.)

ZERO_STATE = tf.linalg.LinearOperatorFullMatrix([COMPLEX_ONE, COMPLEX_ZERO])
ONE_STATE = tf.linalg.LinearOperatorFullMatrix([COMPLEX_ZERO, COMPLEX_ONE])

X = tf.linalg.LinearOperatorFullMatrix([[COMPLEX_ZERO, COMPLEX_ONE],
                                        [COMPLEX_ONE, COMPLEX_ZERO]])

Y = tf.linalg.LinearOperatorFullMatrix([[COMPLEX_ZERO, COMPLEX_NEG_I],
                                        [COMPLEX_I, COMPLEX_ZERO]])

Z = tf.linalg.LinearOperatorFullMatrix([[COMPLEX_ONE, COMPLEX_ZERO],
                                        [COMPLEX_ZERO, COMPLEX_NEG_ONE]])

S = tf.linalg.LinearOperatorFullMatrix([[COMPLEX_ONE, COMPLEX_ONE],
                                        [COMPLEX_ZERO, COMPLEX_I]])

H = tf.linalg.LinearOperatorFullMatrix([[COMPLEX_ONE_OVER_SQRT_TWO, COMPLEX_ONE_OVER_SQRT_TWO],
                                        [COMPLEX_ONE_OVER_SQRT_TWO, COMPLEX_NEG_ONE_OVER_SQRT_TWO]])

M_ONE = tf.linalg.LinearOperatorFullMatrix([[COMPLEX_ONE, COMPLEX_ONE],
                                            [COMPLEX_ZERO, COMPLEX_ZERO]])

M_ZERO = tf.linalg.LinearOperatorFullMatrix([[COMPLEX_ZERO, COMPLEX_ZERO],
                                             [COMPLEX_ONE, COMPLEX_ONE]])

I = tf.linalg.LinearOperatorIdentity(num_rows=2, dtype=tf.complex64)

NULL_MATRIX = tf.linalg.LinearOperatorFullMatrix([[COMPLEX_ZERO, COMPLEX_ZERO],
                                                  [COMPLEX_ZERO, COMPLEX_ZERO]])

KET_ZERO_BRA_ZERO = tf.linalg.LinearOperatorFullMatrix([[COMPLEX_ONE, COMPLEX_ZERO],
                                                        [COMPLEX_ZERO, COMPLEX_ZERO]])

KET_ONE_BRA_ONE = tf.linalg.LinearOperatorFullMatrix([[COMPLEX_ZERO, COMPLEX_ZERO],
                                                      [COMPLEX_ZERO, COMPLEX_ONE]])


class TensorState:
    """
    A class that represents a full quantum state in tensor form.
    """

    def __init__(self, ket_list=[], num_qubits=1, symbol='Ψ'):
        """
        Initializes a quantum state with a given number of qubits.

        :param ket_list: The kets are only used to print the initial state.
        :param num_qubits: The total number of qubits.
        :param symbol: The identifier for this quantum state.
        :raises: ValueError
        """
        super().__init__(ket_list, num_qubits, symbol)

        for ket in ket_list:
            if ONE in ket.get_val():
                raise ValueError("tensor state only supports initialization to |00...0>")

        self.state = reduce(
            lambda state, qubit: tf.linalg.LinearOperatorKronecker([state, qubit]),
            [ZERO_STATE for q in range(num_qubits)]
        )
        self.num_qubits = num_qubits

        self.requirements = {
            'floats': self.state.size(),
            'flops': 0
        }

        print("Initializing tensor state:")
        self.print()

    def _correct_dimensionality(self, op, qubit):
        """
        Performs appropriate Kronecker tensor multiplication of the single qubit
        operator with identities in order to correct the dimensionality of the operator
        so that it may be applied to the full state.

        :param op: The single qubit operator to extend.
        :param qubit: The target qubit.
        :return: The operator extended to the correct size to operate on the full state.
        """
        return reduce(
            lambda state, d_qubit: tf.linalg.LinearOperatorKronecker([state, d_qubit]),
            [(I if q != qubit else op) for q in range(self.num_qubits)]
        )

    def x(self, qubit):
        """
        Performs a Pauli X gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        print("x ({0})".format(qubit), end='')
        print(self.state, end=' ')
        x_matrix = self._correct_dimensionality(X, qubit)
        self.state = tf.linalg.matmul(x_matrix, self.state)
        print(" =", end='')
        print(self.state)
        return self

    def y(self, qubit):
        """
        Performs a Pauli Y gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        print("y ({0})".format(qubit), end='')
        print(self.state, end=' ')
        y_matrix = self._correct_dimensionality(Y, qubit)
        self.state = tf.linalg.matmul(y_matrix, self.state)
        print(" =", end='')
        print(self.state)
        return self

    def z(self, qubit):
        """
        Performs a Pauli Z gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        print("z ({0})".format(qubit), end='')
        print(self.state, end=' ')
        z_matrix = self._correct_dimensionality(Z, qubit)
        self.state = tf.linalg.matmul(z_matrix, self.state)
        print(" =", end='')
        print(self.state)
        return self

    def s(self, qubit):
        """
        Performs an S phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        print("s ({0})".format(qubit), end='')
        print(self.state, end=' ')
        s_matrix = self._correct_dimensionality(S, qubit)
        self.state = tf.linalg.matmul(s_matrix, self.state)
        print(" =", end='')
        print(self.state)
        return self

    def cx(self, source, target):
        """
        Performs a Controlled X gate on the target qubit with the
        source qubit as controller.

        :param source: The source qubit.
        :param source: The target qubit.
        :return: The full quantum state after the opeation.
        """
        print("cx ({0} -> {1})".format(source, target), end='')
        print(self.state, end=' ')
        cx_matrix = tf.math.add(
            self._correct_dimensionality(KET_ZERO_BRA_ZERO, source),
            reduce(
                lambda operator, cx_qubit: tf.linalg.LinearOperatorKronecker([operator, cx_qubit]),
                [
                    (I if (q != source and q != target) else (KET_ONE_BRA_ONE if q == source else X))
                    for q in range(self.num_qubits)
                ]
            )
        )
        self.state = tf.linalg.matmul(cx_matrix, self.state)
        print(" =", end='')
        print(self.state)
        return self

    def h(self, qubit):
        """
        Performs a Hadamard gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        print("h ({0})".format(qubit), end='')
        print(self.state, end=' ')
        h_matrix = self._correct_dimensionality(H, qubit)
        self.state = tf.linalg.matmul(h_matrix, self.state)
        print(" =", end='')
        print(self.state)
        return self

    def collapse(self, qubit, outcome):
        """
        Collapses the target qubit's state.

        :param qubit: The target qubit.
        :param ourcome: The result of the measurement.
        """

        if outcome == ONE:
            collapse_operator = M_ONE
        else:
            collapse_operator = M_ZERO

        c_matrix = reduce(
            lambda state, c_qubit: tf.linalg.LinearOperatorKronecker([state, c_qubit]),
            [(I if q != qubit else collapse_operator) for q in range(self.num_qubits)]
        )

        self.state = tf.linalg.matmul(c_matrix, self.state)
        return outcome

    def m(self, qubit):
        """
        Measures the target qubit.

        :param qubit: The target qubit.
        :return: The result of the measurement.
        """

        # matrix isolates the amplitudes of the target qubit, nulling the rest of the state
        iso_matrix = reduce(
            lambda state, m_qubit: tf.linalg.LinearOperatorKronecker([state, m_qubit]),
            [(NULL_MATRIX if q != qubit else I) for q in range(self.num_qubits)]
        )
        isolated_state = tf.linalg.matmul(iso_matrix, self.state)

        # gets the nested locations of non-zero surviving terms
        target_amp_locs = tf.where(tf.not_equal(isolated_state, COMPLEX_ZERO))

        # finds the first surviving term
        for amp_locs in target_amp_locs[0]:
            for location in amp_locs:
                isolated_state = isolated_state[location]

        # checks if the target is in a pure observable state
        if target_amp_locs.length < 2:
            if target_amp_locs[0][0] == (self.num_qubits/2 + 1):
                return self.collapse(qubit, ONE)
            else:
                return self.collapse(qubit, ZERO)

        # if not a pure observable, measure using pseudo-probability
        else:
            alpha = isolated_state
            return self._measure(alpha)

    def _measure(self, alpha):
        """
        Used pseudo-random number generation to simulate the probabilistic outcome of a qubit
        measurement. Update the quantum system with the measurement results.

        :param alpha: The first component of the qubit's state vector being measured.
        :return: The result of the measurement in the computational basis.
        """
        cutoff = int(tf.math.square(tf.abs(alpha))[0] * 100)
        outcome = random.randint(0, 100)
        if outcome < cutoff:
            return ZERO
        else:
            return ONE

    def register_requirements(self):
        """
        Checks if the current state of the quantum system is the most expensive yet seen during runtime.
        If it is the most expensive state, updates the resource requirements.
        """
        if self.state.size() > self.requirements['floats']:
            self.requirements['floats'] = self.state.size()

        # 2 for number of elements calculated, .5 for the number of terms in each calculation sqrt(size)
        self.requirements['flops'] += self.state.size()**2.5

        return

    def print_requirements(self):
        """
        Prints the requirements for maintaining the current state of the quantum system.
        """
        print({
            'floats': self.state.size(),
            'flops': self.requirements['flops']
        })

    def print_max_requirements(self):
        """
        Prints the requirements for the most expensive state/operation encountered by the class during runtime.
        """
        print(self.requirements)

    def print(self):
        """
        Prints the full quantum tensor state as well as its shape and trace.
        """
        print("State tensor:")
        print(self.state)
        print("Tensor state shape:")
        self.state.shape()
        print("Tensor state trace:")
        tf.linalg.trace(self.state)
