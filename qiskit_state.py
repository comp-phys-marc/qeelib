from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import Sampler
from qiskit_ibm_runtime import QiskitRuntimeService
from .profiler import normalize_print_and_get_requirements


class QiskitState:
    """
    A class that represents a Qiskit quantum state.
    """

    def __init__(self, ket_list=[], num_qubits=1, symbol='q', device='default', api=None, api_token=None):
        """
        Initializes a quantum state with a given number of qubits.

        :param ket_list: The kets are only used to print the initial state.
        :param num_qubits: The total number of qubits.
        :param symbol: The identifier for this quantum state.
        :param device: The IBM device to execute on.
        :param api: A pre-initialized api.
        :param api_token: The IBMQX access token for the user.
        :raises: ValueError
        """

        self.state = QuantumRegister(num_qubits)
        cr = ClassicalRegister(num_qubits)
        self.circuit = QuantumCircuit(self.state, cr)

        self.num_qubits = num_qubits
        self.symbol = symbol
        self.device = device

        if api_token:
            self.api_token = api_token
        if api:
            self.api = api
        else:
            self.api = None

            if not api_token:
                raise ValueError("Either an initialized api or api token is required")

        self.requirements = {
            'qubits': self.num_qubits,
            'gates': 0,
            'processor': device
        }

        if self.api is None:
            self._connect()

        print("Initializing Qiskit state:")
        self.print()

    @normalize_print_and_get_requirements
    def x(self, qubit):
        """
        Performs a Pauli X gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("x ({0})".format(qubit))
        self.circuit.x(self.state[qubit])
        self.register_requirements()
        return self

    @normalize_print_and_get_requirements
    def y(self, qubit):
        """
        Performs a Pauli Y gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("y ({0})".format(qubit))
        self.circuit.y(self.state[qubit])
        self.register_requirements()
        return self

    @normalize_print_and_get_requirements
    def z(self, qubit):
        """
        Performs a Pauli Z gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("z ({0})".format(qubit))
        self.circuit.z(self.state[qubit])
        self.register_requirements()
        return self

    @normalize_print_and_get_requirements
    def s(self, qubit):
        """
        Performs an S phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("s ({0})".format(qubit))
        self.circuit.s(self.state[qubit])
        self.register_requirements()
        return self

    @normalize_print_and_get_requirements
    def sdg(self, qubit):
        """
        Performs an S dagger phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("sdg ({0})".format(qubit))
        self.circuit.sdg(self.state[qubit])
        self.register_requirements()
        return self

    @normalize_print_and_get_requirements
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
        self.register_requirements()
        return self

    @normalize_print_and_get_requirements
    def h(self, qubit):
        """
        Performs a Hadamard gate on the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("h ({0})".format(qubit))
        self.circuit.h(self.state[qubit])
        self.register_requirements()
        return self

    @normalize_print_and_get_requirements
    def m(self, qubit):
        """
        Measures the target qubit.

        :param qubit: The target qubit.
        :return: self
        """
        print("m ({0})".format(qubit))
        self.circuit.measure(self.state[qubit], qubit)
        self.register_requirements()
        return self

    def execute(self):
        service = QiskitRuntimeService(channel="ibm_quantum")

        if self.device == 'default':
            # get the least busy operational quantum hardware backend
            backend = service.least_busy(operational=True, simulator=False)
            target = backend.target
        else:
            backend = service.backends(self.device)
            target = backend.target

        # transpile the circuit for the backend
        pass_manager = generate_preset_pass_manager(target=target, optimization_level=3)
        isa_circuit = pass_manager.run(self.circuit)

        # run the circuit
        sampler = Sampler(session=backend)
        job = sampler.run([isa_circuit])
        job_result = job.result()

        # return the measurement outcomes
        return job_result

    def _connect(self):
        """
        Attempt to connect to the IBM Quantum Platform.
        :return:
        """
        QiskitRuntimeService.save_account(channel="ibm_quantum", token=self.api_token, overwrite=True)

    def register_requirements(self):
        """
        Updates the resources required by the state.
        """
        self.requirements['gates'] += 1

    def print_requirements(self):
        """
        Prints the requirements for maintaining the current state of the quantum system.
        """
        print()
        self.print_max_requirements()

    def print_max_requirements(self):
        """
        Prints the requirements for the most expensive state/operation encountered by the class during runtime.
        """
        print(self.requirements)

    def print_state_vectors(self):
        pass

    def normalize(self):
        pass

    def print(self):
        """
        Prints the full quantum circuit.
        """
        print(self.circuit)
