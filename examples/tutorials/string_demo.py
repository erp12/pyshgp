# _*_ coding: utf_8 _*_
"""
The **string_demo** problem is a simple benchmark that is designed to
deomonstrate a PushGP's string manipulation capabilities. The goal of the
problem is as follows:

Take the input string, remove the last 2 characters, and then concat this
result with itself. The fitness will be the number of non-matching characters
in the resulting string. For example, desired result of "abcde" would be
"abcabc", and a string of "abcabcrrr" would have an error of 3, for 3 too many
characters, and the string "aaaaaa" would have error of 4, since it gets 2 of
the characters right.

Running The Example
###################

To run the odd problem, install ``pyshgp`` and run the example file.::

    python pyshgp/examples/tutorials/string_demo.py

The Error Function
##################

The error of a Push program for this problem is determined by comparing an
outputed string value to a target value using the sum of two error values.

The first error value is the difference between two strings based on the
characters at each position. This is calculated by the ``string_difference``
function, found below.

.. literalinclude:: /../examples/tutorials/string_demo.py
    :pyobject: string_difference

The second error value is the difference in counts for each character between
the output string and target string. This is calcuated using the
``string_char_counts_difference`` function below:

.. literalinclude:: /../examples/tutorials/string_demo.py
    :pyobject: string_char_counts_difference

The error function (given below) is a python function that takes a Push
program as input, loads the input string into a PushInterpreter, runs the
program, and scores the output by summing the two functions described above.
This processes is reapeated for each training case, and the resulting list of
numeric errors is returned as the error vector.

.. literalinclude:: /../examples/tutorials/string_demo.py
   :pyobject: string_error_func

Hyperparameters
#################

The instance of the string demo problem described in this file overides the
default atom generators. Atom generators are things that produce an "atom".
For example, an anonymous function that returns a random floating point value
and an instruction can also be considered an atom generator that adds itself to
the random program. You can read more about atom generators
`here <https://erp12.github.io/push-redux/pages/intro_to_push/index.html#push_gp>`_.

This string manipulation problem on requires the use of a handful of string
instructions and integer instructions to be solved. It does not need to make
use of boolean instructions, float instructions, or code instructions. To
lower the search space, and make things easier for evolution, we hand pick a
smaller set of atom generators.

.. literalinclude:: /../examples/tutorials/string_demo.py
   :lines: 168-181

Another hyperparameter that is changed from its default for this problemm is
the variation operators. You can find the supported variation operators in the
``pyshgp`` API documation `here <../api/gp.html#module-pyshgp.gp.variation>`_
and you can learn more about how these genetic operators work on the push-redux
`here <https://erp12.github.io/push-redux/pages/genetic_operators/index.html#mutation>`_.

The ``pyshgp`` variation operators are set using a list containing tuples. Each
tuple contains two elements: 1) A VariationOperator ojbect and 2) a float
describing the relative frequency which the operator will be selected compared
to the rest of the operators in the list.

.. literalinclude:: /../examples/tutorials/string_demo.py
   :lines: 163-166

As you can see by the above code snippet, this string problem uses two
variation operators, one UniformMutation and one Alternation. Each is inside of
a tuple where the seond element (the float) is set to 0.5. Given that both
floats are equal, both operators will be eqaully as likely to be chosen when
creating a child. If the float in the UniformMutation tuple was 1.0 and the
float in the Alternation tuple was 0.5, the UniformMutation operator would be
twice as likely to be selected to produce a child as Alternation.

Starting The Run
#################

Finally, we must instanciate the ``SimplePushGPEvolver`` and set the
hyperparameters. Then we can call the ``fit`` method and pass three things:
1) The error function 2) the number of input values that will be supplied and
3) a list of pysh types to output.
"""
import random
import collections

from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instruction
from pyshgp.gp.evolvers import SimplePushGPEvolver


def string_difference(s1, s2):
    """Returns the difference in the strings, based on character position.
    """
    char_lvl_diff = 0
    for c1, c2 in zip(s1, s2):
        char_lvl_diff += int(not c1 == c2)
    return char_lvl_diff + abs(len(s1) - len(s2))


def string_char_counts_difference(s1, s2):
    """Returns the difference in character counts between the two input
    strings.
    """
    result = len(s1) + len(s2)
    s1_letters = collections.Counter(s1)
    for c in s2:
        if c in s1_letters:
            result -= 2
            s1_letters[c] -= 1
            if s1_letters[c] == 0:
                s1_letters.pop(c, None)
    return result


def random_str():
    s = ""
    for i in range(random.randint(1, 10)):
        alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        s += random.choice(alph)
    return s


def string_error_func(program):
    inputs = ["abcde", "", "E", "Hi", "Tom", "leprechaun", "zoomzoomzoom",
              "qwertyuiopasd", "GallopTrotCanter", "Quinona", "_abc"]
    errors = []

    for inpt in inputs:
        # Create the push interpreter
        interpreter = PushInterpreter([inpt], ['_string'])
        y_hat = interpreter.run(program)[0]
        if y_hat is None:
            errors.append(1e5)
        else:
            # compare to target output
            target_output = inpt[:-2] + inpt[:-2]
            errors.append(string_difference(y_hat, target_output) +
                          string_char_counts_difference(y_hat, target_output))
    return errors


atom_generators = [get_instruction("_string_length"),
                   get_instruction("_string_head"),
                   get_instruction("_string_concat"),
                   get_instruction("_string_stack_depth"),
                   get_instruction("_string_swap"),
                   get_instruction("_string_dup"),
                   get_instruction("_integer_add"),
                   get_instruction("_integer_sub"),
                   get_instruction("_integer_dup"),
                   get_instruction("_integer_swap"),
                   get_instruction("_integer_stack_depth"),
                   get_instruction("_integer_inc"),
                   lambda: random.randint(0, 10),
                   lambda: random_str()]

if __name__ == "__main__":
    # evo = SimplePushGPEvolver(
    #     verbose=1,
    #     atom_generators=atom_generators,
    #     population_size=100,
    #     max_generations=3,
    #     simplification_steps=100,
    #     n_jobs=1)
    evo = SimplePushGPEvolver(
        verbose=2,
        atom_generators=atom_generators,
        n_jobs=-1)
    evo.fit(string_error_func, 1, ['_string'])
