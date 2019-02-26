import time
from functools import wraps, partial

OUTPUT_HEADER = "----------------------------------------\nmethod         time\n----------------------------------------"


def normalize_print_and_get_requirements(func):
    """
    Provides automatic normalization, operation result printing
    and requirement registration between state mutations.

    :param func: A method intended to mutate the quantum state.
    :return: The wrapped method with normalization, printing and requirements registration added.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        pfunc = partial(func, *args, **kwargs)
        func_name = func.__name__
        start_time = time.time()
        result = pfunc()
        end_time = time.time()
        elapsed_time = end_time - start_time
        states = args[0]
        if states.kets is not None and len(states.kets) > 0:
            states.normalize()
            states.register_requirements()
            states.print()
            states.print_density_matrices()
            states.print_state_vectors()

        Profiler().profile_efficiency(func_name, elapsed_time * 1000)
        return result
    return wrapper


class Profiler:
    """
    A singleton class used to profile time spent during execution of a quantum program.
    """

    instance = None

    def __init__(self):
        """
        Initializes the singleton if it hasn't already been initialized.
        """
        if not Profiler.instance:
            Profiler.instance = Profiler.__Profiler()

    def __getattr__(self, item):
        """
        Attribute proxy for the underlying singleton instance.

        :param item: The attribute to fetch form the singleton instance.
        :return: The fetched attribute.
        """
        return getattr(self.instance, item)

    class __Profiler:
        """
        A profiler instance.
        """

        def __init__(self):
            """
            Initializes the single profiler instance for hte execution.
            """
            self.func_profiles = {}

        def profile_efficiency(self, func_name, elapsed_time):
            """
            Registers the time spent running the provided method.

            :param func_name: The method being added to the profile.
            :param elapsed_time: The time spent running the method.
            :return:
            """
            if func_name not in self.func_profiles:
                self.func_profiles[func_name] = elapsed_time
            else:
                self.func_profiles[func_name] += elapsed_time

        def print(self):
            """
            Prints the performance profile of the execution with times spent running each method.
            """
            print(OUTPUT_HEADER)
            for func_name in self.func_profiles:
                print("{:15}".format(func_name), end='')
                print("{0} ms".format(self.func_profiles[func_name]))
