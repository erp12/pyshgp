"""Definitions for all core text instructions."""
from pyshgp.push.instruction import SimpleInstruction, ProducesManyOfTypeInstruction
from pyshgp.push.types import Char
from pyshgp.utils import Token


def _concat(a, b):
    return str(b) + str(a),


def _first_char(s):
    if len(s) == 0:
        return Token.revert
    return s[0],


def _last_char(s):
    if len(s) == 0:
        return Token.revert
    return s[-1],


def _nth_char(s, ndx):
    if len(s) == 0:
        return Token.revert
    return s[ndx % len(s)],


def _contains(s, x):
    return x in s,


def _p_index(s, substr):
    try:
        return s.index(substr),
    except ValueError:
        return -1,


def _head(s, i):
    if len(s) == 0:
        return "",
    return s[:i % len(s)],


def _tail(s, i):
    if len(s) == 0:
        return "",
    return s[i % len(s):],


def _rest(s):
    if len(s) < 2:
        return "",
    return s[1:],


def _but_last(s):
    if len(s) < 2:
        return "",
    return s[:-1],


def _drop(s, i):
    if len(s) == 0:
        return "",
    return s[i % len(s):],


def _but_last_n(s, i):
    if len(s) == 0:
        return "",
    return s[:-(i % len(s))],


def _split_on(s, x):
    if x == "":
        return []
    return s.split(x)


def _replace_n(s, old, new, n=1):
    return s.replace(str(old), str(new), n),


def _replace_all(s, old, new):
    return s.replace(str(old), str(new)),


def _remove_n(s, x, n=1):
    return _replace_n(s, x, "", n)


def _remove_all(s, x):
    return _replace_all(s, x, "")


def _len(s):
    return len(s),


def _reverse(s):
    return s[::-1],


def _make_empty():
    return "",


def _is_empty(s):
    return s == "",


def _occurrences_of(s, x):
    return s.count(str(x)),


def _remove_nth(s, ndx):
    return s[:ndx] + s[ndx + 1:],


def _set_nth(s, c, ndx):
    return s[:ndx] + str(c) + s[ndx + 1:],


def _insert(s, x, ndx):
    return s[:ndx] + str(x) + s[ndx:],


def _strip_whitespace(s):
    return s.strip(),


# @TODO: Implement exec_string_iterate instruction.


def _is_whitespace(c):
    return str(c).isspace(),


def _is_letter(c):
    return str(c).isalpha(),


def _is_digit(c):
    return str(c).isdigit(),


def _str_from_thing(thing):
    return str(thing),


def _char_from_bool(b):
    if b:
        return Char("T"),
    return Char("F"),


def _char_from_ascii(i):
    return Char(chr(i % 128)),


def _char_from_float(f):
    return _char_from_ascii(int(f))


def _all_chars(s):
    return [Char(c) for c in list(s)[::-1]]


