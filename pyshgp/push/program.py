"""The :mod:`program` module defines an abstraction to represent Push programs and their the specification.

Program objects encapsulate everything required to execute the program on a Push interpreter with the exception
of instruction definitions. Programs are serializable, and thus can be saved and reused. There is the possibility
(but not a guarantee) that Push programs can be executed across different versions of ``pyshgp`.

"""
from pyrsistent import PRecord, field

from pyshgp.push.config import PushConfig
from pyshgp.push.atoms import CodeBlock
from pyshgp.utils import Saveable


class ProgramSignature(PRecord):
    """A specification of a Push program.

    Attributes
    ----------
    arity : int
        The number of inputs that the program will take.
    output_stacks : List[str]
        The names of the stack(s) which the output values will be pulled from after program execution.
    push_config : PushConfig
        The configuration of the PushInterpreter to use when executing the program.

    """

    arity = field(type=int, mandatory=True)
    output_stacks = field(type=list, mandatory=True)
    push_config = field(type=PushConfig, mandatory=True, initial=PushConfig())


class Program(Saveable, PRecord):
    """A Push program containing all information needed to run the code with consistent behavior.

    Attributes
    ----------
    code : CodeBlock
        The Push code expressing the logic of the program.
    signature : ProgramSignature
        The specification of the program and the configuration of the Push interpreter that it was evolved under.

    """

    code = field(type=CodeBlock, mandatory=True)
    signature = field(type=ProgramSignature, mandatory=True)
