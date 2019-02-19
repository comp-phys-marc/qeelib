from functools import wraps, partial
import random
import copy
from math import sqrt
from ket import Ket, ONE, ZERO
from coefficient import Coefficient


def normalize_print_and_get_requirements(func):
    """
    Provides automatic normalization, operation result printing
    and requirement registration between state mutations.

    :param func: A method intended to mutate the quantum state.
    :return: The wrapped method with normalization, printing and requirements registration added.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        pfunc = partial(func, *args, **kwargs)
        result = pfunc()
        states = args[0]
        states.normalize()
        states.register_requirements()
        states.print()
        return result
    return wrapper


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
    
    def get_components(self, qubit):
        """
        Determines the components of the state vector for the given target qubit.

        :param qubit: The target qubit.
        :return: the state vector as a list.
        """
        alpha = Coefficient()
        beta = Coefficient()
        for ket in self.kets:
            if ket.get_val()[qubit] == ONE:
                beta = beta.add(ket.get_coefficient())
            elif ket.get_val()[qubit] == ZERO:
                alpha = alpha.add(ket.get_coefficient())
        return [alpha, beta]
        
    @normalize_print_and_get_requirements
    def x(self, qubit):
        """
        Performs a Pauli X gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        for ket in self.kets:
            print("x ({0})".format(qubit), end='')
            ket.print()
            print(" =", end='')
            ket.x(qubit)
            ket.print()
            print("\n")
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
            print("cx ({0} -> {1})".format(source, target), end='')
            ket.print()
            print(" =", end='')
            ket.cx(source, target)
            ket.print()
            print("\n")
        return self
       
    @normalize_print_and_get_requirements
    def y(self, qubit):
        """
        Performs a Pauli Y gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        for ket in self.kets:
            print("y ({0})".format(qubit), end='')
            ket.print()
            print(" =", end='')
            ket.y(qubit)
            ket.print()
            print("\n")
        return self
            
    @normalize_print_and_get_requirements
    def z(self, qubit):
        """
        Performs a Pauli Z gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        for ket in self.kets:
            print("z ({0})".format(qubit), end='')
            ket.print()
            print(" =", end='')
            ket.z(qubit)
            ket.print()
            print("\n")
        return self
            
    @normalize_print_and_get_requirements
    def h(self, qubit):
        """
        Performs a Hadamard gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full quantum state after the operation.
        """
        
        alpha = Coefficient(magnitude=0.00, imaginary=False)
        beta = Coefficient(magnitude=0.00, imaginary=False)
        one_kets = []
        zero_kets = []
        
        for ket in self.kets:
            if ket.get_val()[qubit] == ONE:
                one_kets.append(ket)
                beta = beta.add(ket.get_coefficient())
            elif ket.get_val()[qubit] == ZERO:
                zero_kets.append(ket)
                alpha = alpha.add(ket.get_coefficient())
        
        negative_beta = copy.deepcopy(beta)
        negative_beta.negate_magnitude()
        if alpha.equals(beta):
            print("h ({0})".format(qubit), end='')
            for ket in self.kets:
                ket.print()
            print(" =", end='')
            self.kets = zero_kets
            for ket in self.kets:
                ket.print()
            print("\n")
        elif alpha.equals(negative_beta):
            print("h ({0})".format(qubit), end='')
            for ket in self.kets:
                ket.print()
            print(" =", end='')
            self.kets = one_kets
            for ket in self.kets:
                ket.print()
            print("\n")
        else:
            new_kets = []
            for ket in self.kets:
                print("h ({0})".format(qubit), end='')
                ket.print()
                hadamard_result = ket.h(qubit)
                new_kets.extend(hadamard_result)
                print(" =", end='')
                hadamard_result[0].print()
                hadamard_result[1].print()
                print("\n")
            self.kets = new_kets
        return self
    
    @normalize_print_and_get_requirements
    def m(self, qubit):
        """
        Measures the target qubit.

        :param qubit: The target qubit.
        :return: The result of the measurement.
        """
        alpha = Coefficient()
        beta = Coefficient()
        one_kets = []
        zero_kets = []
        
        for ket in self.kets:
            if ket.get_val()[qubit] == ONE:
                one_kets.append(ket)
                beta = beta.add(ket.get_coefficient())
            elif ket.get_val()[qubit] == ZERO:
                zero_kets.append(ket)
                alpha = alpha.add(ket.get_coefficient())
        
        result = self._measure(alpha.to_probability(), beta.to_probability())
        
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
                    unique_ket.get_coefficient().add(ket.get_coefficient())
            if not already_found:
                unique_kets.append(ket)
        for unique_ket in unique_kets:
            total_probability += unique_ket.get_probability()
        norm_factor = 1/sqrt(total_probability)
        if total_probability != 1:
            for unique_ket in unique_kets:
                unique_ket.get_coefficient().multiply_by_number(norm_factor)
        self.kets = unique_kets
        print("normalizing factor: {0}\n".format(norm_factor))
        return self
                
    def _measure(self, alpha, beta):
        """
        Used pseudo-random number generation to simulate the probabilistic outcome of a qubit
        measurement. Update the quantum system with the measurement results.

        :param alpha: The first component of the qubit's state vector being measured.
        :param beta: The second component of the qubit's state vector being measured.
        :return: The result of the measurement in the computational basis.
        """
        cutoff = int(alpha*100)
        outcome = random.randint(0, 100)
        if outcome < cutoff:
            return ZERO
        else:
            return ONE
        
    def print(self):
        """
        Prints teh full quantum state.
        """
        print("|{0}> =".format(self.symbol), end='')
        for ket in self.kets:
            ket.print()
        print("\n")
        
    def register_requirements(self):
        """
        Checks if the current state of the quantum system is the most expensive yet seen during runtime.
        If it is the most expensive state, updates the resource requirements.
        """
        return
        
    def print_requirements(self):
        """
        Prints the requirements for maintaining the current state of the quantum system.
        """
        num_states = len(self.kets)
        print("TODO")
        
    def print_max_requirements(self):
        """
        Prints the requirements for the most expensive state/operation encountered by the class during runtime.
        """
        print("TODO")
    
    def get_density_matrix(self, qubit):
        """
        Determines the density matrix representations of the target qubit.

        :param qubit: The target qubit.
        :return: The density matrix as a two dimensional list.
        """
            
        [alpha, beta] = self.get_components(qubit)
        if isinstance(beta, Coefficient) and isinstance(alpha, Coefficient):
            
            entry00 = abs(alpha.get_magnitude())**2
            entry00 = str(round(entry00, 3))
            
            beta_conjugate = copy.deepcopy(beta)
            beta_conjugate.complex_conjugate()
    
            entry01 = alpha.get_magnitude()*beta_conjugate.get_magnitude()
            if alpha.get_imaginary() == True and beta_conjugate.get_imaginary() == True:
                entry01 = - entry01
            elif alpha.get_imaginary() == True or beta_conjugate.get_imaginary() == True:
                entry01 = str(entry01) + 'i'
            entry01 = str(round(entry01, 3))
            
            alpha_conjugate = copy.deepcopy(alpha)
            alpha_conjugate.complex_conjugate()
            
            entry10 = alpha_conjugate.get_magnitude()*beta.get_magnitude()
            if alpha_conjugate.get_imaginary() == True and beta.get_imaginary() == True:
                entry10 = - entry10
            elif alpha_conjugate.get_imaginary() == True or beta.get_imaginary() == True:
                entry10 = str(entry10) + 'i'
            entry10 = str(round(entry10, 3))
            
            entry11 = abs(beta.get_magnitude())**2
            entry11 = str(round(entry11, 3))
            
            return [[entry00, entry01], [entry10, entry11]]
    
    def print_density_matrices(self):
        """
        Prints the density matrices of each qubit.
        """
        
        for qubit in range(self.num_qubits):
            print("qubit {0} density matrix:\n".format(qubit))
            
            matrix = self.get_density_matrix(qubit)
            print(" _         _")
            print("|{:5s} {:>5s}|\n|{:5s} {:>5s}|\n".format(matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]), end='')
            print(" -         -")     
        return
