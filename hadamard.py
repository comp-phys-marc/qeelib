from coefficient import Coefficient, ComplexCoefficient
from state import State
from superimposed_states import States
import math

def hadamard_edge(first_state, second_state, qubit):
    first_coeff = Coefficient(magnitude=1.00, imaginary=False)
    first_state = State(coeff=first_coeff, val=first_state)
    
    second_coeff = Coefficient(magnitude=0.00, imaginary=False)
    second_state = State(coeff=second_coeff, val=second_state)
    
    state = States(state_array=[first_state, second_state], num_qubits=2)
    
    state.print()
    state.h(qubit)
    
def hadamard_chief(first_state, second_state, third_state, fourth_state, qubit):
    first_coeff = Coefficient(magnitude=1.00, imaginary=False)
    first_state = State(coeff=first_coeff, val=first_state)
    
    second_coeff = Coefficient(magnitude=0.00, imaginary=False)
    second_state = State(coeff=second_coeff, val=second_state)
    
    third_coeff = Coefficient(magnitude=1.00, imaginary=False)
    third_state = State(coeff=third_coeff, val=third_state)
    
    fourth_coeff = Coefficient(magnitude=0.00, imaginary=False)
    fourth_state = State(coeff=fourth_coeff, val=fourth_state)
    
    state = States(state_array=[first_state, second_state, third_state, fourth_state], num_qubits=2)
    
    state.print()
    state.h(qubit)

hadamard_chief("00", "01", "10", "11", 0)
