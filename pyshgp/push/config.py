from pyrsistent import PRecord, field


class PushConfig(PRecord):
    """A configuration for a Push program.

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
    step_limit = field(type=int, initial=500, mandatory=True)
    runtime_limit = field(type=int, initial=5000, mandatory=True)
    growth_cap = field(type=int, initial=500, mandatory=True)
    collection_size_cap = field(type=int, initial=1000, mandatory=True)
