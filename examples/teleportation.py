from coefficient import Coefficient
from ket import Ket, ONE
from state import State


def teleportation():
    initial_coeff = Coefficient(magnitude=1.00, imaginary=False)
    initial_state = Ket(coeff=initial_coeff, val="000")
    state = State(ket_list=[initial_state], num_qubits=3)
    
    print("State to transmit: {0}\n".format(initial_state.get_val()[2]))
        
    state.h(qubit=0).cx(source=0, target=1).cx(source=2, target=0).h(qubit=2)
    
    m_1 = state.m(qubit=2)
    m_2 = state.m(qubit=0)

    print("Alice measures {0}, {1}\n".format(m_1, m_2))
    
    if m_2 == ONE:
        state.x(qubit=1)
    if m_1 == ONE:
        state.z(qubit=1)
        
    state.print_density_matrices()
    
    print("State received: {0}\n".format(state.kets[0].get_val()[1]))
    
    state.print_max_requirements()

teleportation()
