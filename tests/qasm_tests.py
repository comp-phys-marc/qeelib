import unittest
from .constants import GENERAL_TEST_QASM, MEASUREMENT_TEST_QASM, EXPECTED_MEASUREMENT
from parser.parser import run_qasm


class QasmParserTests(unittest.TestCase):

    def test_parser(self):
        try:
            run_qasm(GENERAL_TEST_QASM)
        except Exception as e:
            self.fail(f'Parser raised exception {e}')

    def test_measurement(self):
        result = run_qasm(MEASUREMENT_TEST_QASM)
        self.assertEqual(result.classical_registers, EXPECTED_MEASUREMENT)


