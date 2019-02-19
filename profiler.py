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
        states.normalize()
        states.register_requirements()
        Profiler().profile_efficiency(func_name, elapsed_time * 1000)
        states.print()
        states.print_density_matrices()
        states.print_state_vectors()
        return result
    return wrapper


class Profiler:
    instance = None

    def __init__(self):
        if not Profiler.instance:
            Profiler.instance = Profiler.__Profiler()

    def __getattr__(self, item):
        return getattr(self.instance, item)

    class __Profiler:

        def __init__(self):
            self.func_profiles = {}

        def profile_efficiency(self, func_name, elapsed_time):
            if func_name not in self.func_profiles:
                self.func_profiles[func_name] = elapsed_time
            else:
                self.func_profiles[func_name] += elapsed_time

        def print(self):
            print(OUTPUT_HEADER)
            for func_name in self.func_profiles:
                print("{:15}".format(func_name), end='')
                print("{0} ms".format(self.func_profiles[func_name]))