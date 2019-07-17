import datetime
import numpy as np
import csv
from IBMQuantumExperience import IBMQuantumExperience
from functools import reduce
from coefficient import Coefficient
from ket import Ket
from ibmqx_vis_state import VisualizedState as State
from functools import wraps, partial
from ibmqx_state import BackendException
from state import State as VerificationState
from profiler import Profiler
from IPython.utils.capture import capture_output


# GitHub Account
# API_TOKEN = 'a0f9090f4b9b0a7f86cb31848730654bb4dbc35aab364a7d728162c96b264752d413b88daea7303c87f12e0a719345119c0f8a880a27d73b998887664a989fce'

# UWaterloo Account
API_TOKEN = 'c05e0105601b0c1d7e68e294844fdc5615b42f53b6d6a2bb5d6181206fcaec4753276e3bf4bb1eca8cf2bbf179f15b8ecee6df026b13fb8350df2172a6af23a5'
API_URL = 'https://api.quantum-computing.ibm.com/api/Hubs/ibm-q/Groups/open/Projects/main'

# Dr. Farouk's Account
# API_TOKEN = '033df3fead612eb383875727dfe1dbb6022cbd44e1a23410fec2db9f5d09b6e465cf4d7944cd98da84ca65e5b90e77db05d498b70c997989bae6f7d3827c09e9'

BELL_MAPPING = ["00", "01", "10", "11"]


