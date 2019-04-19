import math
import sys

from pyshgp.push.atoms import Literal, CodeBlock, JitInstructionRef
from pyshgp.push.interpreter import DEFAULT_INTERPRETER
from pyshgp.push.types import Char, PushInt, PushStr

# Renames for convience
i_set = DEFAULT_INTERPRETER.instruction_set
L = Literal
jir = JitInstructionRef
CB = CodeBlock


SPECS = [
    # COMMON
    {
        "instr": i_set["bool_pop"],
        "in": {"bool": [True, False]},
        "ex": {"bool": [True]}
    },
    {
        "instr": i_set["int_dup"],
        "in": {"int": [101]},
        "ex": {"int": [101, 101]}
    },
    {
        "instr": i_set["float_dup_times"],
        "in": {"int": [3], "float": [1.23]},
        "ex": {"int": [],  "float": [1.23, 1.23, 1.23]}
    },
    {
        "instr": i_set["bool_dup_times"],
        "in": {"int": [sys.maxsize + 1], "bool": [True]},
        "ex": {"int": [],               "bool": [True] * 500}
    },
    {
        "instr": i_set["char_swap"],
        "in": {"char": [Char("a"), Char("b")]},
        "ex": {"char": [Char("b"), Char("a")]}
    },
    {
        "instr": i_set["str_rot"],
        "in": {"str": ["A", "B", "C"]},
        "ex": {"str": ["B", "C", "A"]}
    },
    {
        "instr": i_set["bool_flush"],
        "in": {"bool": [True, False]},
        "ex": {"bool": []}
    },
    {
        "instr": i_set["int_eq"],
        "in": {"int": [5, 6], "bool": []},
        "ex": {"int": [],     "bool": [False]}
    },
    {
        "instr": i_set["float_eq"],
        "in": {"float": [1.23, 1.23], "bool": []},
        "ex": {"float": [],           "bool": [True]}
    },
    {
        "instr": i_set["char_stack_depth"],
        "in": {"char": [], "int": []},
        "ex": {"char": [], "int": [0]}
    },
    {
        "instr": i_set["str_stack_depth"],
        "in": {"str": ["A", "B", "C"], "int": []},
        "ex": {"str": ["A", "B", "C"], "int": [3]}
    },
    {
        "instr": i_set["str_yank"],
        "in": {"str": ["A", "B", "C", "D"], "int": [1]},
        "ex": {"str": ["A", "B", "D", "C"], "int": []}
    },
    {
        "instr": i_set["str_yank"],
        "in": {"str": ["A", "B", "C", "D"], "int": [100]},
        "ex": {"str": ["B", "C", "D", "A"], "int": []}
    },
    {
        "instr": i_set["int_yank_dup"],
        "in": {"int": [8, 7, 6, 5, 4, 3]},
        "ex": {"int": [8, 7, 6, 5, 4, 7]}
    },
    {
        "instr": i_set["int_shove"],
        "in": {"int": [8, 7, 6, 5, 4, 3]},
        "ex": {"int": [8, 4, 7, 6, 5]}
    },
    {
        "instr": i_set["str_shove_dup"],
        "in": {"str": ["A", "B", "C", "D"],      "int": [100]},
        "ex": {"str": ["D", "A", "B", "C", "D"], "int": []}
    },
    {
        "instr": i_set["float_is_empty"],
        "in": {"float": [1.23, 1.23], "bool": []},
        "ex": {"float": [1.23, 1.23], "bool": [False]},
    },
    {
        "instr": i_set["char_is_empty"],
        "in": {"char": [], "bool": []},
        "ex": {"char": [], "bool": [True]},
    },
    # NUMERIC
    {
        "instr": i_set["int_add"],
        "in": {"int": [1, 2]},
        "ex": {"int": [3]}
    },
    {
        "instr": i_set["float_sub"],
        "in": {"float": [100.5, 50.1]},
        "ex": {"float": [50.4]}
    },
    {
        "instr": i_set["float_mult"],
        "in": {"float": [10.0, 1.5]},
        "ex": {"float": [15.0]}
    },
    {
        "instr": i_set["int_div"],
        "in": {"int": [10, 3]},
        "ex": {"int": [3]}
    },
    {
        "instr": i_set["float_div"],
        "in": {"float": [10.0, 0.0]},
        "ex": {"float": [10.0, 0.0]}
    },
    {
        "instr": i_set["float_mod"],
        "in": {"float": [10.0, 3.0]},
        "ex": {"float": [1.0]}
    },
    {
        "instr": i_set["int_mod"],
        "in": {"int": [10, 0]},
        "ex": {"int": [10, 0]}
    },
    {
        "instr": i_set["int_max"],
        "in": {"int": [10, 0]},
        "ex": {"int": [10]}
    },
    {
        "instr": i_set["float_min"],
        "in": {"float": [10.1, 3.1]},
        "ex": {"float": [3.1]}
    },
    {
        "instr": i_set["float_inc"],
        "in": {"float": [1.5]},
        "ex": {"float": [2.5]}
    },
    {
        "instr": i_set["int_dec"],
        "in": {"int": [100]},
        "ex": {"int": [99]}
    },
    # lt, lte, gt, gte
    {
        "instr": i_set["float_sin"],
        "in": {"float": [math.pi]},
        "ex": {"float": [math.sin(math.pi)]}
    },
    {
        "instr": i_set["float_cos"],
        "in": {"float": [math.pi]},
        "ex": {"float": [math.cos(math.pi)]}
    },
    {
        "instr": i_set["float_tan"],
        "in": {"float": [math.pi]},
        "ex": {"float": [math.tan(math.pi)]}
    },
    {
        "instr": i_set["int_from_bool"],
        "in": {"bool": [True],  "int": []},
        "ex": {"bool": [],      "int": [1]}
    },
    {
        "instr": i_set["float_from_bool"],
        "in": {"bool": [False], "float": []},
        "ex": {"bool": [],      "float": [0.0]}
    },
    {
        "instr": i_set["int_from_float"],
        "in": {"float": [1.23], "int": []},
        "ex": {"float": [],     "int": [1]}
    },
    {
        "instr": i_set["float_from_int"],
        "in": {"int": [7],  "float": []},
        "ex": {"int": [],   "float": [7.0]}
    },
    # TEXT
    {
        "instr": i_set["char_concat"],
        "in": {"char": [Char("a"), Char("b")], "str": []},
        "ex": {"char": [],                     "str": ["ab"]}
    },
    {
        "instr": i_set["str_insert_str"],
        "in": {"str": ["Z", "abc"], "int": [1]},
        "ex": {"str": ["aZbc"], "int": []}
    },
    {
        "instr": i_set["str_from_first_char"],
        "in": {"str": ["Hello"]},
        "ex": {"str": ["H"]}
    },
    {
        "instr": i_set["char_from_last_char"],
        "in": {"str": ["Hello"], "char": []},
        "ex": {"str": [],        "char": [Char("o")]}
    },
    {
        "instr": i_set["char_from_nth_char"],
        "in": {"str": ["Hello"], "int": [1], "char": []},
        "ex": {"str": [],        "int": [],  "char": [Char("e")]}
    },
    {
        "instr": i_set["str_contains_str"],
        "in": {"str": ["el", "Hello"], "bool": []},
        "ex": {"str": [],              "bool": [True]}
    },
    {
        "instr": i_set["str_contains_char"],
        "in": {"str": ["Hello"], "char": ["z"], "bool": []},
        "ex": {"str": [],        "char": [],    "bool": [False]}
    },
    {
        "instr": i_set["str_index_of_str"],
        "in": {"str": ["el", "Hello"], "int": []},
        "ex": {"str": [],              "int": [1]}
    },
    # LOGICAL
    # IO
    {
        "instr": i_set["print_str"],
        "in": {"str": ["Hello World!"], "stdout": ""},
        "ex": {"str": [],               "stdout": "Hello World!"}
    },
    {
        "instr": i_set["print_int"],
        "in": {"int": [10], "stdout": ""},
        "ex": {"int": [],   "stdout": "10"}
    },
    # CODE
    {
        "instr": i_set["noop"],
        "in": {"int": [3], "str": ["foo"]},
        "ex": {"int": [3], "str": ["foo"]}
    },
    {
        "instr": i_set["noop_open"],
        "in": {"int": [3], "str": ["foo"]},
        "ex": {"int": [3], "str": ["foo"]}
    },
    {
        "instr": i_set["code_is_code_block"],
        "in": {"code": [L(5, PushInt)], "bool": []},
        "ex": {"code": [],              "bool": [False]}
    },
    {
        "instr": i_set["code_is_code_block"],
        "in": {"code": [CB(L(5, PushInt))], "bool": []},
        "ex": {"code": [],                  "bool": [True]}
    },
    {
        "instr": i_set["code_is_singular"],
        "in": {"code": [L(5, PushInt)], "bool": []},
        "ex": {"code": [],              "bool": [True]}
    },
    {
        "instr": i_set["code_is_singular"],
        "in": {"code": [CB(L(5, PushInt))], "bool": []},
        "ex": {"code": [],                  "bool": [False]}
    },
    {
        "instr": i_set["code_length"],
        "in": {"code": [CB(L(5, PushInt))], "int": []},
        "ex": {"code": [],                  "int": [1]}
    },
    {
        "instr": i_set["code_wrap"],
        "in": {"code": [L(5, PushInt)]},
        "ex": {"code": [CB(L(5, PushInt))]}
    },
    {
        "instr": i_set["code_list"],
        "in": {"code": [L(5, PushInt), L(1, PushInt)]},
        "ex": {"code": [CB(L(1, PushInt), L(5, PushInt))]}
    },
    {
        "instr": i_set["code_list"],
        "in": {"code": [L(5, PushInt), CB(L(1, PushInt))]},
        "ex": {"code": [CB(CB(L(1, PushInt)), L(5, PushInt))]}
    },
    {
        "instr": i_set["code_combine"],
        "in": {"code": [L(5, PushInt), L(1, PushInt)]},
        "ex": {"code": [CB(L(1, PushInt), L(5, PushInt))]}
    },
    {
        "instr": i_set["code_combine"],
        "in": {"code": [L(5, PushInt), CB(L(1, PushInt))]},
        "ex": {"code": [CB(L(1, PushInt), L(5, PushInt))]}
    },
    {
        "instr": i_set["code_do"],
        "in": {"code": [L(5, PushInt)], "exec": []},
        "ex": {"code": [],              "exec": [L(5, PushInt)]},
    },
    {
        "instr": i_set["code_do_dup"],
        "in": {"code": [L(5, PushInt)], "exec": []},
        "ex": {"code": [L(5, PushInt)], "exec": [L(5, PushInt)]},
    },
    {
        "instr": i_set["code_do_then_pop"],
        "in": {"code": [L(5, PushInt)], "exec": []},
        "ex": {"code": [L(5, PushInt)], "exec": [jir("code_pop"), L(5, PushInt)]},
    },
    {
        "instr": i_set["code_do_range"],
        "in": {
            "code": [L(5, PushInt)],
            "int": [13, 10],
            "exec": []
        },
        "ex": {
            "code": [],
            "int": [13],
            "exec": [CB(L(12, PushInt), L(10, PushInt), jir("code_from_exec"), L(5, PushInt), jir("code_do_range")), L(5, PushInt)]
        }
    },
    {
        "instr": i_set["exec_do_range"],
        "in": {"int": [0, 3], "exec": [L(5, PushInt)]},
        "ex": {"int": [0],    "exec": [CB(L(1, PushInt), L(3, PushInt), jir("exec_do_range"), L(5, PushInt)), L(5, PushInt)]}
    },
    {
        "instr": i_set["code_do_count"],
        "in": {"code": [L(5, PushInt)], "int": [3], "exec": []},
        "ex": {
            "code": [],
            "int": [],
            "exec": [CB(L(0, PushInt), L(2, PushInt), jir("code_from_exec"), L(5, PushInt), jir("code_do_range"))]
        }
    },
    {
        "instr": i_set["exec_do_count"],
        "in": {"int": [3], "exec": [L(5, PushInt)]},
        "ex": {"int": [],  "exec": [CB(L(0, PushInt), L(2, PushInt), jir("exec_do_range"), L(5, PushInt))]}
    },
    {
        "instr": i_set["code_do_times"],
        "in": {"code": [L(5, PushInt)], "int": [3], "exec": []},
        "ex": {
            "code": [],
            "int": [],
            "exec": [CB(L(0, PushInt), L(2, PushInt), jir("code_from_exec"), CB(jir("int_pop"), L(5, PushInt)), jir("code_do_range"))]
        }
    },
    {
        "instr": i_set["exec_do_times"],
        "in": {"int": [3], "exec": [L(5, PushInt)]},
        "ex": {"int": [],  "exec": [CB(L(0, PushInt), L(2, PushInt), jir("exec_do_range"), CB(jir("int_pop"), L(5, PushInt)))]}
    },
    {
        "instr": i_set["exec_while"],
        "in": {"bool": [False], "exec": [L(5, PushInt)]},
        "ex": {"bool": [],      "exec": []},
    },
    {
        "instr": i_set["exec_while"],
        "in": {"bool": [True], "exec": [L(5, PushInt)]},
        "ex": {"bool": [],     "exec": [L(5, PushInt), jir("exec_while"), L(5, PushInt)]},
    },
    {
        "instr": i_set["exec_do_while"],
        "in": {"exec": [L(5, PushInt)]},
        "ex": {"exec": [L(5, PushInt), jir("exec_while"), L(5, PushInt)]},
    },
    {
        "instr": i_set["code_map"],
        "in": {"code": [L(5, PushInt)], "exec": [L(-1, PushInt)]},
        "ex": {"code": [],              "exec": [CB(CB(jir("code_from_exec"), L(5, PushInt), L(-1, PushInt)), jir("code_wrap"))]},
    },
    {
        "instr": i_set["code_if"],
        "in": {"bool": [True], "code": [L("C", PushStr), L("B", PushStr), L("A", PushStr)], "exec": []},
        "ex": {"bool": [],     "code": [L("C", PushStr)],                                   "exec": [L("A", PushStr)]}
    },
    {
        "instr": i_set["code_if"],
        "in": {"bool": [False], "code": [L("C", PushStr), L("B", PushStr), L("A", PushStr)], "exec": []},
        "ex": {"bool": [],      "code": [L("C", PushStr)],                                   "exec": [L("B", PushStr)]}
    },
    {
        "instr": i_set["exec_if"],
        "in": {"bool": [True], "exec": [L("C", PushStr), L("B", PushStr), L("A", PushStr)]},
        "ex": {"bool": [],     "exec": [L("C", PushStr), L("A", PushStr)]}
    },
    {
        "instr": i_set["exec_if"],
        "in": {"bool": [False], "exec": [L("C", PushStr), L("B", PushStr), L("A", PushStr)]},
        "ex": {"bool": [],      "exec": [L("C", PushStr), L("B", PushStr)]}
    },
    {
        "instr": i_set["code_when"],
        "in": {"bool": [True], "code": [L("A", PushStr)], "exec": []},
        "ex": {"bool": [],     "code": [],                "exec": [L("A", PushStr)]}
    },
    {
        "instr": i_set["code_when"],
        "in": {"bool": [False], "code": [L("A", PushStr)], "exec": []},
        "ex": {"bool": [],      "code": [],       "exec": []}
    },
    {
        "instr": i_set["exec_when"],
        "in": {"bool": [True], "exec": [L("A", PushStr)]},
        "ex": {"bool": [],     "exec": [L("A", PushStr)]}
    },
    {
        "instr": i_set["exec_when"],
        "in": {"bool": [False], "exec": [L("A", PushStr)]},
        "ex": {"bool": [],      "exec": []}
    },
    {
        "instr": i_set["code_member"],
        "in": {"code": [L(1, PushInt), CB(L(1, PushInt), L(2, PushInt))], "bool": []},
        "ex": {"code": [],                                                "bool": [True]},
    },
    {
        "instr": i_set["code_member"],
        "in": {"code": [L("Z", PushStr), L(1, PushInt)], "bool": []},
        "ex": {"code": [],                               "bool": [False]},
    },
    {
        "instr": i_set["code_nth"],
        "in": {"code": [CB(L(1, PushInt), L(2, PushInt))], "int": [1]},
        "ex": {"code": [L(2, PushInt)],                    "int": []},
    },
    {
        "instr": i_set["make_empty_code_block"],
        "in": {"code": []},
        "ex": {"code": [CB()]},
    },
    {
        "instr": i_set["is_empty_code_block"],
        "in": {"code": [L(1, PushInt)], "bool": []},
        "ex": {"code": [],              "bool": [False]},
    },
    {
        "instr": i_set["is_empty_code_block"],
        "in": {"code": [CB(L(1, PushInt))], "bool": []},
        "ex": {"code": [],                  "bool": [False]},
    },
    {
        "instr": i_set["is_empty_code_block"],
        "in": {"code": [CB()], "bool": []},
        "ex": {"code": [],     "bool": [True]},
    },
    {
        "instr": i_set["code_size"],
        "in": {"code": [CB()], "int": []},
        "ex": {"code": [],     "int": [0]},
    },
    {
        "instr": i_set["code_size"],
        "in": {"code": [CB(CB(L("a", PushStr)), L("a", PushStr))], "int": []},
        "ex": {"code": [],                                         "int": [3]},
    },
    {
        "instr": i_set["code_extract"],
        "in": {"code": [CB(CB(L("a", PushStr)), L("b", PushStr))], "int": [0]},
        "ex": {"code": [CB(CB(L("a", PushStr)), L("b", PushStr))], "int": []},
    },
    {
        "instr": i_set["code_extract"],
        "in": {"code": [CB(CB(L("a", PushStr)), L("b", PushStr))], "int": [1]},
        "ex": {"code": [CB(L("a", PushStr))],                      "int": []},
    },
    {
        "instr": i_set["code_extract"],
        "in": {"code": [CB(CB(L("a", PushStr)), L("b", PushStr))], "int": [2]},
        "ex": {"code": [L("a", PushStr)],                          "int": []},
    },
    {
        "instr": i_set["code_extract"],
        "in": {"code": [CB()], "int": [10]},
        "ex": {"code": [CB()], "int": [10]},
    },
    {
        "instr": i_set["code_insert"],
        "in": {"code": [L("Z", PushStr), CB(CB(L("A", PushStr)), L("B", PushStr))], "int": [0]},
        "ex": {"code": [CB(L("Z", PushStr), CB(L("A", PushStr)), L("B", PushStr))], "int": []},
    },
    {
        "instr": i_set["code_insert"],
        "in": {"code": [L("Z", PushStr), CB(CB(L("A", PushStr)), L("B", PushStr))], "int": [1]},
        "ex": {"code": [CB(CB(L("Z", PushStr), L("A", PushStr)), L("B", PushStr))], "int": []},
    },
    {
        "instr": i_set["code_insert"],
        "in": {"code": [L("Z", PushStr), CB(CB(L("A", PushStr)), L("B", PushStr))], "int": [2]},
        "ex": {"code": [CB(CB(L("A", PushStr)), L("Z", PushStr), L("B", PushStr))], "int": []},
    },
    {
        "instr": i_set["code_first_position"],
        "in": {"code": [L("B", PushStr), CB(L("A", PushStr), L("B", PushStr))], "int": []},
        "ex": {"code": [], "int": [1]},
    },
    {
        "instr": i_set["code_first_position"],
        "in": {"code": [L("Z", PushStr), CB(L("A", PushStr), L("B", PushStr))], "int": []},
        "ex": {"code": [], "int": [-1]},
    },
    {
        "instr": i_set["code_reverse"],
        "in": {"code": [CB(L("A", PushStr), L("B", PushStr))]},
        "ex": {"code": [CB(L("B", PushStr), L("A", PushStr))]},
    },
]
