import numpy as np
from .linear_algebra import vector_to_bitstring, correct_dimensionality, to_sum_of_basis_kets

ZERO = np.array([[1],
                 [0]])
ONE = np.array([[0],
                [1]])


class Ket:
    """
    A class that represents the data associated with a single computatonal basis ket in a quantum state.
    TODO: add support for other bases.
    TODO: create Gate class or just decorator honestly.
    """
    
    def __init__(self, coeff=None, val=None):
        """
        Initializes a ket with a value and coefficient.

        :param coeff: The ket's complex coefficient.
        :param val: The qubit string value.
        """
        self.set_coefficient(coeff)
        self.set_val(val)
        
    def __eq__(self, other):
        """
        The equality of kets compares their qubit strings and their coefficients.

        :param other: Another ket.
        :return: Whether they are the same ket.
        """
        if isinstance(other, Ket):
            return self._val == other.get_val() and self._coefficient == other.get_coefficient()
        return False
        
    def get_val(self):
        """
        The qubit string value of the ket.

        :return: The qubit string.
        """
        return self._val

    def get_coefficient(self):
        """
        Returns the coefficient of the ket.

        :return: The ket's coefficient.
        """
        return self._coefficient
        
    def set_val(self, val):
        """
        Sets the qubit string value for the ket.

        :param val:
        :return:
        """
        self._val = None
        self.num_qubits = len(val)
        if isinstance(val, str):
            for bit in val:
                if bit not in ['0', '1']:
                    self._val = None
                    raise ValueError("state value {0} is not entirely 1's and 0's".format(val))
                if bit == '0':
                    if self._val is None:
                        self._val = ZERO
                    else:
                        self._val = np.kron(self._val, ZERO)
                if bit == '1':
                    if self._val is None:
                        self._val = ONE
                    else:
                        self._val = np.kron(self._val, ONE)

    def set_coefficient(self, coeff):
        """
        Sets the coefficient of the ket's term in the overall quantum state.

        :param coeff: The coefficient of the ket.
        :raises: ValueError
        """
        if isinstance(coeff, complex):
            self._coefficient = coeff
        else:
            raise ValueError("setting coefficient of incorrect type was attempted")
            
    def get_probability(self):
        """
        Determines the probabilistic weight of the ket within
        its overall quantum state.

        :return: The probabilistic weight of the ket.
        """
        return abs(self._coefficient) ** 2
        
    def x(self, qubit):
        """
        Performs a Pauli X gate on the target qubit.

        :param qubit: The target qubit.
        :return: The ket after the operation.
        """
        targeted_gate = correct_dimensionality(
            np.array([[0, 1],
                     [1, 0]]),
            qubit,
            self.num_qubits
        )
        self._val = np.matmul(targeted_gate, self._val)
        return self

    def s(self, qubit):
        """
        Performs an S phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: The ket after the operation.
        """
        if vector_to_bitstring(self._val)[qubit] == '1':
            self._coefficient = self._coefficient * complex(0, 1)
        return self

    def sdg(self, qubit):
        """
        Performs an S dagger phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: The ket after the operation.
        """
        if vector_to_bitstring(self._val)[qubit] == '1':
            self._coefficient = self._coefficient * -complex(0, 1)
        return self
    
    def cx(self, source, target):
        """
        Performs a Controlled X gate on the target qubit with the
        source qubit as controller.

        :param source: The source qubit.
        :param target: The target qubit.
        :return: The ket after the operation.
        """

        cx_matrix = [[0. for _ in range(len(self._val))] for _ in range(len(self._val))]

        for i, row in enumerate(cx_matrix):
            label = f'{i:0{self.num_qubits}b}'
            if label[source] == '1':
                label = label[0:target] + ('0' if label[target] == '1' else '1') + label[target+1:]
            one_position = int(label, 2)
            row[one_position] = 1.

        cx_gate = np.array(cx_matrix)
        self._val = np.matmul(cx_gate, self._val)
        return self
    
    def z(self, qubit):
        """
        Performs a Pauli Z gate on the target qubit.

        :param qubit: The target qubit.
        :return: The ket after the operation.
        """
        targeted_gate = correct_dimensionality(
            np.array([[1, 0],
                     [0, -1]]),
            qubit,
            self.num_qubits
        )
        self._val = np.matmul(targeted_gate, self._val)
        return self
    
    def y(self, qubit):
        """
        Performs a Pauli Y gate on the target qubit.

        :param qubit: The target qubit.
        :return: The ket after the operation.
        """
        targeted_gate = correct_dimensionality(
            np.array([[0, -1],
                     [1, 0]]),
            qubit,
            self.num_qubits
        )
        self._coefficient = self._coefficient * complex(0, 1)
        self._val = np.matmul(targeted_gate, self._val)
        return self
        
    def h(self, qubit):
        """
        Performs a Hadamard gate on the target qubit.

        :param qubit: The target qubit.
        :return: The two resulting kets.
        """
        targeted_gate = correct_dimensionality(
            np.array([[1, 1],
                     [1, -1]]),
            qubit,
            self.num_qubits
        )
        self._coefficient = self._coefficient / np.sqrt(2)
        self._val = np.matmul(targeted_gate, self._val)
        pos_vals, neg_vals = to_sum_of_basis_kets(self._val)

        res = [Ket(self._coefficient, pv) for pv in pos_vals] + [Ket(-self._coefficient, nv) for nv in neg_vals]
        return res

    def print(self):
        """
        Prints the state.
        """
        print(f"|{vector_to_bitstring(self._val)}>")
