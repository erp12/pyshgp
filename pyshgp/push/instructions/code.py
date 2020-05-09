"""Definitions for all core code instructions."""
from typing import Tuple, Union

from pyshgp.push.types import PushInt
from pyshgp.push.instruction import (
    SimpleInstruction,
    StateToStateInstruction
)
from pyshgp.push.instructions.common import _revert, _wrap_tuple, _dup
from pyshgp.push.atoms import Atom, InstructionMeta, CodeBlock, Literal
from pyshgp.push.state import PushState
from pyshgp.utils import Token


def _is_code_block(x) -> Tuple[bool]:
    return isinstance(x, CodeBlock),


def _is_singular(x) -> Tuple[bool]:
    return not isinstance(x, CodeBlock),


def _code_length(x) -> Tuple[int]:
    if isinstance(x, CodeBlock):
        return len(x),
    return 1,


def _code_first(x) -> Tuple[Atom]:
    if isinstance(x, CodeBlock) and len(x) > 1:
        return x[0],
    return Token.revert


def _code_last(x) -> Tuple[Atom]:
    if isinstance(x, CodeBlock) and len(x) > 1:
        return x[-1],
    return Token.revert


def _code_rest(x) -> Tuple[Atom]:
    if isinstance(x, CodeBlock) and len(x) > 1:
        return CodeBlock(x[1:]),
    return Token.revert


def _code_but_last(x) -> Tuple[Atom]:
    if isinstance(x, CodeBlock) and len(x) > 1:
        return CodeBlock(x[:-1]),
    return Token.revert


def _wrap_code_block(*args):
    return CodeBlock(args),


def _code_combine(a: Atom, b: Atom) -> Tuple[CodeBlock]:
    if isinstance(a, CodeBlock) and isinstance(b, CodeBlock):
        return CodeBlock(b + a),
    elif isinstance(b, CodeBlock):
        return b.append(a),
    elif isinstance(a, CodeBlock):
        return a.append(b),
    else:
        return CodeBlock([a, b]),


def _code_do_then_pop(state: PushState) -> Union[Token, PushState]:
    if state["code"].is_empty():
        return Token.revert
    c = state["code"].top()
    state["exec"].push(InstructionMeta(name="code_pop", code_blocks=0))
    state["exec"].push(c)
    return state


def _code_do_range(state: PushState) -> Union[Token, PushState]:
    if state["code"].is_empty() or len(state["int"]) < 2:
        return Token.revert
    to_do = state["code"].pop()
    destintaiton_ndx = state["int"].pop()
    current_ndx = state["int"].pop()

    increment = 0
    if current_ndx < destintaiton_ndx:
        increment = 1
    elif current_ndx > destintaiton_ndx:
        increment = -1

    if not increment == 0:
        state["exec"].push(CodeBlock([
            Literal(value=current_ndx + increment, push_type=PushInt),
            Literal(value=destintaiton_ndx, push_type=PushInt),
            InstructionMeta(name="code_from_exec", code_blocks=1),
            to_do,
            InstructionMeta(name="code_do_range", code_blocks=0)
        ]))
    state["int"].push(current_ndx)
    state["exec"].push(to_do)
    return state


def _exec_do_range(state: PushState) -> Union[Token, PushState]:
    if state["exec"].is_empty() or len(state["int"]) < 2:
        return Token.revert
    to_do = state["exec"].pop()
    destination_ndx = state["int"].pop()
    current_ndx = state["int"].pop()

    increment = 0
    if current_ndx < destination_ndx:
        increment = 1
    elif current_ndx > destination_ndx:
        increment = -1

    if not increment == 0:
        state["exec"].push(CodeBlock([
            Literal(value=current_ndx + increment, push_type=PushInt),
            Literal(value=destination_ndx, push_type=PushInt),
            InstructionMeta(name="exec_do_range", code_blocks=1),
            to_do
        ]))
    state["int"].push(current_ndx)
    state["exec"].push(to_do)
    return state


