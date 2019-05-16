from coefficient import Coefficient
from ket import Ket
from ibmqx_state import IBMQXState as State


def ghz_communication_partial_servcer_cooperation(shots, bell_state, server, message):

    initial_coeff = Coefficient(magnitude=1.00, imaginary=False)
    initial_state = Ket(coeff=initial_coeff, val="00000")
    state = State(ket_list=[initial_state], num_qubits=5)

    # Create GHZ state
    state.h(2).cx(2, 1).cx(1, 0)

    # Ui prepares the state to be transmitted to Uj

    # if message == "00":
        # nop
    if message == "01":
        state.x(3)
    if message == "10":
        state.y(3)
    if message == "11":
        state.z(3)

    # Uj performs Bell state measurement
    state.cx(3, 2).h(3)

    # Server measures the state of its qubit
    # 0 corresponds to the outcome |+> and 1 corresponds to the |->
    state.h(1).m(1)

    state.barrier()

    # Uj's decoding operation will be one of 4 depending on the server's publication and the Bell measurement
    if bell_state == 1 and server == 1:
        state.z(0)

    if bell_state == 2 and server == 0:
        state.z(0)

    if bell_state == 3 and server == 0:
        state.x(0)

    elif bell_state == 3 and server == 1:
        state.z(0)
        state.x(0)

    if bell_state == 4 and server == 1:
        state.x(0)

    elif bell_state == 4 and server == 0:
        state.z(0)
        state.x(0)

    # Perform state tomography
    tomography_results = [state.tomography(qubit=q, phases=21, shots=shots) for q in range(5)]

    return tomography_results


def run_experiment():

    # Parameters for the states to teleport
    messages_to_transmit = ["01", "10", "11"]

    # Run each case this many times to estimate resulting qubit
    case_trial_array = [1024]

    # Expect the server to measure this state for post selection
    server_expect_array = [0, 1, -1]

    # Ui's Bell states to test
    bell_states = [1, 2, 3, 4]

    for message in messages_to_transmit:
        for i in range(len(server_expect_array)):
            for j in range(len(case_trial_array)):
                server_expect = server_expect_array[i]
                shots = case_trial_array[j]

                for bell_state in bell_states:

                    exp = ghz_communication_partial_servcer_cooperation(
                        shots,
                        bell_state,
                        server_expect,
                        message
                    )

                    print(exp)

run_experiment()