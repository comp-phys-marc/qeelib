from ..coefficient import Coefficient, ComplexCoefficient
from ..state import State
from ..superimposed_states import States
import math

def hadamard(first_state, second_state, qubit):
    first_coeff = Coefficient(magnitude=1.00, imaginary=False)
    first_state = State(coeff=first_coeff, val=first_state)
    
    second_coeff = Coefficient(magnitude=1.00, imaginary=False)
    second_state = State(coeff=second_coeff, val=second_state)
    
    state = States(state_array=[first_state, second_state], num_qubits=2)
    
    state.print()
    state.h(qubit)

hadamard("00", "01", 0)
