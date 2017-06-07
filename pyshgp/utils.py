# -*- coding: utf-8 -*-
"""
The :mod:`utils` module provides classes and functions that are used throughout
the push interpreter and GP modules.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys, random, math
import numpy as np

from . import exceptions as e
from .push import instruction as instr
from . import constants as c


##             ##
# Utility Types #
##             ##

class Character(object):
    '''Holds a string of length 1.

    Used to distinguish between string and char literals
    in Push program interpretation.

    :attributes: :attr:`char` - String of length 1.
    '''
    def __init__(self, char):
        if len(char) == 0:
            raise e.EmptyCharacterException()
        if len(char) > 1:
            raise e.LongCharacterException()
        self.char = char

    def __repr__(self):
        if self.char == '\n':
          return 'c_newline'
        if self.char == ' ':
          return 'c_space'
        return "c_" + self.char

    def __eq__(self, other):
        if isinstance(other, Character):
          return self.char == other.char
        return False

class PushVector(list):
    '''List where elements are all of same pysh literal type.

    Args:
        lst (list): Python list where all elements are of type ``typ``.
        typ (type): Python Type that denotes the type of the vector.

    Is a subclass of the Python list, and has access to all list methods.

    :attributes: :attr:`typ` - Python type that all elements must be.
    '''
    def __init__(self, lst, typ):
        self.typ = typ
        if typ == None:
            self.typ = '_exec'

        for el in lst:
            if type(el) == typ:
                self.append(el)
            else:
                raise e.PushVectorTypeException(typ, type(el))

class UnevaluatableStackResponse:
    '''Used as the superclass for other bad stack responses.
    '''
    def __repr__(self):
        return 'UNEVALUATABLE_STACK_RESPONSE'

class NoStackItem(UnevaluatableStackResponse):
    '''Used as a response when getting value from empty PushStack.
    '''
    def __repr__(self):
        return 'NO_STACK_ITEM'

class StackOutOfBounds(UnevaluatableStackResponse):
    '''Used as a response when getting value from empty PushStack.
    '''
    def __repr__(self):
        return 'NO_STACK_ITEM'


##                 ##
# Utility Functions #
##                 ##

def flatten_all(lst):
    """Recursively flattens nested lists into a single list.

    :param list lst: Nested lists
    :returns: Flattened lists.

    :example:
        >>> flatten_all([1, [2, 3, [4], 5]])
        [1, 2, 3, 4, 5]
    """
    result = []
    for i in lst:
        if isinstance(i, list):
            result += flatten_all(i)
        else:
            result.append(i)
    return result

def is_str_type(thing):
    """Returns true if thing is a string, agnostic to Python version.

    TODO: I think these functions need unit tests...

    :param thing: Anything!
    :returns: True if thing is a string, False otherwise.
    """
    if sys.version_info[0] == 3:
        return isinstance(thing, (str, bytes))
    elif sys.version_info[0] == 2:
        return isinstance(thing, (str, unicode))
    else:
        raise Exception("Uknown python version?")

def is_int_type(thing):
    """Returns true if thing is an int or long, agnostic to Python version.

    TODO: I think these functions need unit tests...

    :param thing: Anything!
    :returns: True if thing is an int or long, False otherwise.
    """
    if isinstance(thing, np.int64):
        return True
    if sys.version_info[0] == 3:
        return isinstance(thing, int)
    elif sys.version_info[0] == 2:
        return isinstance(thing, (int, long))
    else:
        raise Exception("Uknown python version?")

def is_float_type(thing):
    """TODO: Write function docstring.
    TODO: I think these functions need unit tests...
    """
    return isinstance(thing, (float, np.float, np.float64))

def recognize_pysh_type(thing):
    """If thing is a literal, return its type -- otherwise return False.

    :param thing: anything!
    :returns: A string with a ``_`` as the first char. This is how Pysh types
        are denoted throughout the entire package.
        If there is no appropriate Pysh type, returns False.

    :example:
        >>> recognize_pysh_type(True)
        '_bool'
        >>> recognize_pysh_type(77)
        '_integer'
        >>> recognize_pysh_type(abs)
        False
    """
    if isinstance(thing, instr.PyshInputInstruction):
        return '_input_instruction'
    elif isinstance(thing, instr.PyshOutputInstruction):
        return '_output_instruction'
    elif isinstance(thing, instr.PyshClassVoteInstruction):
        return '_class_vote_instruction'
    elif isinstance(thing, instr.PyshInstruction):
        return '_instruction'
    elif isinstance(thing, (bool, np.bool_)):
        return '_boolean'
    elif is_int_type(thing):
        return '_integer'
    elif is_float_type(thing):
        return '_float'
    elif is_str_type(thing):
        return '_string'
    elif isinstance(thing, Character):
        return '_char'
    elif isinstance(thing, PushVector):
        t = recognize_pysh_type(thing.typ())
        return '_vector' + t
    elif isinstance(thing, list):
        return '_list'
    else:
        print("Could not find pysh type for", thing, "of type", type(thing))
        return False

def keep_number_reasonable(n):
    '''Returns a version of n that obeys the limits set in :mod:`constants`.

    :param n: Any numeric value.
    :returns: ``n`` clamped to ``-c.max_number_magnitude < n < c.max_number_magnitude``
    '''
    if n > c.max_number_magnitude:
        n = c.max_number_magnitude
    elif n < -c.max_number_magnitude:
        n = -c.max_number_magnitude
    return n

def count_parens(tree):
    '''Returns the number of paren pairs in tree.

    :param list tree: Nested list structure equivalent to tree.
    :returns: Integer equal to the number of paren pairs.

    '''
    remaining = tree
    total = 0

    while True:
        if not isinstance(remaining, list):
            return total
        elif len(remaining) == 0:
            return total + 1
        elif isinstance(remaining[0], list):
            remaining.pop(0)
        else:
            remaining = remaining[0] + remaining[1:]
            total += 1

def count_points(tree):
    """Returns the number of points in tree.

    Each atom and each pair of parentheses counts as a point.

    :param list tree: Nested list structure equivalent to tree.
    :returns: Integer equal to the number of points.
    """
    remaining = tree
    total = 0

    while True:
        if not isinstance(remaining, list):
            return total + 1
        elif len(remaining) == 0:
            return total + 1
        elif not type(remaining[0], list):
            remaining = remaining[1:]
            total += 1
        else:
            remaining = remaining[0] + remaining[1:]
            total += 1
    return total

def reductions(f, l):
    """Returns intermediate values of the reduction of ``l`` by ``f``.

    :param f: Function to be reduced down ``l``.
    :param l: List to reduce ``f`` down.
    :returns: List of intermediate values.

    :example:
        >>> reductions(lambda x,y: x * y, [1, 3, 5, 7])
        [1, 3, 15, 105]
    """
    result = []
    for i, val in enumerate(l):
        if i == 0:
            result.append(val)
        else:
            result.append(f(result[-1], val))
    return result

def merge_dicts(*dict_args):
    """Merges arbitrary number of dicts into one dict.

    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    Taken From: http://stackoverflow.com/a/26853961/4297413 Thanks to Aaron Hall

    :param *dict_args: Arbitrary number of arguments, all must be dicts.
    :returns: Result of merging all dicts into a single dict.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def merge_sets(*set_args):
    """Given any number of sets, shallow copy and merge into a new set.

    :param *set_args: Arbitrary number of arguments, all must be sets.
    :returns: Result of union-ing all sets into a single set.
    """
    result = set()
    for s in set_args:
        result.update(s)
    return result

