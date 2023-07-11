import pdfquery
from lxml import etree
from operator import itemgetter

from coefficient import Coefficient
from ibmqx_state import IBMQXState as State
from ket import Ket


GATES = [
    'x',
    'y',
    'z',
    'u1',
    'u2',
    'u3',
    's',
    'sdg',
    'h',
    'tdg',
    'cx',
    'cy',
    'cz',
    't',
    'ccx',
    'reset',
    'cu1',
    'ccy',
    'ccz'
]

pdf = pdfquery.PDFQuery("Circuits.pdf")
pdf.load()

pdf.tree.write('readable.xml', pretty_print=True)

tree = etree.parse(open("readable.xml", "r"))
root = tree.getroot()

wires = {}

for element in root.iter(tag=etree.Element):
    if 'x0' in element.attrib.keys():
        print("%s - %s - (%s, %s)" % (element.tag, element.text, element.attrib['x0'], element.attrib['y0']))

    # if we have a wire
    if element.tag == 'LTTextLineHorizontal':
        # get the vertical position
        y = element.attrib['y0']
        # register the wire
        if y not in wires.keys():
            wires[y] = []

    # if we have a gate
    if element.tag == 'LTTextBoxHorizontal':
        # find the wire
        wire = element.attrib['y0']
        # register the wire if needed
        if wire not in wires.keys():
            wires[wire] = []
        # register the gate
        if element.text.strip().lower() in GATES:
            wires[wire].append({'name': element.text.strip().lower(), 'index': element.attrib['x0']})
            # sort the wire's gates by x index
            wires[wire] = sorted(wires[wire], key=itemgetter('index'))

qasm = ''

initial_coeff = Coefficient(magnitude=1.00, imaginary=False)
initial_state = Ket(coeff=initial_coeff, val="".join(["0" for i in range(len(wires))]))
state = State(ket_list=[initial_state], num_qubits=len(wires))

for wire, gates in wires.items():
    for gate in gates:
        getattr(state, gate['name'])(list(wires.keys()).index(wire))

print(state.qasm)
