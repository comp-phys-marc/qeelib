import unittest

from ..qiskit_state import QiskitState
from ..ket import Ket


class QiskitTests(unittest.TestCase):

    def test_qiskit(self):
        print("Testing QiskitState...")
        try:
            initial_coeff = complex(1, 0)
            initial_state = Ket(coeff=initial_coeff, val="00000")
            state = QiskitState(ket_list=[initial_state], num_qubits=5)

            state.x(0).x(2).x(4)  # TODO: automate this initialization in the IBMQXState class?

            state.cx(source=1, target=3) \
                .cx(source=2, target=4)

            print(state.execute())

        except Exception as e:
            self.fail(f'Raised exception {e}')
