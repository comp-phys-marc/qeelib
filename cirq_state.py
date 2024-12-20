import cirq
import numpy as np


class CirqState:
    """
    A class that represents a Cirq quantum state.
    """

    def __init__(self, ket_list=[], num_qubits=1, symbol='Ψ'):
        """
        Initializes a quantum state with a given number of qubits.

        :param ket_list: The kets are only used to print the initial state.
        :param num_qubits: The total number of qubits.
        :param symbol: The identifier for this quantum state.
        :raises: ValueError
        """

        self.circuit = cirq.Circuit()
        self.state = cirq.LineQubit.range(num_qubits)
        self.num_qubits = num_qubits
        self.symbol = symbol

        self.requirements = {
            'floats': self.state.size(),
            'flops': 0
        }

        print("Initializing Cirq state:")
        self.print()

    def x(self, qubit):
        """
        Performs a Pauli X gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("x ({0})".format(qubit))
        self.circuit.append(cirq.X(self.state[qubit]))
        return self

    def y(self, qubit):
        """
        Performs a Pauli Y gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("y ({0})".format(qubit))
        self.circuit.append(cirq.Y(self.state[qubit]))
        return self

    def z(self, qubit):
        """
        Performs a Pauli Z gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("z ({0})".format(qubit))
        self.circuit.append(cirq.Z(self.state[qubit]))
        return self

    def s(self, qubit):
        """
        Performs an S phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("s ({0})".format(qubit))
        self.circuit.append(cirq.S(self.state[qubit]))
        return self

    def sdg(self, qubit):
        """
        Performs an S dagger phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("sdg ({0})".format(qubit))

        class Sdg(cirq.Gate):
            def __init__(self):
                super(Sdg, self)
            def _num_qubits_(self):
                return 1
            def _unitary_(self):
                return np.array([
                    [1.0, 0.0],
                    [0.0, -complex(0, 1)]
                ])
            def _circuit_diagram_info_(self, args):
                return "Sdg"

        sdg_gate = Sdg()
        self.circuit.append(sdg_gate.on(self.state[qubit]))

        return self

    def cx(self, source, target):
        """
        Performs a Controlled X gate on the target qubit with the
        source qubit as controller.

        :param source: The source qubit.
        :param source: The target qubit.
        :return: self
        """
        print("cx ({0} -> {1})".format(source, target))
        self.circuit.append(cirq.CNOT(self.state[source], self.state[target]))
        return self

    def h(self, qubit):
        """
        Performs a Hadamard gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("h ({0})".format(qubit))
        self.circuit.append(cirq.H(self.state[qubit]))
        return self

    def m(self, qubit):
        """
        Measures the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("m ({0})".format(qubit))
        self.circuit.append(cirq.M(self.state[qubit]))
        return self

    def execute(self):
        #TODO: support different backend executions
        simulator = cirq.Simulator()
        result = simulator.run(self.circuit)

        print(result)

    def register_requirements(self):
        pass

    def print_requirements(self):
        pass

    def print_max_requirements(self):
        pass

    def print_state_vectors(self):
        pass

    def normalize(self):
        pass

    def print(self):
        """
        Prints the full quantum circuit.
        """
        print(self.circuit)
