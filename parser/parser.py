import re
from itertools import zip_longest
from .patterns import INCLUDE, SEMICOLON, QREG, CREG, HEADER, BARRIER, MEASURE, \
    CONTROL_X, PAULI_X, PAULI_Y, PAULI_Z, HADAMARD, SPACE, ASSIGN, OPEN_BRACKET
from superimposed_states import States
from state import State, ZERO
from ensemble import Ensemble
from coefficient import Coefficient


class UnsupportedInputException(Exception):
    pass


class BadHeaderException(Exception):
    pass


class QasmProgrammingException(Exception):
    pass


class Parser:

    def __init__(self, qubits=0, q_name=None, bits=0, b_name=None):

        self.ensemble = Ensemble()
        self._gates = {'ensemble': {CONTROL_X: self.ensemble.cx}}

        self.quantum_registers = {}
        self._quantum_register_names = {}

        self.classical_registers = {}
        self._classical_register_names = {}

        if not qubits == 0 and q_name is not None:
            self.add_quantum_reg(qubits, q_name)

        if not bits == 0 and b_name is not None:
            self.add_classical_reg(bits, b_name)

    def add_quantum_reg(self, qubits, name):
        new_coeffs = [Coefficient(magnitude=1.00, imaginary=False) for q in range(qubits)]
        new_states = [State(coeff=coeff, val=ZERO * qubits) for coeff in new_coeffs]

        self.ensemble.add_subsystem(States(state_array=new_states, num_qubits=qubits, symbol=name), name)

        self.ensemble.subsystems[name].normalize()

        self.quantum_registers[len(self.quantum_registers.keys())] = qubits
        self._quantum_register_names[name] = len(self._quantum_register_names.keys())

        self._gates[name] = {
            PAULI_X: self.ensemble.subsystems[name].x,
            PAULI_Z: self.ensemble.subsystems[name].z,
            PAULI_Y: self.ensemble.subsystems[name].y,
            HADAMARD: self.ensemble.subsystems[name].h,
            MEASURE: self.ensemble.subsystems[name].m
        }

    def add_classical_reg(self, bits, name):
        self.classical_registers[name] = [0 for b in range(bits)]
        self._classical_register_names[name] = len(self._classical_register_names.keys())

    def _gate_from_qasm_line(self, line, registers):
        operator = line.split(SPACE)[0]
        method = None

        if operator == CONTROL_X:
            method = self._gates['ensemble'][CONTROL_X]
            return method

        for register_name in registers:
            for gate in self._gates[register_name]:
                if gate.lower() == operator.lower():
                    method = self._gates[register_name][gate]

        return method

    @property
    def _inverted_quantum_register_names(self):
        return dict([v, k] for k, v in self._quantum_register_names.items())

    @property
    def _inverted_classical_register_names(self):
        return dict([v, k] for k, v in self._classical_register_names.items())

    def _find_quantum_reg_by_name(self, register_name):
        return self._quantum_register_names[register_name]

    @staticmethod
    def _find_classical_reg_by_name(register_name):
        return register_name

    def _parse_quantum_operands(self, line):
        return self._parse_operands(line,
                                    self._inverted_quantum_register_names,
                                    self.quantum_registers,
                                    self._find_quantum_reg_by_name
                                    )

    def _parse_classical_operands(self, line):
        return self._parse_operands(line,
                                    self._inverted_classical_register_names,
                                    self.classical_registers,
                                    self._find_classical_reg_by_name
                                    )

    def _parse_operands(self, line, register_names, registers, reg_lookup_method):

        operands = line

        if SPACE in line:
            elements = line.split(SPACE)
            del elements[0]
            operands = ''.join(elements)

        register_entries = {}
        register_name = None

        inverted_register_names = register_names
        qubit_loc = -1
        reg_index = 0
        while qubit_loc == -1 and reg_index < len(inverted_register_names.keys()):
            register_name = inverted_register_names[reg_index]
            qubit_loc = operands.find(register_name)
            reg_index += 1

        if reg_index > len(inverted_register_names.keys()):
            raise QasmProgrammingException(f'No operand provided for operation: {line}')

        register_entries[register_name] = []

        while qubit_loc != -1:
            if len(operands) > (qubit_loc + 2) and operands[qubit_loc + 1] == OPEN_BRACKET:  # it is a qubit level operation
                if register_name in register_entries:
                    register_entries[register_name].append(int(operands[qubit_loc + 2]))
            else:  # it is a register level operation

                target_register = reg_lookup_method(register_name)

                target_bits = []
                if isinstance(registers[target_register], int):
                    target_bits = [i for i in range(registers[target_register])]
                elif isinstance(registers[target_register], list):
                    target_bits = [i for i in range(len(registers[target_register]))]
                reg_targets = []

                for target_bit in target_bits:
                    reg_targets.append(target_bit)
                register_entries[register_name] += reg_targets

            next_qubit_loc = -1
            reg_index = 0
            while next_qubit_loc == -1 and reg_index < len(inverted_register_names.keys()):
                register_name = inverted_register_names[reg_index]
                next_qubit_loc = operands.find(register_name, qubit_loc + 1, len(operands))
                reg_index += 1

            qubit_loc = next_qubit_loc

            if reg_index > len(inverted_register_names.keys()):
                break

            if register_name not in register_entries and qubit_loc != -1:
                register_entries[register_name] = []

        return register_entries

    def _measure(self, line):

        operands = line.split(ASSIGN)

        source_qubits = operands[0]
        dest_bits = operands[1]
        qubits = self._parse_quantum_operands(source_qubits)
        bits = self._parse_classical_operands(dest_bits)

        register = list(qubits.keys())[0]
        method = self._gates[register][MEASURE]

        for quantum_register, classical_register in zip_longest(qubits, bits):
            for target_qubit, target_bit in zip_longest(qubits[quantum_register], bits[classical_register]):
                result = method(target_qubit)
                self.classical_registers[classical_register][int(target_bit)] = int(result)

        return self.classical_registers

    def _parse_operation(self, line):
        qubits = self._parse_quantum_operands(line)
        method = self._gate_from_qasm_line(line, qubits.keys())

        if method is None or len(qubits) == 0:
            raise UnsupportedInputException(f'Unsupported QASM operation {line}.')

        if method.__name__ != CONTROL_X:
            for register in qubits.keys():
                for target_qubit in qubits[register]:
                    method(target_qubit)
        else:
            registers = []
            for register in qubits.keys():
                registers.append(register)
            if len(qubits.keys()) == 2 and (len(qubits[registers[0]]) == len(qubits[registers[1]])):
                for controller, controlled in zip_longest(qubits[registers[0]], qubits[registers[1]]):
                    method(registers[0], controller, registers[1], controlled)
            elif len(qubits.keys()) == 1 and len(registers[0] == 2):
                method(*registers[0])


