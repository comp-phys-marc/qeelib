from ibmqx_state import IBMQXState
from qiskit import IBMQ
from qiskit.visualization import(
  plot_state_city,
  plot_bloch_multivector,
  plot_state_paulivec,
  plot_state_hinton,
  plot_state_qsphere
)


class VisualizedState(IBMQXState):
    """
    A class that abstracts the visualization features provided by IBM's qiskit.
    """

    def __init__(self, api_token, url, ket_list=[], num_qubits=1, symbol='q', qasm=None, device='ibmqx4', api=None, job_ids=[]):
        """
        Initializes a quantum state with the given parameters.

        :param api_token: The IBMQX access token for the user.
        :param url: The IBMQX url for the user.
        :param ket_list: The kets are only used to print the initial state.
        :param num_qubits: The total number of qubits.
        :param symbol: The identifier for this quantum state.
        :param qasm: Predefined qasm provided to initialization.
        :param device: The IBM device to execute on.
        :param api: A pre-initialized api.
        :param: job_ids: A set of job ids
        """

        self.api_token = api_token
        self.url = url
        self.device = device
        self._connect()
        self.job_ids = job_ids
        self.load_jobs()
        super().__init__(ket_list, num_qubits, symbol, qasm, device, api, api_token)

    def _connect(self):
        IBMQ.enable_account(self.api_token, self.url)
        self.backend = IBMQ.get_backend(self.device)
        super()._connect()

    def load_jobs(self):
        self.jobs = [self.backend.retrieve_job(id) for id in self.job_ids]

    def visualize_state_city(self):
        if not self.jobs:
            print("No executions to visualize.")
            return
        locations = []
        for job in self.jobs:
            result = job.result()
            psi = result.get_statevector()
            fig = plot_state_city(psi)
            location = f'outputs/{self.symbol}-{id}.png'
            locations.append(location)
            fig.savefig(location, bbox_inches='tight')

        return locations
