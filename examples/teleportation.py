from ..coefficient import Coefficient
from ..state import State, one, zero
from ..superimposed_states import States
from IPython.utils.capture import capture_output

def teleportation():
    initial_coeff = Coefficient(magnitude=1.00, imaginary=False)
    initial_state = State(coeff=initial_coeff, val="000")
    state = States(state_array=[initial_state], num_qubits=3)
    
    print("State to transmit: {0}\n".format(initial_state.get_val()[2]))
        
    state.h(qubit=0).cx(source=0, target=1).cx(source=2, target=0).h(qubit=2)
    
    m_1 = state.m(qubit=2)
    m_2 = state.m(qubit=0)

    print("Alice measures {0}, {1}\n".format(m_1, m_2))
    
    if m_2 == one:
        state.x(qubit=1)
    if m_1 == one:
        state.z(qubit=1)
        
    state.print_density_matrices()
    
    print("State received: {0}\n".format(state.states[0].get_val()[1]))
    
    state.print_max_requirements()

teleportation()
    