def _bits_for_reg_init(line):
    elements = line.split(SPACE)
    del elements[0]
    operands = ''.join(elements)

    register_name = operands[0]
    qubits = int(operands[2])

    return qubits, register_name


def run_qasm(qasm):
    lines = qasm.replace('\n', '').split(SEMICOLON)
    parser = None

    if re.match(HEADER, lines[0]):
        header = lines.pop(0)
        print(f'Found header. Recognized QASM version: {header}')
    else:
        raise BadHeaderException(f'No well-formed header present at the top of the file.')

    while len(lines) > 0:

        if lines[0] == '':
            del lines[0]
            break

        if INCLUDE in lines[0] or BARRIER in lines[0]:
            del lines[0]

        if QREG in lines[0]:
            line = lines.pop(0)
            reg_qubits, reg_name = _bits_for_reg_init(line)
            if parser is None:
                parser = Parser(qubits=reg_qubits, q_name=reg_name)
            else:
                parser.add_quantum_reg(reg_qubits, reg_name)

        elif CREG in lines[0] or BARRIER in lines[0]:
            line = lines.pop(0)
            reg_bits, reg_name = _bits_for_reg_init(line)
            if parser is None:
                parser = Parser(bits=reg_bits, b_name=reg_name)
            else:
                parser.add_classical_reg(reg_bits, reg_name)

        elif MEASURE in lines[0]:
            parser._measure(lines.pop(0))

        elif parser is not None:
            parser._parse_operation(lines.pop(0))

        else:
            raise QasmProgrammingException('QREG command not found before first QASM operation.')

    return parser