def instructions():
    """Return all core text instructions."""
    i = []

    for push_type in ["str", "char"]:

        i.append(SimpleInstruction(
            "{t}_concat".format(t=push_type),
            _concat,
            input_types=[push_type, push_type],
            output_types=["str"],
            code_blocks=0,
            docstring="Concatenates the top two {t}s and pushes the resulting string.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "str_insert_{t}".format(t=push_type),
            _insert,
            input_types=["str", push_type, "int"],
            output_types=["str"],
            code_blocks=0,
            docstring="""Inserts {t} into the top str at index `n` and pushes
            the resulting string. The value for `n` is taken from the int stack.""".format(t=push_type)
        ))

        # Getting Characters

        i.append(SimpleInstruction(
            "{t}_from_first_char".format(t=push_type),
            _first_char,
            input_types=["str"],
            output_types=[push_type],
            code_blocks=0,
            docstring="Pushes a {t} of the first character of the top string.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_from_last_char".format(t=push_type),
            _last_char,
            input_types=["str"],
            output_types=[push_type],
            code_blocks=0,
            docstring="Pushes a {t} of the last character of the top string.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_from_nth_char".format(t=push_type),
            _nth_char,
            input_types=["str", "int"],
            output_types=[push_type],
            code_blocks=0,
            docstring="Pushes a {t} of the nth character of the top string. The top integer denotes nth position.".format(t=push_type)
        ))

        # Checking string contents

        i.append(SimpleInstruction(
            "str_contains_{t}".format(t=push_type),
            _contains,
            input_types=["str", push_type],
            output_types=["bool"],
            code_blocks=0,
            docstring="Pushes true if the next {t} is in the top string. Pushes false otherwise.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "str_index_of_{t}".format(t=push_type),
            _p_index,
            input_types=["str", push_type],
            output_types=["int"],
            code_blocks=0,
            docstring="Pushes the index of the next {t} in the top string. If not found, pushes -1.".format(t=push_type)
        ))

        # Splitting

        # @TODO: srt_split_on_space

        i.append(ProducesManyOfTypeInstruction(
            "str_split_on_{t}".format(t=push_type),
            _split_on,
            input_types=["str", push_type],
            output_type="str",
            code_blocks=0,
            docstring="Pushes multiple strs produced by splitting the top str on the top {t}.".format(t=push_type)
        ))

        # Replacements

        i.append(SimpleInstruction(
            "str_replace_first_{t}".format(t=push_type),
            _replace_n,
            input_types=["str", push_type, push_type],
            output_types=["str"],
            code_blocks=0,
            docstring="""Pushes the str produced by replaceing the first occurrence of the
            top {t} with the second {t}.""".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "str_replace_n_{t}".format(t=push_type),
            _replace_n,
            input_types=["str", push_type, push_type, "int"],
            output_types=["str"],
            code_blocks=0,
            docstring="""Pushes the str produced by replaceing the first `n` occurrences of the
            top {t} with the second {t}. The value for `n` is the top int.""".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "str_replace_all_{t}".format(t=push_type),
            _replace_all,
            input_types=["str", push_type, push_type],
            output_types=["str"],
            code_blocks=0,
            docstring="""Pushes the str produced by replaceing all occurrences of the
            top {t} with the second {t}.""".format(t=push_type)
        ))

        # Removals

        i.append(SimpleInstruction(
            "str_remove_first_{t}".format(t=push_type),
            _remove_n,
            input_types=["str", push_type],
            output_types=["str"],
            code_blocks=0,
            docstring="Pushes the str produced by removing the first occurrence of the top {t}.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "str_remove_n_{t}".format(t=push_type),
            _remove_n,
            input_types=["str", push_type, "int"],
            output_types=["str"],
            code_blocks=0,
            docstring="""Pushes the str produced by remvoing the first `n` occurrences of the
            top {t}. The value for `n` is the top int.""".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "str_remove_all_{t}".format(t=push_type),
            _remove_all,
            input_types=["str", push_type],
            output_types=["str"],
            code_blocks=0,
            docstring="Pushes the str produced by removing all occurrences of the top {t}.".format(t=push_type)
        ))

        # Misc

        i.append(SimpleInstruction(
            "str_occurrences_of_{t}".format(t=push_type),
            _occurrences_of,
            input_types=["str", push_type],
            output_types=["int"],
            code_blocks=0,
            docstring="Pushes the number of times the top {t} occurs in the top str to the int stack.".format(t=push_type)
        ))

    i.append(SimpleInstruction(
        "str_reverse",
        _reverse,
        input_types=["str"],
        output_types=["str"],
        code_blocks=0,
        docstring="""Takes the top string and pushes it reversed."""
    ))

    i.append(SimpleInstruction(
        "str_head",
        _head,
        input_types=["str", "int"],
        output_types=["str"],
        code_blocks=0,
        docstring="""Pushes a string of the first `n` characters from the top string. The value
        for `n` is the top int mod the length of the string."""
    ))

    i.append(SimpleInstruction(
        "str_tail",
        _tail,
        input_types=["str", "int"],
        output_types=["str"],
        code_blocks=0,
        docstring="""Pushes a string of the last `n` characters from the top string. The value
        for `n` is the top int mod the length of the string."""
    ))

    i.append(SimpleInstruction(
        "str_append_char",
        _concat,
        input_types=["str", "char"],
        output_types=["str"],
        code_blocks=0,
        docstring="Appends the top char to the top string pushes the resulting string."
    ))

    i.append(SimpleInstruction(
        "str_rest",
        _rest,
        input_types=["str"],
        output_types=["str"],
        code_blocks=0,
        docstring="Pushes the top str without its first character."
    ))

    i.append(SimpleInstruction(
        "str_but_last",
        _but_last,
        input_types=["str"],
        output_types=["str"],
        code_blocks=0,
        docstring="Pushes the top str without its last character."
    ))

    i.append(SimpleInstruction(
        "str_drop",
        _drop,
        input_types=["str", "int"],
        output_types=["str"],
        code_blocks=0,
        docstring="""Pushes the top str without its first `n` character. The value for `n`
        is the top int mod the length of the string."""
    ))

    i.append(SimpleInstruction(
        "str_but_last_n",
        _but_last_n,
        input_types=["str", "int"],
        output_types=["str"],
        code_blocks=0,
        docstring="""Pushes the top str without its last `n` character. The value for `n`
        is the top int mod the length of the string."""
    ))

    i.append(SimpleInstruction(
        "str_length",
        _len,
        input_types=["str"],
        output_types=["int"],
        code_blocks=0,
        docstring="Pushes the length of the top str to the int stack."
    ))

    i.append(SimpleInstruction(
        "str_make_empty",
        _make_empty,
        input_types=[],
        output_types=["str"],
        code_blocks=0,
        docstring="Pushes an empty string."
    ))

    i.append(SimpleInstruction(
        "str_is_empty_string",
        _is_empty,
        input_types=["str"],
        output_types=["bool"],
        code_blocks=0,
        docstring="Pushes True if top string is empty. Pushes False otherwise."
    ))

    i.append(SimpleInstruction(
        "str_remove_nth",
        _remove_nth,
        input_types=["str", "int"],
        output_types=["str"],
        code_blocks=0,
        docstring="Pushes the top str with the nth character removed."
    ))

    i.append(SimpleInstruction(
        "str_set_nth",
        _set_nth,
        input_types=["str", "char", "int"],
        output_types=["str"],
        code_blocks=0,
        docstring="Pushes the top str with the nth character set to the top character."
    ))

    i.append(SimpleInstruction(
        "str_strip_whitespace",
        _strip_whitespace,
        input_types=["str"],
        output_types=["str"],
        code_blocks=0,
        docstring="Pushes the top str with trailing and leading whitespace stripped."
    ))

    # @TODO: Instructions for trim_left and trim_right
    # @TODO: Instructions for pad_left and pad_right

    #  CHARACTER INSTRUCTIONS

    i.append(SimpleInstruction(
        "char_is_whitespace",
        _is_whitespace,
        input_types=["char"],
        output_types=["bool"],
        code_blocks=0,
        docstring="Pushes True if the top Char is whitespace. Pushes False otherwise."
    ))

    i.append(SimpleInstruction(
        "char_is_letter",
        _is_letter,
        input_types=["char"],
        output_types=["bool"],
        code_blocks=0,
        docstring="Pushes True if the top Char is a letter. Pushes False otherwise."
    ))

    i.append(SimpleInstruction(
        "char_is_digit",
        _is_digit,
        input_types=["char"],
        output_types=["bool"],
        code_blocks=0,
        docstring="Pushes True if the top Char is a numeric digit. Pushes False otherwise."
    ))

    #  TYPE CONVERTING

    for push_type in ["bool", "int", "float", "char"]:
        i.append(SimpleInstruction(
            "str_from_{t}".format(t=push_type),
            _str_from_thing,
            input_types=[push_type],
            output_types=["str"],
            code_blocks=0,
            docstring="Pushes the top {t} converted into a str.".format(t=push_type)
        ))

    i.append(SimpleInstruction(
        "char_from_bool",
        _char_from_bool,
        input_types=["bool"],
        output_types=["char"],
        code_blocks=0,
        docstring="""Pushes the char \"T\" if the top bool is True. If the top
        bool is False, pushes the char \"F\"."""
    ))

    i.append(SimpleInstruction(
        "char_from_ascii_int",
        _char_from_ascii,
        input_types=["int"],
        output_types=["char"],
        code_blocks=0,
        docstring="Pushes the top int converted into a Character by using the int mod 128 as an ascii value."
    ))

    i.append(SimpleInstruction(
        "_char_from_float",
        _char_from_float,
        input_types=["float"],
        output_types=["char"],
        code_blocks=0,
        docstring="""Pushes the top float converted into a Character by flooring
        the float to an int, taking the int mod 128, and using it as an ascii value."""
    ))

    i.append(ProducesManyOfTypeInstruction(
        "chars_from_str",
        _all_chars,
        input_types=["str"],
        output_type="char",
        code_blocks=0,
        docstring="""Pushes each character of the top str to the char stack in reverse order."""
    ))

    return i
