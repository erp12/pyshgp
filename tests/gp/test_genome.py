import pytest

import random

from pyshgp.gp.genome import Opener, _has_opener, Genome, GeneSpawner, GenomeSimplifier
from pyshgp.gp.evaluation import DatasetEvaluator
from pyshgp.push.atoms import Atom, Literal, Instruction, CodeBlock
from pyshgp.push.instruction_set import InstructionSet


@pytest.fixture(scope="function")
def simple_genome_spawner(atoms):
    i_set = InstructionSet()
    i_set.register_list([atoms["add"], atoms["sub"], atoms["if"]])
    l_set = [atoms["5"], atoms["1.2"], atoms["true"]]
    return GeneSpawner(i_set, l_set, [random.random])


def test_opener():
    o = Opener(2)
    assert o.count == 2
    o.dec()
    assert o.count == 1


def test__has_opener():
    lst = ["_" for x in range(5)]
    assert not _has_opener(lst)
    lst[2] = Opener(1)
    assert _has_opener(lst)


class TestGenome:

    def test_genome_bad_init(self, atoms):
        with pytest.raises(ValueError):
            Genome(CodeBlock.from_list([atoms["5"], [atoms["5"], atoms["add"]]]))

    def test_missing_close_genome_to_codeblock(self, atoms):
        gn = Genome([atoms["true"], atoms["if"], atoms["1.2"], atoms["close"], atoms["5"]])
        cb = gn.to_code_block()
        assert cb[0] == Literal(True)
        assert isinstance(cb[1], Instruction)
        assert isinstance(cb[2], CodeBlock)

    def test_extra_close_genome_to_codeblock(self, atoms):
        gn = Genome([atoms["close"], atoms["5"], atoms["close"], atoms["close"]])
        cb = gn.to_code_block()
        assert len(cb) == 1
        assert cb[0] == Literal(5)

    def test_empty_genome_to_codeblock(self, atoms):
        gn = Genome()
        cb = gn.to_code_block()
        assert len(cb) == 0

    def test_genome_write(self, atoms):
        gn = Genome([atoms["true"], atoms["if"], atoms["1.2"], atoms["close"], atoms["5"]])
        s = gn.jsonify()
        assert s == '[{"a":"lit","t":"bool","v":true},{"a":"instr","n":"exec_if"},{"a":"lit","t":"float","v":1.2},{"a":"close"},{"a":"lit","t":"int","v":5}]'


class TestGenomeSpawner:

    def test_random_instruction(self, simple_genome_spawner):
        assert isinstance(simple_genome_spawner.random_instruction(), Instruction)

    def test_random_literal(self, simple_genome_spawner):
        assert isinstance(simple_genome_spawner.random_literal(), Literal)

    def test_random_erc(self, simple_genome_spawner):
        assert isinstance(simple_genome_spawner.random_erc(), Literal)

    def test_spawn_atom(self, simple_genome_spawner):
        assert isinstance(simple_genome_spawner.spawn_atom(), Atom)

    def test_spawn_genome(self, simple_genome_spawner):
        gn = simple_genome_spawner.spawn_genome(10)
        assert isinstance(gn, Genome)
        assert len(gn) == 10

    def test_spawn_var_length_genome(self, simple_genome_spawner):
        gn = simple_genome_spawner.spawn_genome((8, 10))
        assert isinstance(gn, Genome)
        assert len(gn) >= 8
        assert len(gn) <= 10


class TestGenomeSimplifier:

    def test_simplify_no_change(self, simple_genome):
        evaluator = DatasetEvaluator([[]], [10])
        err = evaluator.evaluate(simple_genome.to_code_block())

        gs = GenomeSimplifier(evaluator)
        new_genome, new_err = gs.simplify(simple_genome, err, 100)

        assert simple_genome == new_genome
        assert new_err == [0.0]

    def test_simplify_no_change(self, simple_genome, atoms):
        evaluator = DatasetEvaluator([[]], [5])
        err = evaluator.evaluate(simple_genome.to_code_block())

        gs = GenomeSimplifier(evaluator)
        new_genome, new_err = gs.simplify(simple_genome, err, 100)

        assert new_genome == Genome([atoms["5"]])
        assert new_err == [0.0]
