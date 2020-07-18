from typing import Tuple, Union, List

from functools import partial
from pyrsistent import PVector, pvector

from pyshgp.push.type_library import PushTypeLibrary
from pyshgp.push.atoms import InstructionMeta, Literal
from pyshgp.push.state import PushState
from pyshgp.push.types import CORE_VECTOR_PUSH_TYPES, PushType
from pyshgp.push.instruction import (
    SimpleInstruction,
    StateToStateInstruction,
    ProducesManyOfTypeInstruction, Instruction
)
from pyshgp.utils import Token


def concat(v1: PVector, v2: PVector) -> Tuple[PVector]:
    return v1 + v2,


def conj(v1: PVector, el) -> Tuple[PVector]:
    return v1.append(el),


def take(v1: PVector, n: int) -> Tuple[PVector]:
    return v1[:n],


def subvec(v1: PVector, start: int, end: int) -> Tuple[PVector]:
    start, end = (start, end) if start <= end else (end, start)
    start = max(start, 0)
    end = min(end, len(v1))
    return v1[start:end],


def first(v1: PVector) -> Union[Token, Tuple]:
    if len(v1) == 0:
        return Token.revert
    return v1[0],


def last(v1: PVector) -> Union[Token, Tuple]:
    if len(v1) == 0:
        return Token.revert
    return v1[-1],


def nth(v1: PVector, idx: int) -> Union[Token, Tuple]:
    if len(v1) == 0:
        return Token.revert
    return v1[idx % len(v1)],


def rest(v1: PVector) -> Tuple[PVector]:
    return v1[1:],


def but_last(v1: PVector) -> Tuple[PVector]:
    return v1[:-1],


def length(v1: PVector) -> Tuple[int]:
    return len(v1),


def reverse(v1: PVector) -> Tuple[PVector]:
    return v1[::-1],


def push_all(v1: PVector) -> PVector:
    return v1[::-1]


def empty_vector(v1: PVector) -> Tuple[bool]:
    return len(v1) == 0,


def contains(v1: PVector, el) -> Tuple[bool]:
    return el in v1,


def index_of(v1: PVector, el) -> Tuple[int]:
    try:
        return v1.index(el),
    except ValueError:
        return -1,


def occurrences_of(v1: PVector, el) -> Tuple[int]:
    return sum([1 if i == el else 0 for i in v1]),


def set_nth(v1: PVector, idx: int, el) -> Tuple[PVector]:
    if len(v1) == 0:
        return v1,
    return v1.set(idx % len(v1), el),


def replace(v1: PVector, old, new) -> Tuple[PVector]:
    return pvector([new if el == old else el for el in v1]),


def replace_first(v1: PVector, old, new) -> Tuple[PVector]:
    try:
        idx = v1.index(old)
        return v1.set(idx, new),
    except ValueError:
        return v1,


def remove(v1: PVector, el) -> Tuple[PVector]:
    return pvector([i for i in v1 if i != el]),


def iterate(state: PushState, *, vec_type: PushType, el_type: PushType) -> Union[Token, PushState]:
    vec_type_name = vec_type.name
    el_type_name = el_type.name
    if state[vec_type_name].is_empty() or state["exec"].is_empty():
        return Token.revert
    vec = state[vec_type_name].pop()
    if len(vec) == 0:
        state["exec"].pop()
        return state
    elif len(vec) == 1:
        state[el_type_name].push(vec[0])
        return state
    else:
        top_exec = state["exec"].top()
        state["exec"].push(InstructionMeta(name=vec_type_name + "_iterate", code_blocks=1))
        state["exec"].push(Literal(value=vec_type.coerce(vec[1:]), push_type=vec_type))
        state["exec"].push(top_exec)
        state[el_type_name].push(vec[0])
        return state


