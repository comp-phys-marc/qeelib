import random
from math import sqrt
from .ket import Ket, ONE, ZERO
from .profiler import normalize_print_and_get_requirements


class State:
    """
    A class that represents a full quantum state and maintains a set of underlying kets.
    """
    
    def __init__(self, ket_list=[], num_qubits=1, symbol='Ψ'):
        """
        Initializes a quantum state with a given set of kets and number of qubits.

        :param ket_list: The kets.
        :param num_qubits: The total number of qubits.
        :param symbol: The identifier for this quantum state.
        """
        
        self.kets = []
        self.num_qubits = num_qubits
        self.symbol = symbol
        
        for ket in ket_list:
            self.add_ket(ket)

    def add_ket(self, ket):
        """
        Adds a ket to the overall quantum state.

        :param ket: The ket to add.
        :raises: ValueError
        """
        if isinstance(ket, Ket):
            if len(ket.get_val()) == self.num_qubits:
                self.kets.append(ket)
            else:
                raise ValueError("setting state with incorrect number of qubits {0} != {1} was attempted".format(len(ket.get_val()), self.num_qubits))
        else:
            raise ValueError("setting state of incorrect type was attempted")
        
    def remove_ket(self, ket):
        """
        Removes a ket from the overall quantum state.

        :param ket: The ket to remove.
        :raises: ValueError
        """
        self.kets.remove(ket)
        
    @normalize_print_and_get_requirements
    def x(self, qubit):
        """
        Performs a Pauli X gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        for ket in self.kets:
            ket.x(qubit)
        return self
         
    @normalize_print_and_get_requirements
    def cx(self, source, target):
        """
        Performs a Controlled X gate on the target qubit with the
        source qubit as controller.

        :param source: The source qubit.
        :param source: The target qubit.
        :return: The full quantum state after the opeation.
        """
        for ket in self.kets:
            ket.cx(source, target)
        return self
       
    @normalize_print_and_get_requirements
    def y(self, qubit):
        """
        Performs a Pauli Y gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        for ket in self.kets:
            ket.y(qubit)
        return self
            
    @normalize_print_and_get_requirements
    def z(self, qubit):
        """
        Performs a Pauli Z gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        for ket in self.kets:
            ket.z(qubit)
        return self
            
    @normalize_print_and_get_requirements
    def h(self, qubit):
        """
        Performs a Hadamard gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        new_kets = []
        for ket in self.kets:
            hadamard_result = ket.h(qubit)
            new_kets.extend(hadamard_result)
        self.kets = new_kets
        return self
    
    @normalize_print_and_get_requirements
    def m(self, qubit):
        """
        Measures the target qubit.

        :param qubit: The target qubit.
        :return: The result of the measurement.
        """
        one_kets = []
        zero_kets = []
        
        for ket in self.kets:
            if (self._val.index(1) // (2 ** (qubit - 1))) % 2 != 0:
                one_kets.append(ket)
                beta = ket.get_coefficient()
            else:
                zero_kets.append(ket)
                alpha = ket.get_coefficient()
        
        result = self._measure(abs(alpha) ** 2, abs(beta) ** 2)

        if result == ONE:
            self.kets = one_kets
        elif result == ZERO:
            self.kets = zero_kets

        return result
    
    def normalize(self):
        """
        Normalizes the current quantum state.

        :return: Returns the full normalized quantum state.
        """
        total_probability = 0
        unique_kets = []
        for ket in self.kets:
            already_found = False
            for unique_ket in unique_kets:
                if ket.get_val() == unique_ket.get_val():
                    already_found = True 
                    unique_ket.set_coefficent(unique_ket.get_coefficient() + ket.get_coefficient())
            if not already_found:
                unique_kets.append(ket)
        for unique_ket in unique_kets:
            total_probability += unique_ket.get_probability()
        norm_factor = 1 / sqrt(total_probability)
        if total_probability != 1:
            for unique_ket in unique_kets:
                unique_ket.set_coefficent(unique_ket.get_coefficient() * norm_factor)
        self.kets = unique_kets

        return self
                
    def _measure(self, alpha, beta):
        """
        Used pseudo-random number generation to simulate the probabilistic outcome of a qubit
        measurement. Update the quantum system with the measurement results.

        :param alpha: The first component of the qubit's state vector being measured.
        :param beta: The second component of the qubit's state vector being measured.
        :return: The result of the measurement in the computational basis.
        """
        cutoff = int(alpha * 100)
        outcome = random.randint(0, 100)
        if outcome < cutoff:
            return ZERO
        else:
            return ONE
        
    def print(self):
        """
        Prints the full quantum state.
        """
        print("|{0}> =".format(self.symbol), end='')
        for ket in self.kets:
            ket.print()
        print("\n")
