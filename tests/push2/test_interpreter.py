import pickle

from pyshgp.push2.interpreter import Program, Signature, Config
from pyshgp.push2.unit import *


class TestInterpreter:
    def test_step_limit(self):
        pass

    def test_growth_limit(self):
        pass

    def test_state_size_limit(self):
        pass

    def test_number_magnitude_limit(self):
        pass

    def test_collection_size_limit(self):
        pass

    def test_eval_intruction(self):
        pass

    def test_eval_input(self):
        pass

    def test_eval_block(self):
        pass

    def test_eval_lit(self):
        pass


class TestProgram:
    def test_call_program(self):
        pass

    def test_missing_args(self):
        pass

    def test_empty_code(self):
        pass

    def test_pickle(self):
        in_prog = Program(
            signature=Signature(
                inputs={"a": "int", "b": "float"},
                outputs=("C",),
            ),
            code=Block(
                [
                    Lit(1, "int"),
                    Input("a"),
                    Instr("int_add"),
                    Instr("float_from_int"),
                    Block(
                        [
                            Input("b"),
                            Instr("float_mult"),
                        ]
                    ),
                ]
            ),
            config=Config(),
        )
        pckl = pickle.dumps(in_prog)
        out_prog = pickle.loads(pckl)
        assert in_prog == out_prog
