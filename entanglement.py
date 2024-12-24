import copy
from .ket import Ket, ONE


class EntangledKet(Ket):

    def __init__(self, coeff=None, val=None, entanglements=[]):

        super().__init__(coeff, val)
        self._entanglements = entanglements

    def is_entangled_with(self, system, qubit):
        """
        Determines whether the existence of the ket is predicated upon
        entanglement interaction of the given qubit.

        :param system: The subsystem of the entangled qubit.
        :param qubit: the entangled qubit.
        :return: Whether the entanglement of the qubit effects the existence of the ket.
        """
        is_entangled = False
        for entanglement in self._entanglements:
            if entanglement.get_system() == system and entanglement.get_qubit() == qubit:
                is_entangled = True

        return is_entangled

    def entangle(self, outcome, system, qubit):
        """
        Registers the ket's dependence on an entanglement of qubits.
        """
        self._entanglements.append(Entanglement(outcome, system, qubit))

    def should_collapse(self, outcome, system, qubit):
        """
        Determines whether the ket should collapse and disappear following
        a measurement of the given qubit.

        :param outcome: The measurement outcome.
        :param system: The subsystem owning the measured qubit.
        :param qubit: The measured qubit.
        :return: Whether the ket should disappear.
        """
        for entanglement in self._entanglements:
            if entanglement.get_system() == system and entanglement.get_qubit() == qubit:
                self._entanglements.remove(entanglement)
                if entanglement.get_outcome() == outcome:
                    return False
                else:
                    return True

    def copy_entanglement_to(self, other_ket):
        """
        Copies the entanglement reference to another ket. This is to be
        used when operating on a ket which will disappear when an entangled
        qubit is measured such that a new ket is created.

        :param other_ket: The ket to copy entanglement to.
        """
        for entanglement in self._entanglements:
            other_ket.entangle(entanglement.get_outcome(), entanglement.get_system(), entanglement.get_qubit())

    def h(self, qubit):
        """
        Performs a Hadamard gate on the target qubit and propagates entanglements.

        :param qubit: The target qubit.
        :return: The two resulting kets.
        """
        new_coeff = copy.deepcopy(self.coefficient)
        new_val = copy.deepcopy(self.val)
        new_state = EntangledKet(new_coeff, new_val)
        new_state.x(qubit)
        self.copy_entanglement_to(new_state)

        if self.val[qubit] == ONE:
            self.coefficient.negate_magnitude()

        return [self, new_state]


class Entanglement:
    """
    Tracks entanglement across quantum state subsystems.
    """

    def __init__(self, outcome=0, system=None, qubit=None):
        """
        Initializes an entanglement object.

        :param outcome: The measurement outcome for which a ket will not disappear.
        :param system: The system owning a qubit which is entangled.
        :param qubit: The qubit that is entangled.
        """
        self._outcome = outcome
        self._system = system
        self._qubit = qubit

    def get_system(self):
        """
        Gets the system owning the entangled qubit.

        :return: The name of the system owning the entangled qubit.
        """
        return self._system

    def get_qubit(self):
        """
        Gets the qubit which is entangled.

        :return: The index of the entangled qubit.
        """
        return self._qubit

    def get_outcome(self):
        """
        Gets the outcome for which the ket will not disappear.

        :return: The outcome for which the ket will not disappear.
        """
        return self._outcome
