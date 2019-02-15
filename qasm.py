from coefficient import Coefficient, ComplexCoefficient
from state import State, one
from superimposed_states import States
from qiskit-terra.qiskit.qasm._qasm import Qasm

def interpret_qasm(qasm_code):
    parsed_code = Qasm(qasm_code).parse()
    print(parsed_code)