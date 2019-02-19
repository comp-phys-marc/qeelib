import copy
from coefficient import Coefficient, ComplexCoefficient

ZERO = "0"
ONE = "1"


class Ket:
    
    def __init__(self, coeff=None, val=None):
        """
        Initializes a ket with a value and coefficient.

        :param coeff: The ket's coefficient.
        :param val: The qubit string value.
        """
        self.set_coefficient(coeff)
        self.set_val(val)
        
    def __eq__(self, other):
        """
        The equality of kets compares their qubit strings, not their coefficients.

        :param other: Another ket.
        :return: Whether they are the same ket.
        """
        if isinstance(other, Ket):
            return self.val == other.get_val()
        return False
        
    def get_val(self):
        """
        The qubit string value of the ket.

        :return: The qubit string.
        """
        return self.val
    
    def get_coefficient(self):
        """
        Returns the coefficient of the ket.

        :return: The ket's coefficient.
        """
        return self.coefficient
        
    def set_val(self, val):
        """
        Sets the qubit string value for the ket.

        :param val:
        :return:
        """
        if isinstance(val, str):
            self.val = val
            for qubit in val:
                if not (qubit in [ZERO, ONE]):
                    self.val = None
                    raise ValueError("state value {0} is not entirely 1's and 0's".format(val))
                    
    def set_coefficient(self, coeff):
        """
        Sets the coefficient of the ket's term in the overall quantum state.

        :param coeff: The coefficient of the ket.
        :raises: ValueError
        """
        if isinstance(coeff, Coefficient) or isinstance(coeff, ComplexCoefficient):
            self.coefficient = coeff
        else:
            raise ValueError("setting coefficient of incorrect type was attempted")
            
    def get_probability(self):
        """
        Determines the probabilistic weight of the ket within
        its overall quantum state.

        :return: The probabilistic weight of the ket.
        """
        return self.coefficient.to_probability()
        
    def x(self, qubit):
        """
        Performs a Pauli X gate on the target qubit.

        :param qubit: The target qubit.
        :return: The ket after the operation.
        """
        self.val = self.val[0:qubit] + str(int(not int(self.val[qubit]))) + self.val[qubit+1:]
        return self
    
    def cx(self, source, target):
        """
        Performs a Controlled X gate on the target qubit with the
        source qubit as controller.

        :param source: The source qubit.
        :param target: The target qubit.
        :return: The ket after the operation.
        """
        new_target = str(int(not int(self.val[target]))) if self.val[source] == ONE else self.val[target]
        self.val = self.val[0:target] + new_target + self.val[target+1:]
        return self
    
    def z(self, qubit):
        """
        Performs a Pauli Z gate on the target qubit.

        :param qubit: The target qubit.
        :return: The ket after the operation.
        """
        if int(self.val[qubit]) == 1:
            self.coefficient.negate_magnitude()
        return self
    
    def y(self, qubit):
        """
        Performs a Pauli Y gate on the target qubit.

        :param qubit: The target qubit.
        :return: The ket after the operation.
        """
        self.z(qubit)
        self.x(qubit)
        self.coefficient.multiply_by_i()
        return self
        
    def h(self, qubit):
        """
        Performs a Hadamard gate on the target qubit.

        :param qubit: The target qubit.
        :return: The two resulting kets.
        """
        new_coeff = copy.deepcopy(self.coefficient)
        new_val = copy.deepcopy(self.val)
        new_state = Ket(new_coeff, new_val)
        new_state.x(qubit)
        
        if self.val[qubit] == ONE:
            self.coefficient.negate_magnitude()
            
        return [self, new_state]
        
    def print(self):
        """
        Prints the state.
        """
        self.coefficient.print()
        print("|{0}>".format(self.val), end='')