def _code_do_count(state: PushState) -> Union[Token, PushState]:
    if state["code"].is_empty() or state["int"].is_empty():
        return Token.revert
    if state["int"].top() < 1:
        return Token.revert
    code = state["code"].pop()
    count = state["int"].pop()
    state["exec"].push(CodeBlock([
        Literal(value=0, push_type=PushInt),
        Literal(value=count - 1, push_type=PushInt),
        InstructionMeta(name="code_from_exec", code_blocks=1),
        code,
        InstructionMeta(name="code_do_range", code_blocks=0)
    ]))
    return state


def _exec_do_count(state: PushState) -> Union[Token, PushState]:
    if state["exec"].is_empty() or state["int"].is_empty():
        return Token.revert
    if state["int"].top() < 1:
        return Token.revert
    code = state["exec"].pop()
    count = state["int"].pop()
    state["exec"].push(CodeBlock([
        Literal(value=0, push_type=PushInt),
        Literal(value=count - 1, push_type=PushInt),
        InstructionMeta(name="exec_do_range", code_blocks=1),
        code
    ]))
    return state


def _code_do_times(state: PushState) -> PushState:
    if state["code"].is_empty() or state["int"].is_empty():
        return Token.revert
    if state["int"].top() < 1:
        return Token.revert
    code = state["code"].pop()
    times = state["int"].pop()
    state["exec"].push(CodeBlock([
        Literal(value=0, push_type=PushInt),
        Literal(value=times - 1, push_type=PushInt),
        InstructionMeta(name="code_from_exec", code_blocks=1),
        CodeBlock([
            InstructionMeta(name="int_pop", code_blocks=0),
            code,
        ]),
        InstructionMeta(name="code_do_range", code_blocks=0)
    ]))
    return state


def _exec_do_times(state: PushState) -> Union[Token, PushState]:
    if state["exec"].is_empty() or state["int"].is_empty():
        return Token.revert
    if state["int"].top() < 1:
        return Token.revert
    code = state["exec"].pop()
    times = state["int"].pop()
    state["exec"].push(CodeBlock([
        Literal(value=0, push_type=PushInt),
        Literal(value=times - 1, push_type=PushInt),
        InstructionMeta(name="exec_do_range", code_blocks=1),
        CodeBlock([
            InstructionMeta(name="int_pop", code_blocks=0),
            code,
        ])
    ]))
    return state


def _exec_while(state: PushState) -> Union[Token, PushState]:
    if state["exec"].is_empty():
        return Token.revert
    if state["bool"].is_empty():
        state["exec"].pop()
        return state
    code = state["exec"].top()
    if state["bool"].pop():
        state["exec"].push(InstructionMeta(name="exec_while", code_blocks=1))
        state["exec"].push(code)
    else:
        state["exec"].pop()
    return state


def _exec_do_while(state: PushState) -> PushState:
    if state["exec"].is_empty():
        return Token.revert
    code = state["exec"].top()
    state["exec"].push(InstructionMeta(name="exec_while", code_blocks=1))
    state["exec"].push(code)
    return state


def _code_map(state: PushState) -> PushState:
    if state["exec"].is_empty() or state["code"].is_empty():
        return Token.revert
    e = state["exec"].pop()
    c = state["code"].pop()
    if not isinstance(c, CodeBlock):
        c = CodeBlock([c])
    l1 = [CodeBlock([InstructionMeta(name="code_from_exec", code_blocks=1), item, e]) for item in c]
    l2 = [InstructionMeta(name="code_combine", code_blocks=0) for _ in c[1:]]
    contents = l1 + [InstructionMeta(name="code_wrap", code_blocks=0)] + l2
    state["exec"].push(CodeBlock(contents))
    return state


def _if(b, _then, _else):
    return _then if b else _else,


def _code_when(state: PushState) -> PushState:
    if state["code"].is_empty() or state["bool"].is_empty():
        return Token.revert
    code = state["code"].pop()
    if state["bool"].pop():
        state["exec"].push(code)
    return state


def _exec_when(state: PushState) -> PushState:
    if state["exec"].is_empty() or state["bool"].is_empty():
        return Token.revert
    if not state["bool"].pop():
        state["exec"].pop()
    return state


def _code_member(code: Atom, item: Atom) -> Tuple[bool]:
    if not isinstance(code, CodeBlock):
        code = CodeBlock([code])
    return item in code,


