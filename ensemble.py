import copy
from .state import State, ONE, ZERO
from .superimposed_states import States


class Ensemble:

    def __init__(self, sub_systems={}):
        self.subsystems = sub_systems

    def add_subsystem(self, states, name):

        if isinstance(states, States):
            self.subsystems[name] = states
        else:
            raise ValueError('Attempting to a non superimposed state object to ensemble.')

    def cx(self, source_system, source_qubit, target_system, target_qubit):

        alpha_source = None
        beta_source = None

        if source_system == target_system:
            self.subsystems[source_system].cx(source_qubit, target_qubit)
        else:
            [alpha_source, beta_source] = self.subsystems[source_system].get_components(source_qubit)

        target_states = copy.deepcopy(self.subsystems[target_system].states)

        print("q: ", end='')
        self.subsystems[source_system].print()

        for state in target_states:
            print("cx ({0}[{1}] -> {2}[{3}])".format(source_system, source_qubit, target_system, target_qubit), end='')
            state.print()
            print(" =", end='')

            new_coeff = copy.deepcopy(state.get_coefficient())
            new_val = copy.deepcopy(state.get_val())
            new_state = State(new_coeff, new_val)
            new_state.x(target_qubit)

            new_state.set_coefficient(new_state.coefficient.multiply(alpha_source))
            state.set_coefficient(state.coefficient.multiply(beta_source))

            self.subsystems[target_system].add_state(new_state)

            state.print()
            print("\n")

            self.subsystems[target_system].print()

        return self.subsystems[target_system]

    def print_density_matrices(self):
        for subsystem in self.subsystems:
            print("|{0}> matrices:".format(subsystem.symbol))
            subsystem.print_density_matrices()

    def print_max_requirements(self):
        for subsystem in self.subsystems:
            print("|{0}> requirements:".format(subsystem.symbol))
            subsystem.print_max_requirements()
