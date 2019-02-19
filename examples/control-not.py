from ..coefficient import Coefficient
from ..state import Ket
from ..state import State

def control_not():
    initial_coeff = Coefficient(magnitude=1.00, imaginary=False)
    initial_state = Ket(coeff=initial_coeff, val="101010010110")
    state = State(ket_list=[initial_state], num_qubits=12)

    state.cx(source=0, target=11)\
    .cx(source=11, target=8)\
    .cx(source=8, target=1)\
    .cx(source=1, target=3)\
    .cx(source=3, target=5)\
    .cx(source=5, target=6)

control_not()
