from coefficient import Coefficient
from ket import Ket
from ibmqx_state import IBMQXState as State


def controlled_teleportation(shots, bell_state, charlie, theta, phi, lamb):

    initial_coeff = Coefficient(magnitude=1.00, imaginary=False)
    initial_state = Ket(coeff=initial_coeff, val="00000")
    state = State(ket_list=[initial_state], num_qubits=5)

    # Create GHZ state
    state.h(2).cx(2, 1).cx(1, 0)

    # Prepare state to be teleported
    state.u3(theta, phi, lamb, 3)

    # Alice performs Bell state measurement entangling x and A
    state.cx(3, 2).h(3)

    # Measure the state of qubit C to obtain Rc
    # 0 corresponds to the outcome |+> and 1 corresponds to the |->
    state.h(1).m(1)

    # Bob's U will be one of 4 gates depending on Rc and the bell measurement used
    if bell_state == 1 and charlie == 1:
        state.z(0)

    if bell_state == 2 and charlie == 0:
        state.z(0)

    if bell_state == 3 and charlie == 0:
        state.x(0)

    elif bell_state == 3 and charlie == 1:
        state.z(0)
        state.x(0)

    if bell_state == 4 and charlie == 1:
        state.x(0)

    elif bell_state == 4 and charlie == 0:
        state.z(0)
        state.x(0)

    # Perform state tomography
    tomography_results, vector = [state.tomography(qubit=q, phases=21, shots=shots) for q in range(4)]
    return tomography_results


def run_experiment():

    # parameters for the states to teleport
    teleport_prep_gates = [["pi/6", "-pi/2", "pi/2"], ["pi/5", "-pi/2", "pi/2"], ["pi/4", "-pi/2", "pi/2"],
                           ["pi/3", "-pi/2", "pi/2"],
                           ["pi/2", "-pi/2", "pi/2"]]

    # run each case this many times to estimate resulting qubit
    case_trial_array = [1024]

    # expect charlie to measure this state for post selection
    charlie_expect_array = [0, 1, -1]

    # Alice's bell states to test
    bell_states = [1, 2, 3, 4]

    for gate in teleport_prep_gates:
        for i in range(len(charlie_expect_array)):
            for j in range(len(case_trial_array)):
                charlie_expect = charlie_expect_array[i]
                shots = case_trial_array[j]

                for bell_state in bell_states:

                    exp = controlled_teleportation(shots, bell_state, charlie_expect, gate[0], gate[1], gate[2])
                    print(exp)