def ensure_list(thing):
    """Returns argument inside of a list if it is not already a list.

    :param thing: Anything!
    :returns: If ``thing`` is a list, returns ``thing``
        otherwise returns ``[thing]``.
    :example:
        >>> ensure_list("ABC")
        ["ABC"]
        >>> ensure_list([1, 2, 3])
        [1, 2, 3]
    """
    if isinstance(thing, list):
        return thing
    else:
        return [thing]

def levenshtein_distance(s1, s2):
    """Computes the string edit distance based on the Levenshtein Distance.

    All credit for implementation goes to:
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    Much appreciated.

    .. note::
        If ``s1`` and ``s2`` must both be strings or both be list. Cannot mix
        types.

    :param s1: String or list
    :param s2: Other string or list
    :returns: Integer equal to the number of edits to get from ``s1`` to ``s2``.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]



def test_and_train_data_from_domains(domains):
    """Creates train and test data.

    Takes a list of domains and creates a set of (random) train inputs and a
    set of test inputs based on the domains. Returns [train test].

    .. note::
        This will likely no longer be used once integration with scikit-learn
        and other libraries improves.
    """
    train_set = []
    test_set = []

    for d in domains:
        num_train = d["train_test_split"][0]
        num_test = d["train_test_split"][1]

        inpts = d["inputs"]
        if callable(inpts):
            inpts = [inpts() for x in range(num_train+num_test)]
        else:
            inpts = inpts[:]

        random.shuffle(list(inpts))
        train_set += inpts[:num_train]
        test_set += inpts[-num_test:]

    return [train_set, test_set]

def int_to_char(i):
    '''Convert int ``i`` to chars and only get English-friendly chars

    :param int i: Any integer.
    :returns: English-friendly string of length 1.
    :example:
        >>> int_to_char(42)
        'J'
        >>> int_to_char(-42)
        'v'
    '''
    i = (i + 32) % 128
    return chr(i)

def gaussian_noise_factor():
    '''Returns Gaussian noise of mean 0, std dev 1.

    :returns: Float samples from Gaussian distribution.

    :example:
        >>> gaussian_noise_factor()
        1.43412557975
        >>> gaussian_noise_factor()
        -0.0410900866765
    '''
    return math.sqrt(-2.0 * math.log(random.random())) * math.cos(2.0 * math.pi * random.random())

def perturb_with_gaussian_noise(sd, n):
    '''Returns n perturbed with standard deviation.

    :param float sd: Standard deviation
    :param float n: number to perturb.
    :returns: Perturbed float.
    :example:
        >>> perturb_with_gaussian_noise(5, 0)
        5.03608878454
        >>> perturb_with_gaussian_noise(1, 100)
        99.9105032498
    '''
    return n + (sd * gaussian_noise_factor())

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
        elif pysh_type in ['_instruction', '_input_instruction',
                           '_output_instruction', '_class_vote_instruction']:
            # If ``el`` an instance of any of the instruction types, append to
            # the program.
            program.append(el)
        elif u.is_str_type(el):
            # If ``el`` is a string:
            el = str(el)
            # Attempt to find an instruction with ``el`` as its name.
            matching_instruction = None
            try:
                matching_instruction = ri.get_instruction(el)
            except e.UnknownInstructionName(el):
                pass
            # If matching_instruction is None, it must be a ssring literal.
            if matching_instruction == None:
                program.append(el)
            else:
                program.append(matching_instruction)
        elif pysh_type == '_list':
            # If ``el`` is a list (but not PushVector) turn it into a program
            # and append it to (aka. nest it in) the program.
            program.append(load_program_from_list(el))
    return program

def median_absolute_deviation(a):
    """Returns the MAD of X.

    Parameters
    ----------
    a : array-like, shape = (n,)

    Returns
    -------
    mad : float

    :param list a: List of numbers.
    :returns: MAD of list.
    """
    return np.median(np.abs(a - np.median(a)))
