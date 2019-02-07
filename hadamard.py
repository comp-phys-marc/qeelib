from coefficient import Coefficient, ComplexCoefficient
from state import State
from superimposed_states import States
import math

def hadamard(first_state, second_state, qubit):
    first_coeff = Coefficient(magnitude=math.sqrt(0.25), imaginary=True)
    first_state = State(coeff=first_coeff, val=first_state)
    
    second_real_coeff = Coefficient(magnitude=math.sqrt(0.75), imaginary=False)
    second_im_coeff = Coefficient(magnitude=math.sqrt(0.75), imaginary=True)
    second_coeff = ComplexCoefficient(real_component=second_real_coeff, imaginary_component=second_im_coeff)
    second_state = State(coeff=second_coeff, val=second_state)
    
    state = States(state_array=[first_state, second_state], num_qubits=2)
    
    state.print()
    state.h(qubit)

hadamard("00", "11", 0)
