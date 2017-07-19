"""
The :mod:`registered_instructions` module provides functions to retreive
instructions from the set of instructions supported by ``pyshgp``.
"""

from ..utils import recognize_pysh_type, is_str_type
from ..exceptions import UnknownInstructionName

from .instructions import all_instructions

instruction_set = {i.name: i for i in all_instructions}

def get_instruction(name):
    """Returns a registered instruction by its name.

    Parameters
    ----------
    name : str
        Name of instruction to return.

    Returns
    -------
    A PushInstruction with ``name``, or throws UnknownInstructionName.
    """
    if name in instruction_set.keys():
        return instruction_set[name]
    else:
        raise UnknownInstructionName(name)


def get_instructions_by_pysh_type(pysh_type):
    """Returns list of instructions that deal with the given pysh_type

    Parameters
    ----------
    pysh_type : str
        Pysh type string (ie ``'_integer'``) to filter by.

    Returns
    -------
    List of PushInstruction objects that are associated with ``pysh_type``.
    """
    return [i for i in all_instructions if pysh_type in i.stack_types]


def load_program_from_list(lst):
    """Loads a program from a list, and checks each string in list for an
    instruction with the same name.

    .. warning::
        This function will attempt to look up all strings in the registered
        instructions to see if an instruction with a matching name exists.
        This limits you to only using strings that are not exact matches of
        instruction names. This is mitigated by the fact that all instruction
        names begin with a ``'_'``.

    :param list lst: List that should be translated into a Push program.
    :returns: List that can be executed as a Push program.
    """
    program = []
    for el in lst:
        # For each element in the list
        pysh_type = recognize_pysh_type(el)
        if pysh_type in ['_integer', '_float', '_boolean', '_char', '_vector']:
            # If ``el`` is an int, float, bool, Character object or PushVector
            # object simply append to the program because these are push
            # literals.
            program.append(el)
        elif pysh_type == '_instruction':
            # If ``el`` an instance of any of the instruction types, append to
            # the program.
            program.append(el)
        elif is_str_type(el):
            # If ``el`` is a string:
            el = str(el)
            # Attempt to find an instruction with ``el`` as its name.
            matching_instruction = None
            try:
                matching_instruction = get_instruction(el)
            except UnknownInstructionName(el):
                pass
            # If matching_instruction is None, it must be a ssring literal.
            if matching_instruction is None:
                program.append(el)
            else:
                program.append(matching_instruction)
        elif pysh_type == '_list':
            # If ``el`` is a list (but not PushVector) turn it into a program
            # and append it to (aka. nest it in) the program.
            program.append(load_program_from_list(el))
    return program
