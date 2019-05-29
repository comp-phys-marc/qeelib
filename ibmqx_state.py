import numpy as np
from IBMQuantumExperience import IBMQuantumExperience
from ket import ONE
from profiler import normalize_print_and_get_requirements

# API_TOKEN = 'a0f9090f4b9b0a7f86cb31848730654bb4dbc35aab364a7d728162c96b264752d413b88daea7303c87f12e0a719345119c0f8a880a27d73b998887664a989fce'
# API_TOKEN = 'c05e0105601b0c1d7e68e294844fdc5615b42f53b6d6a2bb5d6181206fcaec4753276e3bf4bb1eca8cf2bbf179f15b8ecee6df026b13fb8350df2172a6af23a5'
API_TOKEN = '033df3fead612eb383875727dfe1dbb6022cbd44e1a23410fec2db9f5d09b6e465cf4d7944cd98da84ca65e5b90e77db05d498b70c997989bae6f7d3827c09e9'

class IBMQXState:
    """
    A class that represents a quantum system being run on IBM's quantum computer platform.
    """

    def __init__(self, ket_list=[], num_qubits=1, symbol='q', qasm=None, device='ibmqx4', api=None):
        """
        Initializes a quantum state with the given parameters.

        :param ket_list: The kets are only used to print the initial state.
        :param num_qubits: The total number of qubits.
        :param symbol: The identifier for this quantum state.
        :param qasm: Predefined qasm provided to initialization.
        :param device: The IBM device to execute on.
        :raises: ValueError
        """

        for ket in ket_list:
            if ONE in ket.get_val():
                raise ValueError("IBMQX state only supports initialization to |00...0>")

        if num_qubits > 5 and (device in ['ibmqx4', 'ibmqx2']):
            raise ValueError("This device only supports 5 qubit states")

        if api:
            self.api = api
        else:
            self.api = None

        self.num_qubits = num_qubits
        self.symbol = symbol
        self.device = device

        if qasm is None:
            self.qasm = f'OPENQASM 2.0;include "qelib1.inc";qreg {self.symbol}[{num_qubits}];creg c[{num_qubits}];'
        else:
            self.qasm = qasm

        self.requirements = {
            'qubits': self.num_qubits,
            'gates': 0,
            'processor': device
        }

        print("Initializing IBMQX state:")
        self.print()

    @staticmethod
    def _test_api_auth_token():
        """
        Authentication with Quantum Experience Platform
        :return: IBMQX Credentials
        """
        api = IBMQuantumExperience(API_TOKEN)
        credential = api.check_credentials()

        return credential

    def _connect(self):
        """
        Attempt to connect to the Quantum Experience Platform
        :return:
        """
        connection_success = IBMQXState._test_api_auth_token()

        if connection_success:
            self.api = IBMQuantumExperience(API_TOKEN)
            print("IBMQX API auth success.")
        else:
            print("IBMQX API auth failure.")

    @normalize_print_and_get_requirements
    def execute(self, shots=1024):
        """
        Executes the QASM built by calls to this object.
        :param shots:  The number of times to run the experiment on IBM's backend.
        :return:
        """
        if not self.api:
            self._connect()
        results = self.api.run_job([{'qasm': self.qasm}], self.device, shots)
        return results

    @normalize_print_and_get_requirements
    def barrier(self, qubit=None):
        """
        Applies a barrier to the circuit to disable circuit optimization.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        if qubit:
            print("barrier ({0})".format(qubit), end='')
            self.qasm = self.qasm + f'\nbarrier {self.symbol}[{qubit}];'
        else:
            print("barrier ({0})".format(self.symbol), end='')
            self.qasm = self.qasm + f'\nbarrier {self.symbol};'
        return self

    @normalize_print_and_get_requirements
    def x(self, qubit):
        """
        Performs a Pauli X gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("x ({0})".format(qubit), end='')
        self.qasm = self.qasm + f'\nx {self.symbol}[{qubit}];'
        return self

    @normalize_print_and_get_requirements
    def y(self, qubit):
        """
        Performs a Pauli Y gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("y ({0})".format(qubit), end='')
        self.qasm = self.qasm + f'\ny {self.symbol}[{qubit}];'
        return self

    @normalize_print_and_get_requirements
    def z(self, qubit):
        """
        Performs a Pauli Z gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("z ({0})".format(qubit), end='')
        self.qasm = self.qasm + f'\nz {self.symbol}[{qubit}];'
        return self

    @normalize_print_and_get_requirements
    def u1(self, lamb, qubit):
        """
        A single parameter single qubit phase gate with zero duration:

        [[1,0],[0,exp(1i*lamb)]]

        :param lamb: The phase parameter.
        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("u1({1}) ({0})".format(qubit, lamb), end='')
        self.qasm = self.qasm + f'\nu1({lamb}) {self.symbol}[{qubit}];'
        return self

    @normalize_print_and_get_requirements
    def u3(self, theta, phi, lamb, qubit):
        """
        A three parameter single qubit gate:

        [[cos(theta/2),-exp(1i*lambda)*sin(theta/2)],[exp(1i*phi)*sin(theta/2),exp(1i*lambda+1i*phi)*cos(theta/2)]]

        :param theta: The first parameter.
        :param phi: The second parameter.
        :param lamb: The thrid parameter.
        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("u3({1}, {2}, {3}) ({0})".format(qubit, theta, phi, lamb), end='')
        self.qasm = self.qasm + f'\nu3({theta},{phi},{lamb}) {self.symbol}[{qubit}];'
        return self

    @normalize_print_and_get_requirements
    def s(self, qubit):
        """
        Performs an S phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("s ({0})".format(qubit), end='')
        self.qasm = self.qasm + f'\ns {self.symbol}[{qubit}];'
        return self

    @normalize_print_and_get_requirements
    def sdg(self, qubit):
        """
        Performs an S dagger phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("sdg ({0})".format(qubit), end='')
        self.qasm = self.qasm + f'\nsdg {self.symbol}[{qubit}];'
        return self

    @normalize_print_and_get_requirements
    def cx(self, source, target):
        """
        Performs a Controlled X gate on the target qubit with the
        source qubit as controller.

        :param source: The source qubit.
        :param source: The target qubit.
        :return: The full qasm after the opeation.
        """
        print("cx ({0} -> {1})".format(source, target), end='')
        self.qasm = self.qasm + f'\ncx {self.symbol}[{source}], {self.symbol}[{target}];'
        return self

    @normalize_print_and_get_requirements
    def h(self, qubit):
        """
        Performs a Hadamard gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("h ({0})".format(qubit), end='')
        self.qasm = self.qasm + f'\nh {self.symbol}[{qubit}];'
        return self

    @normalize_print_and_get_requirements
    def m(self, qubit):
        """
        Measures the target qubit.

        :param qubit: The target qubit.
        :return: The result of the measurement.
        """

        print("m ({0})".format(qubit), end='')
        self.qasm = self.qasm + f'\nmeasure {self.symbol}[{qubit}] -> c[{qubit}];'
        return self

    def print_state_vectors(self):
        pass

    def print_density_matrices(self):
        pass

    def normalize(self):
        pass

    def register_requirements(self):
        """
        Updates the resources required by the state.
        """
        self.requirements['gates'] += 1

    def print_requirements(self):
        """
        Prints the requirements for maintaining the current state of the quantum system.
        """
        self.print_max_requirements()

    def print_max_requirements(self):
        """
        Prints the requirements for the most expensive state/operation encountered by the class during runtime.
        """
        print(self.requirements)

    def tomography(self, qubit, phases, shots):
        """
        Replicates the current circuit and performs measurements in each of the three orthogonal axes of the Bloch
        sphere to determine the qubit's state.

        :return: The results from each circuit.
        """

        results = []

        self._connect()

        exp_vector = range(0, phases)
        for index in exp_vector:
            phase = 2 * np.pi * index / (len(exp_vector) - 1)
            index += 1

            # Measure X Axis
            x_state = IBMQXState(
                ket_list=[],
                num_qubits=self.num_qubits,
                symbol=self.symbol,
                qasm=self.qasm,
                device=self.device,
                api=self.api
            )

            x_state.u1(phase, qubit)

            x_state.h(qubit)
            x_state.m(qubit)

            # Measure Y Axis
            y_state = IBMQXState(
                ket_list=[],
                num_qubits=self.num_qubits,
                symbol=self.symbol,
                qasm=self.qasm,
                device=self.device,
                api=self.api
            )

            y_state.u1(phase, qubit)

            y_state.sdg(qubit)
            y_state.h(qubit)
            y_state.m(qubit)

            # Measure Z Axis
            z_state = IBMQXState(
                ket_list=[],
                num_qubits=self.num_qubits,
                symbol=self.symbol,
                qasm=self.qasm,
                device=self.device,
                api=self.api
            )

            z_state.u1(phase, qubit)

            z_state.m(qubit)

            results.append(x_state.execute(shots=shots))
            results.append(y_state.execute(shots=shots))
            results.append(z_state.execute(shots=shots))

        return results

    def print(self):
        """
        Prints the full qasm.
        """
        print("IBMQX QASM:")
        print(self.qasm)
