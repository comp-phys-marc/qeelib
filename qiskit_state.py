from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime import QiskitRuntimeService
import numpy as np


class QiskitState:
    """
    A class that represents a Qiskit quantum state.
    """

    def __init__(self, ket_list=[], num_qubits=1, symbol='Ψ'):
        """
        Initializes a quantum state with a given number of qubits.

        :param ket_list: The kets are only used to print the initial state.
        :param num_qubits: The total number of qubits.
        :param symbol: The identifier for this quantum state.
        :raises: ValueError
        """

        self.state = QuantumRegister(num_qubits)
        cr = ClassicalRegister(num_qubits)
        self.circuit = QuantumCircuit(self.state, cr)

        self.num_qubits = num_qubits
        self.symbol = symbol

        self.requirements = {
            'floats': self.state.size(),
            'flops': 0
        }

        print("Initializing Qiskit state:")
        self.print()

    def x(self, qubit):
        """
        Performs a Pauli X gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("x ({0})".format(qubit))
        self.circuit.x(self.state[qubit])
        return self

    def y(self, qubit):
        """
        Performs a Pauli Y gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("y ({0})".format(qubit))
        self.circuit.y(self.state[qubit])
        return self

    def z(self, qubit):
        """
        Performs a Pauli Z gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("z ({0})".format(qubit))
        self.circuit.z(self.state[qubit])
        return self

    def s(self, qubit):
        """
        Performs an S phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("s ({0})".format(qubit))
        self.circuit.s(self.state[qubit])
        return self

    def sdg(self, qubit):
        """
        Performs an S dagger phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("sdg ({0})".format(qubit))
        self.circuit.sdg(self.state[qubit])
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
        self.circuit.cnot(self.state[source], self.state[target])
        return self

    def h(self, qubit):
        """
        Performs a Hadamard gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("h ({0})".format(qubit))
        self.circuit.h(self.state[qubit])
        return self

    def m(self, qubit):
        """
        Measures the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("m ({0})".format(qubit))
        self.circuit.measure(self.state[qubit], qubit)
        return self

    def execute(self):
        #TODO: support different backend executions

        service = QiskitRuntimeService(channel="ibm_quantum")

        # get the least busy operational quantum hardware backend
        backend = service.least_busy(operational=True, simulator=False)
        target = backend.target

        # transpile the circuit for the backend
        pass_manager = generate_preset_pass_manager(target=target, optimization_level=3)
        isa_circuit = pass_manager.run(self.circuit)

        # run the circuit
        sampler = Sampler(mode=backend)
        job = sampler.run([isa_circuit])
        job_result = job.result()

        # return the measurement outcomes
        return job_result

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