def _code_nth(code: Atom, ndx: int) -> Tuple[Atom]:
    if not isinstance(code, CodeBlock):
        code = CodeBlock([code])
    if len(code) == 0:
        return Token.revert
    ndx = abs(ndx) % len(code)
    return code[ndx],


def _make_empty_code_block() -> Tuple[Atom]:
    return CodeBlock(),


def _is_empty_code_block(code: Atom) -> Tuple[bool]:
    return isinstance(code, CodeBlock) and len(code) == 0,


def _code_size(code: Atom) -> Tuple[int]:
    if not isinstance(code, CodeBlock):
        return 1,
    return code.size(),


def _code_extract(code: Atom, ndx: int) -> Union[Token, Tuple[Atom]]:
    if isinstance(code, CodeBlock) and code.size() == 0:
        return Token.revert
    if not isinstance(code, CodeBlock):
        return code,
    ndx = abs(ndx % code.size())
    return code.code_at_point(ndx),


def _code_insert(code1, code2, ndx) -> Union[Token, Tuple[Atom]]:
    if not isinstance(code1, CodeBlock):
        code1 = CodeBlock([code1])
    if code1.size() == 0:
        return code1.append(code2),
    ndx = abs(ndx) % code1.size()
    return code1.with_code_inserted_at_point(code2, ndx),


def _code_first_position(code1, code2) -> Union[Token, Tuple[int]]:
    if (not isinstance(code1, CodeBlock)) or (len(code1) == 0):
        if code1 == code2:
            return 0,
    else:
        for ndx, el in enumerate(code1):
            if el == code2:
                return ndx,
    return -1,


def _code_reverse(code):
    if not isinstance(code, CodeBlock):
        return code,
    return CodeBlock(code[::-1]),


