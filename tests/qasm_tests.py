import unittest
from tests.constants import GENERAL_TEST_QASM, MEASUREMENT_TEST_QASM, EXPECTED_MEASUREMENT
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
