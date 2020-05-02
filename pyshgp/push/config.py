class PushConfig:
    """A configuration for a Push program.

    Parameters
    ----------
    step_limit : int, optional
        Max number of atoms to process before terminating the execution of a
        given program. Default is 500
    runtime_limit : int, optional
        Max number of milliseconds to run a push program before forcing
        termination. Default is 5000.
    growth_cap : int, optional
        Max number of elements that can be added to a PushState at any given
        step of program execution. If exceeded, program terminates. Default is
        500.
    collection_size_cap : int, optional
        Max size of any collection (code blocks, vectors, strings, etc). Default is 1000.


    Attributes
    ----------
    step_limit : int
        Max number of atoms to process before terminating the execution of a
        given program. Default is 500
    runtime_limit : int
        Max number of milliseconds to run a push program before forcing
        termination. Default is 5000.
    growth_cap : int
        Max number of elements that can be added to a PushState at any given
        step of program execution. If exceeded, program terminates. Default is
        500.
    collection_size_cap : int, optional
        Max size of any collection (code blocks, vectors, strings, etc). Default is 1000.

    """

    def __init__(self, *,
                 step_limit=500,
                 runtime_limit=5000,
                 growth_cap=500,
                 collection_size_cap=1000):
        self.step_limit = step_limit
        self.runtime_limit = runtime_limit
        self.growth_cap = growth_cap
        self.collection_size_cap = collection_size_cap
