from coefficient import Coefficient
from ket import Ket
from state import State


def hadamard(first_state, second_state, qubit):
    first_coeff = Coefficient(magnitude=1.00, imaginary=False)
    first_state = Ket(coeff=first_coeff, val=first_state)
    
    second_coeff = Coefficient(magnitude=1.00, imaginary=False)
    second_state = Ket(coeff=second_coeff, val=second_state)
    
    state = State(ket_list=[first_state, second_state], num_qubits=2)
    
    state.print()
    state.h(qubit)

hadamard("00", "01", 0)
