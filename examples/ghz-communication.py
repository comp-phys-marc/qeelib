from coefficient import Coefficient
from ket import Ket
from ibmqx_state import IBMQXState as State


def ghz_communication_two_parties(shots, bell_state, server, message):

    initial_coeff = Coefficient(magnitude=1.00, imaginary=False)
    initial_state = Ket(coeff=initial_coeff, val="00000")
    state = State(ket_list=[initial_state], num_qubits=5, device="ibmqx4")

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

    # Bell state measurement
    state.cx(3, 2).h(3)

    # Server measures the state of its qubit
    # 0 corresponds to the outcome |+> and 1 corresponds to the |->
    state.h(1)

    # Uj's decoding operation will be one of 4 depending on the server's
    # publication and the Bell measurement
    #
    # After this decoding step, Uj will have the state prepared by Ui
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
    results = [state.tomography(qubit=q, phases=21, shots=shots) for q in [1, 2, 3, 4]]

    return results


def ghz_communication_three_parties(shots, ghz_state, server, message_i, message_j):

    initial_coeff = Coefficient(magnitude=1.00, imaginary=False)
    initial_state = Ket(coeff=initial_coeff, val="00000")
    state = State(ket_list=[initial_state], num_qubits=5, device="ibmqx4")

    # Create GHZ state
    state.cx(3, 2).h(2).cx(2, 1).cx(1, 0)

    # Ui prepares the state to be transmitted to Ul

    # if message_i == "00":
        # nop
    if message_i == "01":
        state.x(4)
    if message_i == "10":
        state.y(4)
    if message_i == "11":
        state.z(4)

    # Uj prepares the state to be transmitted to Ul

    # if message_j == "0":
        # nop
    if message_j == "1":
        state.x(3)

    # GHZ measurement
    state.cx(4, 3).cx(3, 2).h(4)

    # Server measures the state of its qubit
    # 0 corresponds to the outcome |+> and 1 corresponds to the |->
    state.h(1)

    # Ul's decoding operation will depend on the server's
    # publication and the GHZ measurement
    #
    # After this decoding step, Ul will have the message prepared by Ui and Uj

    # Perform state tomography on received state
    results = state.tomography(qubit=0, phases=21, shots=shots)

    return results


def run_two_party_experiment():

    # Parameters for the states to teleport
    messages_to_transmit = ["00", "01", "10", "11"]

    # Run each case this many times to estimate resulting qubit
    case_trial_array = [1]

    # Expect the server to measure this state for post selection
    server_expect_array = [0, 1]

    # Ui's Bell states to test
    bell_states = [1, 2, 3, 4]

    for message in messages_to_transmit:
        for i in range(len(server_expect_array)):
            for j in range(len(case_trial_array)):
                server_expect = server_expect_array[i]
                shots = case_trial_array[j]

                for bell_state in bell_states:

                    print(
                        "------------ message: {0}, server publication: {1}, Bell state: {2} ------------".format(
                            message,
                            server_expect,
                            bell_state
                        )
                    )

                    exp = ghz_communication_two_parties(
                        shots,
                        bell_state,
                        server_expect,
                        message
                    )

                    print(exp)


def run_three_party_experiment():

    # Parameters for the states to teleport
    messages_to_transmit_i = ["00", "01", "10", "11"]
    messages_to_transmit_j = ["0", "1"]

    # Run each case this many times to estimate resulting qubit
    case_trial_array = [1]

    # Expect the server to measure this state for post selection
    server_expect_array = [0, 1]

    # Ui's Bell states to test
    ghz_states = [1, 2, 3, 4, 5, 6, 7]

    for message_j in messages_to_transmit_j:
        for message_i in messages_to_transmit_i:
            for i in range(len(server_expect_array)):
                for j in range(len(case_trial_array)):
                    server_expect = server_expect_array[i]
                    shots = case_trial_array[j]

                    for ghz_state in ghz_states:

                        print(
                            "------------ message: {0}, server publication: {1}, Bell state: {2} ------------".format(
                                message_j + message_i,
                                server_expect,
                                ghz_state
                            )
                        )

                        exp = ghz_communication_three_parties(
                            shots,
                            ghz_state,
                            server_expect,
                            message_i,
                            message_j
                        )

                        print(exp)


# run_two_party_experiment()
run_three_party_experiment()
