import copy
from .entanglement import EntangledKet
from .state import State


class Ensemble:
    """
    Maintains a set of interacting quantum systems.
    """

    def __init__(self, sub_systems={}):
        """
        Initializes an ensemble of quantum systems.

        :param sub_systems: The subsystems' states indexed by name.
        """
        self.subsystems = sub_systems

    def add_subsystem(self, state, name):
        """
        Adds a subsystem to the ensemble.

        :param states: The new subsystem's state.
        :param name: The name of the new subsystem.
        :raises: ValueError
        """

        if isinstance(state, State):
            self.subsystems[name] = state
        else:
            raise ValueError('Attempting to add non state object to ensemble.')

    def m(self, target_system, target_qubit):
        """
        Measures a qubit and collapses quantum state across subsystems accordingly.

        :param target_system: The system owning the qubit to be measured.
        :param target_qubit: The qubit to be measured.
        :return: The outcome of the measurement.
        """
        outcome = self.subsystems[target_system].m(target_qubit)

        for subsystem in self.subsystems:
            for entangled_ket in self.subsystems[subsystem].kets:
                if isinstance(entangled_ket, EntangledKet) \
                        and entangled_ket.is_entangled_with(target_system, target_qubit):
                    collapse = entangled_ket.should_collapse(outcome, target_system, target_qubit)

                    if collapse:
                        self.subsystems[subsystem].remove_ket(entangled_ket)

        return outcome

    def cx(self, source_system, source_qubit, target_system, target_qubit):
        """
        Applies a Controlled X gate within or between subsystems.

        :param source_system: The system owning the controlling qubit.
        :param source_qubit: The controlling qubit.
        :param target_system: The system owning the target qubit.
        :param target_qubit: The target qubit.
        :return:
        """
        alpha_source = None
        beta_source = None

        if source_system == target_system:
            self.subsystems[source_system].cx(source_qubit, target_qubit)
        else:
            [alpha_source, beta_source] = self.subsystems[source_system].get_components(source_qubit)

        target_kets = copy.deepcopy(self.subsystems[target_system].kets)

        print("q: ", end='')
        self.subsystems[source_system].print()

        for ket in target_kets:
            print("cx ({0}[{1}] -> {2}[{3}])".format(source_system, source_qubit, target_system, target_qubit), end='')
            ket.print()
            print(" =", end='')

            new_coeff = copy.deepcopy(ket.get_coefficient())
            new_val = copy.deepcopy(ket.get_val())
            new_ket = EntangledKet(new_coeff, new_val)
            new_ket.x(target_qubit)

            new_ket.set_coefficient(new_ket.coefficient.multiply(alpha_source))
            ket.set_coefficient(ket.coefficient.multiply(beta_source))

            new_ket.entangle(outcome=0, system=source_system, qubit=source_qubit)

            self.subsystems[target_system].add_ket(new_ket)

            if not isinstance(ket, EntangledKet):
                entangled_ket = EntangledKet(new_coeff, new_val)
                entangled_ket.entangle(outcome=1, system=source_system, qubit=source_qubit)

                self.subsystems[target_system].remove_ket(ket)
                self.subsystems[target_system].add_ket(entangled_ket)
                ket = entangled_ket
            else:
                ket.entangle(outcome=1, system=source_system, qubit=source_qubit)

            ket.print()
            print("\n")

            self.subsystems[target_system].print()

        return self.subsystems[target_system]

    def print_density_matrices(self):
        """
        Prints the density matrix representations of each qubit in each subsystem.
        """
        for symbol in self.subsystems:
            print("|{0}> matrices:".format(symbol))
            self.subsystems[symbol].print_density_matrices()

    def print_max_requirements(self):
        """
        Prints the requirements for the most expensive state/operation encountered in the ensemble during runtime.
        """
        for symbol in self.subsystems:
            print("|{0}> requirements:".format(symbol))
            self.subsystems[symbol].print_max_requirements()