def capture_readout(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with capture_output() as captured:
            try:
                pfunc = partial(func, *args, **kwargs)
                pfunc()

            except BackendException as e:
                print(str(e))
                readout = captured.stdout
                write_file(readout)

        readout = captured.stdout
        write_file(readout)

    return wrapper


def ghz_communication_two_parties(state, shots, bell_state, server, message, manual_analysis=True):

    # Create GHZ state
    state.h(1).cx(1, 2).cx(2, 3)

    # Ui prepares the state to be transmitted to Uj

    # if message == "00":
        # nop
    if message == "01":
        state.x(13)
    if message == "10":
        state.y(13)
    if message == "11":
        state.z(13)

    # Bell state measurement
    state.cx(13, 1).h(13)

    # Server measures the state of its qubit
    # 0 corresponds to the outcome |+> and 1 corresponds to the |->
    state.h(2)

    if manual_analysis:

        # Uj's decoding operation will be one of 4 depending on the server's
        # publication and the Bell measurement
        #
        # After this decoding step, Uj will have the state prepared by Ui
        if bell_state == 1 and server == 1:
            state.z(3)

        if bell_state == 2 and server == 0:
            state.z(3)

        if bell_state == 3 and server == 0:
            state.x(3)

        elif bell_state == 3 and server == 1:
            state.z(3)
            state.x(3)

        if bell_state == 4 and server == 1:
            state.x(3)

        elif bell_state == 4 and server == 0:
            state.z(3)
            state.x(3)

        state.m(1)
        state.m(2)
        state.m(3)
        state.m(13)

        if isinstance(state, State):
            result = state.execute()
            return result, state

        return state

    if isinstance(state, State):

        # Perform state tomography
        receiver_results, receiver_vector = receiver_tomography(state, shots)
        server_results, server_vector = server_tomography(state, shots)

        return server_results, state
    else:
        return state


def receiver_tomography(state, shots):
    state.m(2)
    state.m(13)

    # Perform state tomography
    results, vector = state.tomography(qubit=1, phases=21, shots=shots)
    print("Qubit 0 Bloch vector: {0}".format(str(vector)))

    return results, vector


def server_tomography(state, shots):
    state.m(1)
    state.m(13)

    # Perform state tomography
    results, vector = state.tomography(qubit=2, phases=21, shots=shots)
    print("Qubit 0 Bloch vector: {0}".format(str(vector)))

    return results, vector


def ghz_like_communication_two_parties(state, shots, bell_state, server, message, manual_analysis=True):

    # Create GHZ-like state
    state.h(1).cx(1, 2).h(12).cx(12, 2)

    # Ui prepares the state to be transmitted to Uj

    # if message == "00":
        # nop
    if message == "01":
        state.x(13)
    if message == "10":
        state.y(13)
    if message == "11":
        state.z(13)

    # Bell state measurement
    state.cx(13, 1).h(13)

    # Server measures the state of its qubit
    # 0 corresponds to the outcome |+> and 1 corresponds to the |->
    state.h(2)

    if manual_analysis:

        # Uj's decoding operation will be one of 4 depending on the server's
        # publication and the Bell measurement
        #
        # After this decoding step, Uj will have the state prepared by Ui
        if bell_state == 1 and server == 1:
            state.z(12)

        if bell_state == 2 and server == 0:
            state.z(12)

        if bell_state == 3 and server == 0:
            state.x(12)

        elif bell_state == 3 and server == 1:
            state.z(12)
            state.x(12)

        if bell_state == 4 and server == 1:
            state.x(12)

        elif bell_state == 4 and server == 0:
            state.z(12)
            state.x(12)

        state.m(1)
        state.m(2)
        state.m(12)
        state.m(13)

        if isinstance(state, State):
            result = state.execute()
            return result, state

        return state

    if isinstance(state, State):

        # Perform state tomography
        # receiver_results, receiver_vector = receiver_tomography(state, shots)
        server_results, server_vector = server_tomography(state, shots)

        return server_results, state
    else:
        return state


def ghz_communication_three_parties(state, shots, message_i, message_j):

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
    state.h(3).cx(3, 4).cx(3, 2)

    # Server measures the state of its qubit
    # 0 corresponds to the outcome |+> and 1 corresponds to the |->
    state.h(1)

    # Ul's decoding operation will depend on the server's
    # publication and the GHZ measurement
    #
    # After this decoding step, Ul will have the message prepared by Ui and Uj

    # Perform state tomography on received state
    if isinstance(state, State):
        results, vector = state.tomography(qubit=0, phases=21, shots=shots)
        print("Bloch vector: {0}".format(str(vector)))

        return results, state
    else:
        return state


def verify_ghz_communication_two_parties(shots, bell_state, server_expect, message):
    verify_coeff = Coefficient(magnitude=1.00, imaginary=False)
    verify_state = Ket(coeff=verify_coeff, val="00000000000000")
    verification_state = VerificationState(ket_list=[verify_state], num_qubits=14, symbol='g')

    ghz_communication_two_parties(
        verification_state,
        shots,
        bell_state,
        server_expect,
        message
    )

    verification_state.post_select({
        1: str(server_expect),
        2: BELL_MAPPING[bell_state - 1][0],
        3: BELL_MAPPING[bell_state - 1][1]
    })


def execute_ghz_communication_two_parties(shots, bell_state, server_expect, message, manual):
    initial_coeff = Coefficient(magnitude=1.00, imaginary=False)
    initial_state = Ket(coeff=initial_coeff, val="00000000000000")
    state = State(ket_list=[initial_state], num_qubits=14, device="ibmq_16_melbourne", symbol='g', api_token=API_TOKEN, url=API_URL)

    ghz_exp = ghz_communication_two_parties(
        state,
        shots,
        bell_state,
        server_expect,
        message,
        manual_analysis=manual
    )

    print(ghz_exp)


def verify_ghz_like_communication_two_parties(shots, bell_state, server_expect, message):
    verify_coeff = Coefficient(magnitude=1.00, imaginary=False)
    verify_state = Ket(coeff=verify_coeff, val="00000000000000")
    verification_state = VerificationState(ket_list=[verify_state], num_qubits=14, symbol='l')

    ghz_like_communication_two_parties(
        verification_state,
        shots,
        bell_state,
        server_expect,
        message
    )

    verification_state.post_select({
        1: str(server_expect),
        2: BELL_MAPPING[bell_state - 1][0],
        3: BELL_MAPPING[bell_state - 1][1]
    })


def execute_ghz_like_communication_two_parties(shots, bell_state, server_expect, message, manual):
    initial_coeff = Coefficient(magnitude=1.00, imaginary=False)
    initial_state = Ket(coeff=initial_coeff, val="00000000000000")
    state = State(ket_list=[initial_state], num_qubits=14, device="ibmq_16_melbourne", symbol='l', api_token=API_TOKEN, url=API_URL)

    ghz_like_exp = ghz_like_communication_two_parties(
        state,
        shots,
        bell_state,
        server_expect,
        message,
        manual_analysis=manual
    )

    print(ghz_like_exp)


@capture_readout
def run_two_party_experiment():

    profiler = Profiler()

    # Parameters for the states to teleport
    messages_to_transmit = ["00"]

    # Run each case this many times to estimate resulting qubit
    case_trial_array = [1024]

    # Expect the server to measure this state for post selection
    server_expect_array = [0]

    # Ui's Bell states to test
    bell_states = [1]  # [1, 2, 3, 4]

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

                    # verify_ghz_communication_two_parties(shots, bell_state, server_expect, message)
                    # execute_ghz_communication_two_parties(shots, bell_state, server_expect, message, manual=False)

                    # verify_ghz_like_communication_two_parties(shots, bell_state, server_expect, message)
                    execute_ghz_like_communication_two_parties(shots, bell_state, server_expect, message, manual=False)

    profiler.print()


def run_three_party_experiment():

    profiler = Profiler()

    # Parameters for the states to teleport
    messages_to_transmit_i = ["00", "01", "10", "11"]
    messages_to_transmit_j = ["0", "1"]

    # Run each case this many times to estimate resulting qubit
    case_trial_array = [1024]

    # Expect the server to measure this state for post selection
    server_expect_array = [0, 1]

    # Ui's Bell states to test
    ghz_states = [1, 2, 3, 4, 5, 6, 7, 8]
    ghz_mapping = ["000", "001", "010", "011", "100", "101", "110", "111"]

    for message_j in messages_to_transmit_j:
        for message_i in messages_to_transmit_i:
            for i in range(len(server_expect_array)):
                for j in range(len(case_trial_array)):
                    server_expect = server_expect_array[i]
                    shots = case_trial_array[j]

                    for ghz_state in ghz_states:

                        print(
                            "------------ message: {0}, server publication: {1}, GHZ state: {2} ------------".format(
                                message_i + message_j,
                                server_expect,
                                ghz_state
                            )
                        )

                        verify_coeff = Coefficient(magnitude=1.00, imaginary=False)
                        verify_state = Ket(coeff=verify_coeff, val="00000000000000")
                        verification_state = VerificationState(ket_list=[verify_state], num_qubits=14)

                        ghz_communication_three_parties(
                            verification_state,
                            shots,
                            ghz_state,
                            server_expect,
                            message_i,
                            message_j
                        )

                        verification_state.post_select({
                            1: str(server_expect),
                            2: ghz_mapping[ghz_state - 1][0],
                            3: ghz_mapping[ghz_state - 1][1],
                            4: ghz_mapping[ghz_state - 1][2]
                        })

                        initial_coeff = Coefficient(magnitude=1.00, imaginary=False)
                        initial_state = Ket(coeff=initial_coeff, val="00000000000000")
                        state = State(
                            ket_list=[initial_state],
                            num_qubits=14,
                            device="ibmq_16_melbourne",
                            api_token=API_TOKEN
                        )

                        exp = ghz_communication_three_parties(
                            state,
                            shots,
                            ghz_state,
                            server_expect,
                            message_i,
                            message_j
                        )

                        print(exp)

    profiler.print()


def write_file(readout):
    file = open("outputs/{0} GHZ communication output.txt".format(datetime.datetime.now()), "w+")
    file.write(readout)
    file.close()


def visualize():
    visualization_state = State(
        ket_list=[],
        num_qubits=14,
        device="ibmq_16_melbourne",
        symbol='l',
        api_token=API_TOKEN,
        url=API_URL
    )
    visualization_state.job_ids = [job['id'] for job in visualization_state.api.get_jobs(backend="ibmq_16_melbourne")]
    visualization_state.load_jobs()
    visualization_state.visualize_state_city()


def export_fidelity_to_csv(bell_indicators, jobs):

    bell_states = [1, 2, 3, 4]
    server_expectations = [0, 1]

    fidelity_level = 0

    for job in jobs:
        for exp in job['qasms']:

            if 'u1' not in exp['qasm']:  # is it a tomography circuit?

                with open(f'outputs/{job["id"]}.csv', 'w+') as writeFile:
                    writer = csv.writer(writeFile)
                    labels = list(exp['result']['data']['counts'].keys())
                    values = list(exp['result']['data']['counts'].values())

                    if reduce((lambda sum, label: int(sum) + int(label[3])),
                              labels) > 0:  # is it GHZ or GHZ-like?

                        type = "GHZ-like"
                        symbol = 'l'
                        receiver = '12'
                    else:
                        type = "GHZ"
                        symbol = 'g'
                        receiver = '3'

                    for bell_state in bell_states:
                        bell_indicator = bell_indicators[bell_state-1]

                        for server_expect in server_expectations:

                            if (bell_state == 1 and server_expect == 0) or (bell_state == 2 and server_expect == 1):
                                if f'h {symbol}[2];\nmeasure' not in exp['qasm']:
                                    continue

                            if (bell_state == 1 and server_expect == 1) or (bell_state == 2 and server_expect == 0):
                                if f'h {symbol}[2];\nz {symbol}[{receiver}]' not in exp['qasm']:
                                    continue
                                if f'h {symbol}[2];\nz {symbol}[{receiver}];\nx {symbol}[{receiver}];' in exp['qasm']:
                                    continue

                            if (bell_state == 3 and server_expect == 0) or (bell_state == 4 and server_expect == 1):
                                if f'h {symbol}[2];\nx {symbol}[{receiver}]' not in exp['qasm']:
                                    continue
                                if f'h {symbol}[2];\nz {symbol}[{receiver}];\nx {symbol}[{receiver}]' in exp['qasm']:
                                    continue

                            if (bell_state == 3 and server_expect == 1) or (bell_state == 4 and server_expect == 0):
                                if f'h {symbol}[2];\nz {symbol}[{receiver}];\nx {symbol}[{receiver}]' not in exp['qasm']:
                                    continue

                            server_correct = 0
                            receiver_correct = 0
                            p_set = 0
                            p_clear = 0

                            if type == "GHZ-like":

                                for i in range(len(labels)):
                                    if (int(labels[i][-3]) == server_expect):  # server's measurement is correct!
                                        server_correct += values[i]
                                        if ((int(labels[i][-2]) == bell_indicator[0]) and (
                                                int(labels[i][2]) == bell_indicator[1])):  # receiver's measurement is correct!
                                            receiver_correct += values[i]
                                            if (int(labels[i][3]) == 1):  # and the result is a 1
                                                p_set += int(values[i])
                                            elif (int(labels[i][3]) == 0):  # and the result is a 0
                                                p_clear += int(values[i])

                            else:

                                for i in range(len(labels)):
                                    if (int(labels[i][-3]) == server_expect):  # server's measurement is correct!
                                        server_correct += values[i]
                                        if ((int(labels[i][-2]) == bell_indicator[0]) and (
                                                int(labels[i][2]) == bell_indicator[1])):  # receiver's measurement is correct!
                                            receiver_correct += values[i]
                                            if (int(labels[i][-4]) == 1):  # and the result is a 1
                                                p_set += int(values[i])
                                            elif (int(labels[i][-4]) == 0):  # and the result is a 0
                                                p_clear += int(values[i])

                            writer.writerow(['Bell state', 'Server expect', 'Fidelity'])
                            writer.writerow([f'{bell_state}', f'{server_expect}', p_set/(p_set + p_clear)])

                            fidelity_level += p_set/(p_set + p_clear)

                    writer.writerow(["experiment", exp['executionId']])
                    writer.writerow(["date", exp['result']['date']])
                    for count in exp['result']['data']['counts']:
                        line = [count, exp['result']['data']['counts'][count]]
                        writer.writerow(line)

                    writer.writerow(["qasm", exp["qasm"]])
                    writer.writerow(["type", type])

    return fidelity_level


def export_fidelity_data():
    bell_indicators = ((0, 0), (0, 1), (1, 0), (1, 1))
    jobs = IBMQuantumExperience(API_TOKEN).get_jobs(backend="ibmq_16_melbourne", limit=55)
    export_fidelity_to_csv(bell_indicators, jobs)


def collect_tomography_data(symbol):
    jobs = IBMQuantumExperience(API_TOKEN).get_jobs(backend="ibmq_16_melbourne", limit=200)

    bloch_vectors = {}
    exp_vector = range(0, 21)

    for qubit in [2]:
        for index in exp_vector:
            found_x = False
            found_y = False
            found_z = False
            phase = 2 * np.pi * index / (len(exp_vector) - 1)
            for job in jobs:
                for exp in job['qasms']:
                    if f'{symbol}[{qubit}]' not in exp['qasm'] or str(phase) not in exp['qasm']:
                        continue
                    if f'u1({phase}) {symbol}[{qubit}];\nh {symbol}[{qubit}];' in exp['qasm']:
                        found_x = True
                        bloch_vectors[index * 3] = exp
                    elif f'u1({phase}) {symbol}[{qubit}];\nsdg {symbol}[{qubit}];' in exp['qasm']:
                        bloch_vectors[index * 3 + 1] = exp
                        found_y = True
                    elif f'u1({phase}) {symbol}[{qubit}];\nbarrier {symbol}[{qubit}];' in exp['qasm']:
                        bloch_vectors[index * 3 + 2] = exp
                        found_z = True
            if not found_x:
                print(f'No X circuit found for phase {phase}')
            if not found_y:
                print(f'No Y circuit found for phase {phase}')
            if not found_z:
                print(f'No Z circuit found for phase {phase}')

        bloch_vectors = State.post_analyze_tomographic_results(0, exp_vector, bloch_vectors)
        print(bloch_vectors)


run_two_party_experiment()
# collect_tomography_data('g')
