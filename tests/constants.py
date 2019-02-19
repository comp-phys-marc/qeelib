GENERAL_TEST_QASM = '''OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
qreg r[3];
h q;
cx q, r;
creg c[3];
creg d[3];
barrier q;
measure q->c;
measure r->d;
'''

MEASUREMENT_TEST_QASM = '''OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];
measure q->c;
'''

EXPECTED_MEASUREMENT = {'c': [0, 0, 0]}