def instructions(type_library: PushTypeLibrary):
    """Return all core numeric instructions."""
    i: List[Instruction] = []

    for push_type in set(CORE_VECTOR_PUSH_TYPES).intersection(set(type_library.values())):
        vec_type_name = push_type.name
        el_type_name = vec_type_name.replace("vector_", "")

        i.append(SimpleInstruction(
            vec_type_name + "_concat",
            concat,
            input_stacks=[vec_type_name, vec_type_name],
            output_stacks=[vec_type_name],
            code_blocks=0,
            docstring="Concatenates the top two {vt}.".format(vt=vec_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_conj",
            conj,
            input_stacks=[vec_type_name, el_type_name],
            output_stacks=[vec_type_name],
            code_blocks=0,
            docstring="Appends the top {et} to the top {vt}.".format(vt=vec_type_name, et=el_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_take",
            take,
            input_stacks=[vec_type_name, "int"],
            output_stacks=[vec_type_name],
            code_blocks=0,
            docstring="Creates a new {vt} from the first N elements of the top {vt}. N is top int.".format(vt=vec_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_subvec",
            subvec,
            input_stacks=[vec_type_name, "int", "int"],
            output_stacks=[vec_type_name],
            code_blocks=0,
            docstring="Creates a new {vt} from a slice of the top {vt}. Start and end indices are the top two ints.".format(vt=vec_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_first",
            first,
            input_stacks=[vec_type_name],
            output_stacks=[el_type_name],
            code_blocks=0,
            docstring="Takes the first element of the top {vt} and pushes it to the {et} stack.".format(vt=vec_type_name, et=el_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_last",
            last,
            input_stacks=[vec_type_name],
            output_stacks=[el_type_name],
            code_blocks=0,
            docstring="Takes the last element of the top {vt} and pushes it to the {et} stack.".format(vt=vec_type_name, et=el_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_nth",
            nth,
            input_stacks=[vec_type_name, "int"],
            output_stacks=[el_type_name],
            code_blocks=0,
            docstring="Takes the nth element of the top {vt} and pushes it to the {et} stack. N is the top int.".format(vt=vec_type_name, et=el_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_rest",
            rest,
            input_stacks=[vec_type_name],
            output_stacks=[vec_type_name],
            code_blocks=0,
            docstring="Drops the first element of the top {vt}.".format(vt=vec_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_but_last",
            but_last,
            input_stacks=[vec_type_name],
            output_stacks=[vec_type_name],
            code_blocks=0,
            docstring="Drops the last element of the top {vt}.".format(vt=vec_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_length",
            length,
            input_stacks=[vec_type_name],
            output_stacks=["int"],
            code_blocks=0,
            docstring="Pushes the length of the top {vt} to the int stack.".format(vt=vec_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_reverse",
            reverse,
            input_stacks=[vec_type_name],
            output_stacks=[vec_type_name],
            code_blocks=0,
            docstring="Reverses the top {vt}.".format(vt=vec_type_name)
        ))

        i.append(ProducesManyOfTypeInstruction(
            vec_type_name + "_push_all",
            push_all,
            input_stacks=[vec_type_name],
            output_stack=el_type_name,
            code_blocks=0,
            docstring="Pushes all elements of the top {vt} to the {et}.".format(vt=vec_type_name, et=el_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_empty_vector",
            empty_vector,
            input_stacks=[vec_type_name],
            output_stacks=["bool"],
            code_blocks=0,
            docstring="Pushes True to the bool stack if the top {vt} is empty. Pushes False otherwise.".format(vt=vec_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_contains",
            contains,
            input_stacks=[vec_type_name, el_type_name],
            output_stacks=["bool"],
            code_blocks=0,
            docstring="Pushes True to the bool stack if the top {et} is found in the top {vt}. Pushes False otherwise.".format(vt=vec_type_name, et=el_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_index_of",
            index_of,
            input_stacks=[vec_type_name, el_type_name],
            output_stacks=["int"],
            code_blocks=0,
            docstring="Pushes the index top {et} is top {vt} to int stack. Pushes -1 if not found.".format(vt=vec_type_name, et=el_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_occurrences_of",
            occurrences_of,
            input_stacks=[vec_type_name, el_type_name],
            output_stacks=["int"],
            code_blocks=0,
            docstring="Pushes the number of time the top {et} is found in the top {vt} to int stack.".format(vt=vec_type_name, et=el_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_set_nth",
            set_nth,
            input_stacks=[vec_type_name, "int", el_type_name],
            output_stacks=[vec_type_name],
            code_blocks=0,
            docstring="Sets the nth element of the top {vt} to be the top {et}. N is the top int.".format(vt=vec_type_name, et=el_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_replace",
            replace,
            input_stacks=[vec_type_name, el_type_name, el_type_name],
            output_stacks=[vec_type_name],
            code_blocks=0,
            docstring="Replaces all instances of the top {et} from the top {vt}.".format(vt=vec_type_name, et=el_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_replace_first",
            replace_first,
            input_stacks=[vec_type_name, el_type_name, el_type_name],
            output_stacks=[vec_type_name],
            code_blocks=0,
            docstring="Replaces the first instance of the top {et} from the top {vt}.".format(vt=vec_type_name, et=el_type_name)
        ))

        i.append(SimpleInstruction(
            vec_type_name + "_remove",
            remove,
            input_stacks=[vec_type_name, el_type_name],
            output_stacks=[vec_type_name],
            code_blocks=0,
            docstring="Removes all instances of the top {et} from the top {vt}.".format(vt=vec_type_name, et=el_type_name)
        ))

        i.append(StateToStateInstruction(
            vec_type_name + "_iterate",
            partial(iterate, vec_type=type_library[vec_type_name], el_type=type_library[el_type_name]),
            stacks_used=[vec_type_name, el_type_name, "exec"],
            code_blocks=1,
            docstring="Iterates over the top {vt} using the code on top of the exec stack.".format(vt=vec_type_name)
        ))

    return i
