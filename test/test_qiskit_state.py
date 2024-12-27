import unittest

from ..qiskit_state import QiskitState
from ..ket import Ket

IBM_TOKEN='dbff2dd49706089bda14404d9f0ee4476e66071a8139163266477d4342c410536067e437fe1150d475dcf96d392034765f3aa155818b9afd90eb8b869bbf83c6'


class QiskitTests(unittest.TestCase):

    def test_qiskit(self):
        print("Testing QiskitState...")

        try:
            initial_coeff = complex(1, 0)
            initial_state = Ket(coeff=initial_coeff, val="00000")
            state = QiskitState(ket_list=[initial_state], num_qubits=5, api_token=IBM_TOKEN)

            state.x(0).x(2).x(4)  # TODO: automate this initialization in the IBMQXState class?

            state.cx(source=1, target=3) \
                .cx(source=2, target=4)

            print(state.execute())

        except Exception as e:
            self.fail(f'Raised exception {e}')
