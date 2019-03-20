import unittest
from tests.constants import GENERAL_TEST_QASM, MEASUREMENT_TEST_QASM, EXPECTED_MEASUREMENT, \
    TEN_Q_CC_QASM_ZERO, TEN_Q_CC_QASM_ONE, GROVER_TEST_QASM
from parser.parser import run_qasm


class QasmParserTests(unittest.TestCase):

    def test_parser(self):
        print("Testing Parser...")
        try:
            result, performance_profile = run_qasm(GENERAL_TEST_QASM)
            performance_profile.print()
        except Exception as e:
            self.fail(f'Parser raised exception {e}')

    def test_measurement(self):
        print("Testing Measurement...")
        result, performance_profile = run_qasm(MEASUREMENT_TEST_QASM)
        performance_profile.print()
        self.assertEqual(result.classical_registers, EXPECTED_MEASUREMENT)

    def test_grover(self):
        print("Testing grover search circuit...")
        result, performance_profile = run_qasm(GROVER_TEST_QASM)
        performance_profile.print()

    def test_counterfeit_coin_benchmarks(self):
        print("Testing 10 qubit benchmark circuit 0...")
        result, performance_profile = run_qasm(TEN_Q_CC_QASM_ZERO)
        performance_profile.print()

        print("Testing 10 qubit benchmark circuit 1...")
        result, performance_profile = run_qasm(TEN_Q_CC_QASM_ONE)
        performance_profile.print()
