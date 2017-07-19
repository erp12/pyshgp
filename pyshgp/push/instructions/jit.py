"""
The :mod:`jit` module provides a class which defines the "just-in-time
instructions" which can be used in instruction definitions to retrieve other
instructions.
"""

from ...exceptions import UnknownInstructionName
from ..instruction import PyshInstruction

class JustInTimeInstruction(PyshInstruction):
    """A callable object that, when processed in by the push interpreter,
    returns a specific registered instruction.

    Use of these instructions is only needed when defining new Push
    instructions that must call themselves, or other situations where a Push
    instruction must be defined in a way that creates an instance of another
    Push instruction that is not yet registered.

    Parameters
    ----------
    instruction_name : str
         The name of the instruction to look-up and run when this JiT
         instruction is called.
    """

    def __init__(self, instruction_name):
        self.name = instruction_name

    def __call__(self):
        """
        When the JiT instruction is called, it returns the registered
        instruction by the same name.
        """
        from ..registered_instructions import get_instruction
        return get_instruction(self.name)

    def __repr__(self):
        return self.name + "_JIT"
