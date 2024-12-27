from ..ket import Ket
from ..state import State

API_TOKEN = ''


def control_not():
    initial_coeff = complex(1, 0)
    initial_state = Ket(coeff=initial_coeff, val="101010010110")
    state = State(ket_list=[initial_state], num_qubits=12)

    state.cx(source=0, target=11)\
    .cx(source=11, target=8)\
    .cx(source=8, target=1)\
    .cx(source=1, target=3)\
    .cx(source=3, target=5)\
    .cx(source=5, target=6)


if __name__ == '__main__':
    control_not()
