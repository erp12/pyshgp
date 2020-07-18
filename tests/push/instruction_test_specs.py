import math
import sys

from pyshgp.push.atoms import Literal, CodeBlock, InstructionMeta
from pyshgp.push.types import Char, PushInt, PushStr, BoolVector, IntVector, FloatVector, CharVector, StrVector, \
    PushIntVector

# Shorthand
L = lambda v, t: Literal(value=v, push_type=t)
IM = lambda nm, cb: InstructionMeta(name=nm, code_blocks=cb)
CB = lambda *args: CodeBlock(list(args))

SPECS = [
    # COMMON
    {
        "instr": "bool_pop",
        "in": {"bool": [True, False]},
        "ex": {"bool": [True]}
    },
    {
        "instr": "int_dup",
        "in": {"int": [101]},
        "ex": {"int": [101, 101]}
    },
    {
        "instr": "float_dup_times",
        "in": {"int": [3], "float": [1.23]},
        "ex": {"int": [], "float": [1.23, 1.23, 1.23]}
    },
    {
        "instr": "bool_dup_times",
        "in": {"int": [sys.maxsize + 1], "bool": [True]},
        "ex": {"int": [], "bool": [True] * 500}
    },
    {
        "instr": "char_swap",
        "in": {"char": [Char("a"), Char("b")]},
        "ex": {"char": [Char("b"), Char("a")]}
    },
    {
        "instr": "str_rot",
        "in": {"str": ["A", "B", "C"]},
        "ex": {"str": ["B", "C", "A"]}
    },
    {
        "instr": "bool_flush",
        "in": {"bool": [True, False]},
        "ex": {"bool": []}
    },
    {
        "instr": "int_eq",
        "in": {"int": [5, 6], "bool": []},
        "ex": {"int": [], "bool": [False]}
    },
    {
        "instr": "float_eq",
        "in": {"float": [1.23, 1.23], "bool": []},
        "ex": {"float": [], "bool": [True]}
    },
    {
        "instr": "char_stack_depth",
        "in": {"char": [], "int": []},
        "ex": {"char": [], "int": [0]}
    },
    {
        "instr": "str_stack_depth",
        "in": {"str": ["A", "B", "C"], "int": []},
        "ex": {"str": ["A", "B", "C"], "int": [3]}
    },
    {
        "instr": "str_yank",
        "in": {"str": ["A", "B", "C", "D"], "int": [1]},
        "ex": {"str": ["A", "B", "D", "C"], "int": []}
    },
    {
        "instr": "str_yank",
        "in": {"str": ["A", "B", "C", "D"], "int": [100]},
        "ex": {"str": ["B", "C", "D", "A"], "int": []}
    },
    {
        "instr": "int_yank_dup",
        "in": {"int": [8, 7, 6, 5, 4, 3]},
        "ex": {"int": [8, 7, 6, 5, 4, 7]}
    },
    {
        "instr": "int_shove",
        "in": {"int": [8, 7, 6, 5, 4, 3]},
        "ex": {"int": [8, 4, 7, 6, 5]}
    },
    {
        "instr": "str_shove_dup",
        "in": {"str": ["A", "B", "C", "D"], "int": [100]},
        "ex": {"str": ["D", "A", "B", "C", "D"], "int": []}
    },
    {
        "instr": "float_is_empty",
        "in": {"float": [1.23, 1.23], "bool": []},
        "ex": {"float": [1.23, 1.23], "bool": [False]},
    },
    {
        "instr": "char_is_empty",
        "in": {"char": [], "bool": []},
        "ex": {"char": [], "bool": [True]},
    },
    # NUMERIC
    {
        "instr": "int_add",
        "in": {"int": [1, 2]},
        "ex": {"int": [3]}
    },
    {
        "instr": "float_sub",
        "in": {"float": [100.5, 50.1]},
        "ex": {"float": [50.4]}
    },
    {
        "instr": "float_mult",
        "in": {"float": [10.0, 1.5]},
        "ex": {"float": [15.0]}
    },
    {
        "instr": "int_div",
        "in": {"int": [10, 3]},
        "ex": {"int": [3]}
    },
    {
        "instr": "float_div",
        "in": {"float": [10.0, 0.0]},
        "ex": {"float": [10.0, 0.0]}
    },
    {
        "instr": "float_mod",
        "in": {"float": [10.0, 3.0]},
        "ex": {"float": [1.0]}
    },
    {
        "instr": "int_mod",
        "in": {"int": [10, 0]},
        "ex": {"int": [10, 0]}
    },
    {
        "instr": "int_max",
        "in": {"int": [10, 0]},
        "ex": {"int": [10]}
    },
    {
        "instr": "float_min",
        "in": {"float": [10.1, 3.1]},
        "ex": {"float": [3.1]}
    },
    {
        "instr": "float_inc",
        "in": {"float": [1.5]},
        "ex": {"float": [2.5]}
    },
    {
        "instr": "int_dec",
        "in": {"int": [100]},
        "ex": {"int": [99]}
    },
    # @todo lt, lte, gt, gte
    {
        "instr": "float_sin",
        "in": {"float": [math.pi]},
        "ex": {"float": [math.sin(math.pi)]}
    },
    {
        "instr": "float_cos",
        "in": {"float": [math.pi]},
        "ex": {"float": [math.cos(math.pi)]}
    },
    {
        "instr": "float_tan",
        "in": {"float": [math.pi]},
        "ex": {"float": [math.tan(math.pi)]}
    },
    {
        "instr": "int_from_bool",
        "in": {"bool": [True], "int": []},
        "ex": {"bool": [], "int": [1]}
    },
    {
        "instr": "float_from_bool",
        "in": {"bool": [False], "float": []},
        "ex": {"bool": [], "float": [0.0]}
    },
    {
        "instr": "int_from_float",
        "in": {"float": [1.23], "int": []},
        "ex": {"float": [], "int": [1]}
    },
    {
        "instr": "float_from_int",
        "in": {"int": [7], "float": []},
        "ex": {"int": [], "float": [7.0]}
    },
    # TEXT
    {
        "instr": "char_concat",
        "in": {"char": [Char("a"), Char("b")], "str": []},
        "ex": {"char": [], "str": ["ab"]}
    },
    {
        "instr": "str_insert_str",
        "in": {"str": ["Z", "abc"], "int": [1]},
        "ex": {"str": ["aZbc"], "int": []}
    },
    {
        "instr": "str_from_first_char",
        "in": {"str": ["Hello"]},
        "ex": {"str": ["H"]}
    },
    {
        "instr": "char_from_last_char",
        "in": {"str": ["Hello"], "char": []},
        "ex": {"str": [], "char": [Char("o")]}
    },
    {
        "instr": "char_from_nth_char",
        "in": {"str": ["Hello"], "int": [1], "char": []},
        "ex": {"str": [], "int": [], "char": [Char("e")]}
    },
    {
        "instr": "str_contains_str",
        "in": {"str": ["el", "Hello"], "bool": []},
        "ex": {"str": [], "bool": [True]}
    },
    {
        "instr": "str_contains_char",
        "in": {"str": ["Hello"], "char": ["z"], "bool": []},
        "ex": {"str": [], "char": [], "bool": [False]}
    },
    {
        "instr": "str_index_of_str",
        "in": {"str": ["el", "Hello"], "int": []},
        "ex": {"str": [], "int": [1]}
    },
    # LOGICAL
    # @todo test logical instructions
    # IO
    {
        "instr": "print_str",
        "in": {"str": ["Hello World!"], "stdout": ""},
        "ex": {"str": [], "stdout": "Hello World!"}
    },
    {
        "instr": "print_int",
        "in": {"int": [10], "stdout": ""},
        "ex": {"int": [], "stdout": "10"}
    },
    # CODE
    {
        "instr": "noop",
        "in": {"int": [3], "str": ["foo"]},
        "ex": {"int": [3], "str": ["foo"]}
    },
    {
        "instr": "noop_open",
        "in": {"int": [3], "str": ["foo"]},
        "ex": {"int": [3], "str": ["foo"]}
    },
    {
        "instr": "code_is_code_block",
        "in": {"code": [L(5, PushInt)], "bool": []},
        "ex": {"code": [], "bool": [False]}
    },
    {
        "instr": "code_is_code_block",
        "in": {"code": [CB(L(5, PushInt))], "bool": []},
        "ex": {"code": [], "bool": [True]}
    },
    {
        "instr": "code_is_singular",
        "in": {"code": [L(5, PushInt)], "bool": []},
        "ex": {"code": [], "bool": [True]}
    },
    {
        "instr": "code_is_singular",
        "in": {"code": [CB(L(5, PushInt))], "bool": []},
        "ex": {"code": [], "bool": [False]}
    },
    {
        "instr": "code_length",
        "in": {"code": [CB(L(5, PushInt))], "int": []},
        "ex": {"code": [], "int": [1]}
    },
    {
        "instr": "code_wrap",
        "in": {"code": [L(5, PushInt)]},
        "ex": {"code": [CB(L(5, PushInt))]}
    },
    {
        "instr": "code_list",
        "in": {"code": [L(5, PushInt), L(1, PushInt)]},
        "ex": {"code": [CB(L(1, PushInt), L(5, PushInt))]}
    },
    {
        "instr": "code_list",
        "in": {"code": [L(5, PushInt), CB(L(1, PushInt))]},
        "ex": {"code": [CB(CB(L(1, PushInt)), L(5, PushInt))]}
    },
    {
        "instr": "code_combine",
        "in": {"code": [L(5, PushInt), L(1, PushInt)]},
        "ex": {"code": [CB(L(1, PushInt), L(5, PushInt))]}
    },
    {
        "instr": "code_combine",
        "in": {"code": [L(5, PushInt), CB(L(1, PushInt))]},
        "ex": {"code": [CB(L(1, PushInt), L(5, PushInt))]}
    },
    {
        "instr": "code_do",
        "in": {"code": [L(5, PushInt)], "exec": []},
        "ex": {"code": [], "exec": [L(5, PushInt)]},
    },
    {
        "instr": "code_do_dup",
        "in": {"code": [L(5, PushInt)], "exec": []},
        "ex": {"code": [L(5, PushInt)], "exec": [L(5, PushInt)]},
    },
    {
        "instr": "code_do_then_pop",
        "in": {"code": [L(5, PushInt)], "exec": []},
        "ex": {"code": [L(5, PushInt)], "exec": [IM("code_pop", 0), L(5, PushInt)]},
    },
    {
        "instr": "code_do_range",
        "in": {
            "code": [L(5, PushInt)],
            "int": [13, 10],
            "exec": []
        },
        "ex": {
            "code": [],
            "int": [13],
            "exec": [CB(L(12, PushInt), L(10, PushInt), IM("code_from_exec", 1), L(5, PushInt), IM("code_do_range", 0)),
                     L(5, PushInt)]
        }
    },
    {
        "instr": "exec_do_range",
        "in": {"int": [0, 3], "exec": [L(5, PushInt)]},
        "ex": {"int": [0],
               "exec": [CB(L(1, PushInt), L(3, PushInt), IM("exec_do_range", 1), L(5, PushInt)), L(5, PushInt)]}
    },
    {
        "instr": "code_do_count",
        "in": {"code": [L(5, PushInt)], "int": [3], "exec": []},
        "ex": {
            "code": [],
            "int": [],
            "exec": [CB(L(0, PushInt), L(2, PushInt), IM("code_from_exec", 1), L(5, PushInt), IM("code_do_range", 0))]
        }
    },
    {
        "instr": "exec_do_count",
        "in": {"int": [3], "exec": [L(5, PushInt)]},
        "ex": {"int": [], "exec": [CB(L(0, PushInt), L(2, PushInt), IM("exec_do_range", 1), L(5, PushInt))]}
    },
    {
        "instr": "code_do_times",
        "in": {"code": [L(5, PushInt)], "int": [3], "exec": []},
        "ex": {
            "code": [],
            "int": [],
            "exec": [CB(L(0, PushInt), L(2, PushInt), IM("code_from_exec", 1), CB(IM("int_pop", 0), L(5, PushInt)),
                        IM("code_do_range", 0))]
        }
    },
    {
        "instr": "exec_do_times",
        "in": {"int": [3], "exec": [L(5, PushInt)]},
        "ex": {"int": [],
               "exec": [CB(L(0, PushInt), L(2, PushInt), IM("exec_do_range", 1), CB(IM("int_pop", 0), L(5, PushInt)))]}
    },
    {
        "instr": "exec_while",
        "in": {"bool": [False], "exec": [L(5, PushInt)]},
        "ex": {"bool": [], "exec": []},
    },
    {
        "instr": "exec_while",
        "in": {"bool": [True], "exec": [L(5, PushInt)]},
        "ex": {"bool": [], "exec": [L(5, PushInt), IM("exec_while", 1), L(5, PushInt)]},
    },
    {
        "instr": "exec_do_while",
        "in": {"exec": [L(5, PushInt)]},
        "ex": {"exec": [L(5, PushInt), IM("exec_while", 1), L(5, PushInt)]},
    },
    {
        "instr": "code_map",
        "in": {"code": [L(5, PushInt)], "exec": [L(-1, PushInt)]},
        "ex": {"code": [],
               "exec": [CB(CB(IM("code_from_exec", 1), L(5, PushInt), L(-1, PushInt)), IM("code_wrap", 0))]},
    },
    {
        "instr": "code_if",
        "in": {"bool": [True], "code": [L("C", PushStr), L("B", PushStr), L("A", PushStr)], "exec": []},
        "ex": {"bool": [], "code": [L("C", PushStr)], "exec": [L("A", PushStr)]}
    },
    {
        "instr": "code_if",
        "in": {"bool": [False], "code": [L("C", PushStr), L("B", PushStr), L("A", PushStr)], "exec": []},
        "ex": {"bool": [], "code": [L("C", PushStr)], "exec": [L("B", PushStr)]}
    },
    {
        "instr": "exec_if",
        "in": {"bool": [True], "exec": [L("C", PushStr), L("B", PushStr), L("A", PushStr)]},
        "ex": {"bool": [], "exec": [L("C", PushStr), L("A", PushStr)]}
    },
    {
        "instr": "exec_if",
        "in": {"bool": [False], "exec": [L("C", PushStr), L("B", PushStr), L("A", PushStr)]},
        "ex": {"bool": [], "exec": [L("C", PushStr), L("B", PushStr)]}
    },
    {
        "instr": "code_when",
        "in": {"bool": [True], "code": [L("A", PushStr)], "exec": []},
        "ex": {"bool": [], "code": [], "exec": [L("A", PushStr)]}
    },
    {
        "instr": "code_when",
        "in": {"bool": [False], "code": [L("A", PushStr)], "exec": []},
        "ex": {"bool": [], "code": [], "exec": []}
    },
    {
        "instr": "exec_when",
        "in": {"bool": [True], "exec": [L("A", PushStr)]},
        "ex": {"bool": [], "exec": [L("A", PushStr)]}
    },
    {
        "instr": "exec_when",
        "in": {"bool": [False], "exec": [L("A", PushStr)]},
        "ex": {"bool": [], "exec": []}
    },
    {
        "instr": "code_member",
        "in": {"code": [L(1, PushInt), CB(L(1, PushInt), L(2, PushInt))], "bool": []},
        "ex": {"code": [], "bool": [True]},
    },
    {
        "instr": "code_member",
        "in": {"code": [L("Z", PushStr), L(1, PushInt)], "bool": []},
        "ex": {"code": [], "bool": [False]},
    },
    {
        "instr": "code_nth",
        "in": {"code": [CB(L(1, PushInt), L(2, PushInt))], "int": [1]},
        "ex": {"code": [L(2, PushInt)], "int": []},
    },
    {
        "instr": "make_empty_code_block",
        "in": {"code": []},
        "ex": {"code": [CB()]},
    },
    {
        "instr": "is_empty_code_block",
        "in": {"code": [L(1, PushInt)], "bool": []},
        "ex": {"code": [], "bool": [False]},
    },
    {
        "instr": "is_empty_code_block",
        "in": {"code": [CB(L(1, PushInt))], "bool": []},
        "ex": {"code": [], "bool": [False]},
    },
    {
        "instr": "is_empty_code_block",
        "in": {"code": [CB()], "bool": []},
        "ex": {"code": [], "bool": [True]},
    },
    {
        "instr": "code_size",
        "in": {"code": [CB()], "int": []},
        "ex": {"code": [], "int": [0]},
    },
    {
        "instr": "code_size",
        "in": {"code": [CB(CB(L("a", PushStr)), L("a", PushStr))], "int": []},
        "ex": {"code": [], "int": [3]},
    },
    {
        "instr": "code_extract",
        "in": {"code": [CB(CB(L("a", PushStr)), L("b", PushStr))], "int": [0]},
        "ex": {"code": [CB(CB(L("a", PushStr)), L("b", PushStr))], "int": []},
    },
    {
        "instr": "code_extract",
        "in": {"code": [CB(CB(L("a", PushStr)), L("b", PushStr))], "int": [1]},
        "ex": {"code": [CB(L("a", PushStr))], "int": []},
    },
    {
        "instr": "code_extract",
        "in": {"code": [CB(CB(L("a", PushStr)), L("b", PushStr))], "int": [2]},
        "ex": {"code": [L("a", PushStr)], "int": []},
    },
    {
        "instr": "code_extract",
        "in": {"code": [CB()], "int": [10]},
        "ex": {"code": [CB()], "int": [10]},
    },
    {
        "instr": "code_insert",
        "in": {"code": [L("Z", PushStr), CB(CB(L("A", PushStr)), L("B", PushStr))], "int": [0]},
        "ex": {"code": [CB(L("Z", PushStr), CB(L("A", PushStr)), L("B", PushStr))], "int": []},
    },
    {
        "instr": "code_insert",
        "in": {"code": [L("Z", PushStr), CB(CB(L("A", PushStr)), L("B", PushStr))], "int": [1]},
        "ex": {"code": [CB(CB(L("Z", PushStr), L("A", PushStr)), L("B", PushStr))], "int": []},
    },
    {
        "instr": "code_insert",
        "in": {"code": [L("Z", PushStr), CB(CB(L("A", PushStr)), L("B", PushStr))], "int": [2]},
        "ex": {"code": [CB(CB(L("A", PushStr), L("Z", PushStr)), L("B", PushStr))], "int": []},
    },
    {
        "instr": "code_first_position",
        "in": {"code": [L("B", PushStr), CB(L("A", PushStr), L("B", PushStr))], "int": []},
        "ex": {"code": [], "int": [1]},
    },
    {
        "instr": "code_first_position",
        "in": {"code": [L("Z", PushStr), CB(L("A", PushStr), L("B", PushStr))], "int": []},
        "ex": {"code": [], "int": [-1]},
    },
    {
        "instr": "code_reverse",
        "in": {"code": [CB(L("A", PushStr), L("B", PushStr))]},
        "ex": {"code": [CB(L("B", PushStr), L("A", PushStr))]},
    },
    # Vectors
    {
        "instr": "vector_bool_concat",
        "in": {"vector_bool": [BoolVector([True, False]), BoolVector([False, True])]},
        "ex": {"vector_bool": [BoolVector([False, True, True, False])]}
    },
    {
        "instr": "vector_bool_concat",
        "in": {"vector_bool": [BoolVector([]), BoolVector([])]},
        "ex": {"vector_bool": [BoolVector([])]}
    },
    {
        "instr": "vector_int_conj",
        "in": {"vector_int": [IntVector([0])], "int": [100]},
        "ex": {"vector_int": [IntVector([0, 100])], "int": []}
    },
    {
        "instr": "vector_int_conj",
        "in": {"vector_int": [IntVector([])], "int": [100]},
        "ex": {"vector_int": [IntVector([100])], "int": []}
    },
    {
        "instr": "vector_float_take",
        "in": {"vector_float": [FloatVector([1.2, 3.4])], "int": [1]},
        "ex": {"vector_float": [FloatVector([1.2])], "int": []}
    },
    {
        "instr": "vector_float_take",
        "in": {"vector_float": [FloatVector([1.2, 3.4])], "int": [10]},
        "ex": {"vector_float": [FloatVector([1.2, 3.4])], "int": []}
    },
    {
        "instr": "vector_float_take",
        "in": {"vector_float": [FloatVector([])], "int": [10]},
        "ex": {"vector_float": [FloatVector([])], "int": []}
    },
    {
        "instr": "vector_float_take",
        "in": {"vector_float": [FloatVector([1.2, 3.4])], "int": [0]},
        "ex": {"vector_float": [FloatVector([])], "int": []}
    },
    {
        "instr": "vector_char_subvec",
        "in": {"vector_char": [CharVector([Char("a"), Char("b"), Char("c")])], "int": [1, 2]},
        "ex": {"vector_char": [CharVector([Char("b")])], "int": []}
    },
    {
        "instr": "vector_char_subvec",
        "in": {"vector_char": [CharVector([Char("a"), Char("b"), Char("c")])], "int": [2, 1]},
        "ex": {"vector_char": [CharVector([Char("b")])], "int": []}
    },
    {
        "instr": "vector_char_subvec",
        "in": {"vector_char": [CharVector([])], "int": [0, 100]},
        "ex": {"vector_char": [CharVector([])], "int": []}
    },
    {
        "instr": "vector_char_subvec",
        "in": {"vector_char": [CharVector([Char("a")])], "int": [50, 100]},
        "ex": {"vector_char": [CharVector([])], "int": []}
    },
    {
        "instr": "vector_str_first",
        "in": {"vector_str": [StrVector(["a", "b", "c"])]},
        "ex": {"vector_str": [], "str": ["a"]}
    },
    {
        "instr": "vector_str_first",
        "in": {"vector_str": [StrVector([])]},
        "ex": {"vector_str": [StrVector([])], "str": []}
    },
    {
        "instr": "vector_str_last",
        "in": {"vector_str": [StrVector(["a", "b", "c"])]},
        "ex": {"vector_str": [], "str": ["c"]}
    },
    {
        "instr": "vector_str_last",
        "in": {"vector_str": [StrVector([])]},
        "ex": {"vector_str": [StrVector([])], "str": []}
    },
    {
        "instr": "vector_str_nth",
        "in": {"vector_str": [StrVector(["a", "b", "c"])], "int": [1]},
        "ex": {"vector_str": [], "str": ["b"]}
    },
    {
        "instr": "vector_str_nth",
        "in": {"vector_str": [StrVector(["a", "b", "c"])], "int": [4]},
        "ex": {"vector_str": [], "str": ["b"]}
    },
    {
        "instr": "vector_str_nth",
        "in": {"vector_str": [StrVector([])]},
        "ex": {"vector_str": [StrVector([])], "str": []}
    },
    {
        "instr": "vector_str_rest",
        "in": {"vector_str": [StrVector(["a", "b", "c"])]},
        "ex": {"vector_str": [StrVector(["b", "c"])]}
    },
    {
        "instr": "vector_str_rest",
        "in": {"vector_str": [StrVector([])]},
        "ex": {"vector_str": [StrVector([])]}
    },
    {
        "instr": "vector_str_but_last",
        "in": {"vector_str": [StrVector(["a", "b", "c"])]},
        "ex": {"vector_str": [StrVector(["a", "b"])]}
    },
    {
        "instr": "vector_str_but_last",
        "in": {"vector_str": [StrVector([])]},
        "ex": {"vector_str": [StrVector([])]}
    },
    {
        "instr": "vector_int_length",
        "in": {"vector_int": [IntVector([])]},
        "ex": {"vector_int": [], "int": [0]}
    },
    {
        "instr": "vector_int_length",
        "in": {"vector_int": [IntVector([5, 4, 3])]},
        "ex": {"vector_int": [], "int": [3]}
    },
    {
        "instr": "vector_int_reverse",
        "in": {"vector_int": [IntVector([5, 4, 3])]},
        "ex": {"vector_int": [IntVector([3, 4, 5])]}
    },
    {
        "instr": "vector_int_reverse",
        "in": {"vector_int": [IntVector([])]},
        "ex": {"vector_int": [IntVector([])]}
    },
    {
        "instr": "vector_int_push_all",
        "in": {"vector_int": [IntVector([5, 4, 3])]},
        "ex": {"vector_int": [], "int": [3, 4, 5]}
    },
    {
        "instr": "vector_int_push_all",
        "in": {"vector_int": [IntVector([])]},
        "ex": {"vector_int": [], "int": []}
    },
    {
        "instr": "vector_bool_empty_vector",
        "in": {"vector_bool": [BoolVector([])]},
        "ex": {"vector_bool": [], "bool": [True]}
    },
    {
        "instr": "vector_bool_empty_vector",
        "in": {"vector_bool": [BoolVector([False])]},
        "ex": {"vector_bool": [], "bool": [False]}
    },
    {
        "instr": "vector_bool_contains",
        "in": {"vector_bool": [BoolVector([False])], "bool": [False]},
        "ex": {"vector_bool": [], "bool": [True]}
    },
    {
        "instr": "vector_bool_contains",
        "in": {"vector_bool": [BoolVector([False])], "bool": [True]},
        "ex": {"vector_bool": [], "bool": [False]}
    },
    {
        "instr": "vector_int_index_of",
        "in": {"vector_int": [IntVector([0, 5, 100])], "int": [5]},
        "ex": {"vector_int": [], "int": [1]}
    },
    {
        "instr": "vector_int_index_of",
        "in": {"vector_int": [IntVector([0, -5, 100])], "int": [5]},
        "ex": {"vector_int": [], "int": [-1]}
    },
    {
        "instr": "vector_int_index_of",
        "in": {"vector_int": [IntVector([])], "int": [5]},
        "ex": {"vector_int": [], "int": [-1]}
    },
    {
        "instr": "vector_int_occurrences_of",
        "in": {"vector_int": [IntVector([0, 5, 100])], "int": [5]},
        "ex": {"vector_int": [], "int": [1]}
    },
    {
        "instr": "vector_int_occurrences_of",
        "in": {"vector_int": [IntVector([5, 5, 5])], "int": [5]},
        "ex": {"vector_int": [], "int": [3]}
    },
    {
        "instr": "vector_int_occurrences_of",
        "in": {"vector_int": [IntVector([])], "int": [5]},
        "ex": {"vector_int": [], "int": [0]}
    },
    {
        "instr": "vector_int_occurrences_of",
        "in": {"vector_int": [IntVector([-5])], "int": [5]},
        "ex": {"vector_int": [], "int": [0]}
    },
    {
        "instr": "vector_int_occurrences_of",
        "in": {"vector_int": [IntVector([-5])], "int": [5]},
        "ex": {"vector_int": [], "int": [0]}
    },
    {
        "instr": "vector_int_set_nth",
        "in": {"vector_int": [IntVector([0, 10, 100])], "int": [5, 1]},
        "ex": {"vector_int": [IntVector([0, 5, 100])], "int": []}
    },
    {
        "instr": "vector_int_set_nth",
        "in": {"vector_int": [IntVector([0, 10, 100])], "int": [5, 4]},
        "ex": {"vector_int": [IntVector([0, 5, 100])], "int": []}
    },
    {
        "instr": "vector_int_set_nth",
        "in": {"vector_int": [IntVector([])], "int": [5, 1]},
        "ex": {"vector_int": [IntVector([])], "int": []},
    },
    {
        "instr": "vector_str_replace",
        "in": {"vector_str": [StrVector(["a", "b", "c", "b"])], "str": ["z", "b"]},
        "ex": {"vector_str": [StrVector(["a", "z", "c", "z"])], "str": []},
    },
    {
        "instr": "vector_str_replace",
        "in": {"vector_str": [StrVector(["a", "b", "c", "b"])], "str": ["b", "z"]},
        "ex": {"vector_str": [StrVector(["a", "b", "c", "b"])], "str": []},
    },
    {
        "instr": "vector_str_replace",
        "in": {"vector_str": [StrVector([])], "str": ["z", "b"]},
        "ex": {"vector_str": [StrVector([])], "str": []},
    },
    {
        "instr": "vector_str_replace_first",
        "in": {"vector_str": [StrVector(["a", "b", "c", "b"])], "str": ["z", "b"]},
        "ex": {"vector_str": [StrVector(["a", "z", "c", "b"])], "str": []},
    },
    {
        "instr": "vector_str_replace_first",
        "in": {"vector_str": [StrVector(["a", "b", "c", "b"])], "str": ["b", "z"]},
        "ex": {"vector_str": [StrVector(["a", "b", "c", "b"])], "str": []},
    },
    {
        "instr": "vector_str_replace_first",
        "in": {"vector_str": [StrVector([])], "str": ["z", "b"]},
        "ex": {"vector_str": [StrVector([])], "str": []},
    },
    {
        "instr": "vector_str_remove",
        "in": {"vector_str": [StrVector(["a", "b", "c", "b"])], "str": ["b"]},
        "ex": {"vector_str": [StrVector(["a", "c"])], "str": []},
    },
    {
        "instr": "vector_str_remove",
        "in": {"vector_str": [StrVector(["a", "b", "c", "b"])], "str": ["z"]},
        "ex": {"vector_str": [StrVector(["a", "b", "c", "b"])], "str": []},
    },
    {
        "instr": "vector_str_remove",
        "in": {"vector_str": [StrVector([])], "str": ["b"]},
        "ex": {"vector_str": [StrVector([])], "str": []},
    },
    {
        "instr": "vector_int_iterate",
        "in": {"vector_int": [], "exec": [IM("int_inc", 0)]},
        "ex": {"vector_int": [], "exec": [IM("int_inc", 0)]},
    },
    {
        "instr": "vector_int_iterate",
        "in": {"vector_int": [IntVector([0, 10, 100])], "exec": []},
        "ex": {"vector_int": [IntVector([0, 10, 100])], "exec": []},
    },
    {
        "instr": "vector_int_iterate",
        "in": {"vector_int": [IntVector([])], "exec": [IM("int_inc", 0)]},
        "ex": {"vector_int": [], "exec": []},
    },
    {
        "instr": "vector_int_iterate",
        "in": {"vector_int": [IntVector([100])], "exec": [IM("int_inc", 0)]},
        "ex": {"vector_int": [], "exec": [IM("int_inc", 0)], "int": [100]},
    },
    {
        "instr": "vector_int_iterate",
        "in": {"vector_int": [IntVector([0, 100])], "exec": [IM("int_inc", 0)]},
        "ex": {
            "vector_int": [],
            "exec": [
                IM("int_inc", 0),
                IM("vector_int_iterate", 1),
                L(IntVector([100]), PushIntVector),
                IM("int_inc", 0)
            ],
            "int": [0]
        },
    },
]