def instructions():
    """Return all core code SimpleInstructions."""
    i = []

    i.append(SimpleInstruction(
        "noop",
        _revert,
        input_stacks=[],
        output_stacks=[],
        code_blocks=0,
        docstring="A noop SimpleInstruction which does nothing."
    ))

    i.append(SimpleInstruction(
        "noop_open",
        _revert,
        input_stacks=[],
        output_stacks=[],
        code_blocks=1,
        docstring="A noop SimpleInstruction which does nothing. Opens a code block."
    ))

    i.append(SimpleInstruction(
        "code_is_code_block",
        _is_code_block,
        input_stacks=["code"],
        output_stacks=["bool"],
        code_blocks=0,
        docstring="Push True if top item on code stack is a CodeBlock. False otherwise."
    ))

    i.append(SimpleInstruction(
        "code_is_singular",
        _is_singular,
        input_stacks=["code"],
        output_stacks=["bool"],
        code_blocks=0,
        docstring="Push True if top item on code stack is a not CodeBlock. False otherwise."
    ))

    i.append(SimpleInstruction(
        "code_length",
        _code_length,
        input_stacks=["code"],
        output_stacks=["int"],
        code_blocks=0,
        docstring="If the top code item is a CodeBlock, pushes its length, otherwise pushes 1."
    ))

    i.append(SimpleInstruction(
        "code_first",
        _code_first,
        input_stacks=["code"],
        output_stacks=["code"],
        code_blocks=0,
        docstring="If the top code item is a CodeBlock, pushes its first element."
    ))

    i.append(SimpleInstruction(
        "code_last",
        _code_first,
        input_stacks=["code"],
        output_stacks=["code"],
        code_blocks=0,
        docstring="If the top code item is a CodeBlock, pushes its last element."
    ))

    i.append(SimpleInstruction(
        "code_rest",
        _code_rest,
        input_stacks=["code"],
        output_stacks=["code"],
        code_blocks=0,
        docstring="If the top code item is a CodeBlock, pushes it to the code stack without its first element."
    ))

    i.append(SimpleInstruction(
        "code_but_last",
        _code_but_last,
        input_stacks=["code"],
        output_stacks=["code"],
        code_blocks=0,
        docstring="If the top code item is a CodeBlock, pushes it to the code stack without its last element."
    ))

    i.append(SimpleInstruction(
        "code_wrap",
        _wrap_code_block,
        input_stacks=["code"],
        output_stacks=["code"],
        code_blocks=0,
        docstring="Wraps the top item on the code stack in a CodeBlock."
    ))

    i.append(SimpleInstruction(
        "code_list",
        _wrap_code_block,
        input_stacks=["code", "code"],
        output_stacks=["code"],
        code_blocks=0,
        docstring="Wraps the top two items on the code stack in a CodeBlock."
    ))

    i.append(SimpleInstruction(
        "code_combine",
        _code_combine,
        input_stacks=["code", "code"],
        output_stacks=["code"],
        code_blocks=0,
        docstring="""Combines the top two items on the code stack in a CodeBlock.
        If one items is a CodeBlock, the other item is appended to it. If both
        items are CodeBlocks, they are concatenated together."""
    ))

    i.append(SimpleInstruction(
        "code_do",
        _wrap_tuple,
        input_stacks=["code"],
        output_stacks=["exec"],
        code_blocks=0,
        docstring="Moves the top element of the code stack to the exec stack for execution."
    ))

    i.append(SimpleInstruction(
        "code_do_dup",
        _dup,
        input_stacks=["code"],
        output_stacks=["exec", "code"],
        code_blocks=0,
        docstring="Copies the top element of the code stack to the exec stack for execution."
    ))

    i.append(StateToStateInstruction(
        "code_do_then_pop",
        _code_do_then_pop,
        stacks_used=["exec", "code"],
        code_blocks=0,
        docstring="""Pushes a `code_pop` InstructionMeta and the top item of the
        code stack to the exec stack. Result is the top code item executing before
        it is removed from the code stack."""
    ))

    i.append(StateToStateInstruction(
        "code_do_range",
        _code_do_range,
        stacks_used=["exec", "code", "int"],
        code_blocks=0,
        docstring="""Evaluates the top item on the code stack for each step along
        the range `i` to `j`. Both `i` and `j` are taken from the int stack."""
    ))

    i.append(StateToStateInstruction(
        "exec_do_range",
        _exec_do_range,
        stacks_used=["exec", "int"],
        code_blocks=1,
        docstring="""Evaluates the top item on the exec stack for each step along
        the range `i` to `j`. Both `i` and `j` are taken from the int stack.
        Differs from code_do_range only in the source of the code and the
        recursive call."""
    ))

    i.append(StateToStateInstruction(
        "code_do_count",
        _code_do_count,
        stacks_used=["exec", "code", "int"],
        code_blocks=0,
        docstring="""Evaluates the top item on the code stack `n` times, where
        `n` comes from the `n` comes from the top of the int stack."""
    ))

    i.append(StateToStateInstruction(
        "exec_do_count",
        _exec_do_count,
        stacks_used=["exec", "int"],
        code_blocks=1,
        docstring="""Evaluates the top item on the exec stack `n` times, where
        `n` comes from the `n` comes from the top of the int stack. Differs from
        code.do*count only in the source of the code and the recursive call."""
    ))

    i.append(StateToStateInstruction(
        "code_do_times",
        _code_do_times,
        stacks_used=["exec", "code", "int"],
        code_blocks=0,
        docstring="""Evaluates the top item on the code stack `n` times, where
        `n` comes from the `n` comes from the top of the int stack."""
    ))

    i.append(StateToStateInstruction(
        "exec_do_times",
        _exec_do_times,
        stacks_used=["exec", "code", "int"],
        code_blocks=1,
        docstring="""Evaluates the top item on the code stack `n` times, where
        `n` comes from the `n` comes from the top of the int stack."""
    ))

    i.append(StateToStateInstruction(
        "exec_while",
        _exec_while,
        stacks_used=["exec", "bool"],
        code_blocks=1,
        docstring="""Evaluates the top item on the exec stack repeated until the top
        bool is no longer True."""
    ))

    i.append(StateToStateInstruction(
        "exec_do_while",
        _exec_do_while,
        stacks_used=["exec", "bool"],
        code_blocks=1,
        docstring="""Evaluates the top item on the exec stack repeated until the top
        bool is no longer True."""
    ))

    i.append(StateToStateInstruction(
        "code_map",
        _code_map,
        stacks_used=["exec", "code"],
        code_blocks=0,
        docstring="""Evaluates the top item on the exec stack for each element of the top
        CodeBlock on the code stack. If the top code item is not a CodeBlock, it is wrapped
        into one."""
    ))

    i.append(SimpleInstruction(
        "code_if",
        _if,
        input_stacks=["bool", "code", "code"],
        output_stacks=["exec"],
        code_blocks=0,
        docstring="""If the top boolean is true, execute the top element of the code
        stack and skip the second. Otherwise, skip the top element of the
        code stack and execute the second."""
    ))

    i.append(SimpleInstruction(
        "exec_if",
        _if,
        input_stacks=["bool", "exec", "exec"],
        output_stacks=["exec"],
        code_blocks=2,
        docstring="""If the top boolean is true, execute the top element of the exec
        stack and skip the second. Otherwise, skip the top element of the
        exec stack and execute the second."""
    ))

    i.append(StateToStateInstruction(
        "code_when",
        _code_when,
        stacks_used=["exec", "code", "bool"],
        code_blocks=0,
        docstring="""Evalutates the top code item if the top bool is True.
        Otherwise the top code is popped."""
    ))

    i.append(StateToStateInstruction(
        "exec_when",
        _exec_when,
        stacks_used=["exec", "bool"],
        code_blocks=1,
        docstring="""Pops the next item on the exec stack without evaluating it
        if the top bool is False. Otherwise, has no effect."""
    ))

    i.append(SimpleInstruction(
        "code_member",
        _code_member,
        input_stacks=["code", "code"],
        output_stacks=["bool"],
        code_blocks=0,
        docstring="""Pushes True if the second code item is a found within the top code item.
        If the top code item is not a CodeBlock, it is wrapped."""
    ))

    i.append(SimpleInstruction(
        "code_nth",
        _code_nth,
        input_stacks=["code", "int"],
        output_stacks=["code"],
        code_blocks=0,
        docstring="""Pushes nth item of the top element on the code stack. If
        the top item is not a CodeBlock it is wrapped in a CodeBlock."""
    ))

    i.append(SimpleInstruction(
        "make_empty_code_block",
        _make_empty_code_block,
        input_stacks=[],
        output_stacks=["code"],
        code_blocks=0,
        docstring="""Pushes an empty CodeBlock to the code stack."""
    ))

    i.append(SimpleInstruction(
        "is_empty_code_block",
        _is_empty_code_block,
        input_stacks=["code"],
        output_stacks=["bool"],
        code_blocks=0,
        docstring="""Pushes true if top code item is an empty CodeBlock. Pushes
        false otherwise."""
    ))

    i.append(SimpleInstruction(
        "code_size",
        _code_size,
        input_stacks=["code"],
        output_stacks=["int"],
        code_blocks=0,
        docstring="""Pushes the total size of the top item on the code stack. If
        the top item is a CodeBlock, this includes the size of all the CodeBlock's
        elements recusively."""
    ))

    i.append(SimpleInstruction(
        "code_extract",
        _code_extract,
        input_stacks=["code", "int"],
        output_stacks=["code"],
        code_blocks=0,
        docstring="""Traverses the top code item depth first and returns the nth
        item based on the top int."""
    ))

    i.append(SimpleInstruction(
        "code_insert",
        _code_insert,
        input_stacks=["code", "code", "int"],
        output_stacks=["code"],
        code_blocks=0,
        docstring="""Traverses the top code item depth first and inserts the
        second code item at position `n`. The value of `n` is the top int."""
    ))

    # code_subst
    # code_contains
    # code_container

    i.append(SimpleInstruction(
        "code_first_position",
        _code_first_position,
        input_stacks=["code", "code"],
        output_stacks=["int"],
        code_blocks=0,
        docstring="""Pushes the first position of the second code item within
        the top code item. If not found, pushes -1. If the top code item is not
        a CodeBlock, this instruction returns 0 if the top two code elements are
        equal and -1 otherwise."""
    ))

    i.append(SimpleInstruction(
        "code_reverse",
        _code_reverse,
        input_stacks=["code"],
        output_stacks=["code"],
        code_blocks=0,
        docstring="""Pushes the top code item reversed. No effect if top code
        item is not a CodeBlock."""
    ))

    return i
