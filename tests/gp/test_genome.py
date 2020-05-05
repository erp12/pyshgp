import pytest
from pyrsistent import InvariantException

from pyshgp.gp.genome import Opener, _has_opener, genome_to_code, Genome, GenomeSimplifier
from pyshgp.gp.evaluation import DatasetEvaluator
from pyshgp.push.atoms import Atom, Literal, Instruction, CodeBlock
from pyshgp.push.types import PushInt, PushBool


def test_opener():
    o = Opener(count=2)
    assert o.count == 2
    o = o.dec()
    assert o.count == 1


def test__has_opener():
    lst = ["_" for x in range(5)]
    assert not _has_opener(lst)
    lst[2] = Opener(count=1)
    assert _has_opener(lst)


class TestGenome:

    def test_genome_bad_init(self, atoms):
        with pytest.raises(InvariantException):
            Genome(CodeBlock(*[atoms["5"], [atoms["5"], atoms["add"]]]))

    def test_missing_close_genome_to_codeblock(self, atoms):
        gn = Genome([atoms["true"], atoms["if"], atoms["1.2"], atoms["close"], atoms["5"]])
        cb = genome_to_code(gn)
        assert cb[0] == Literal(True, PushBool)
        assert isinstance(cb[1], Instruction)
        assert isinstance(cb[2], CodeBlock)

    def test_extra_close_genome_to_codeblock(self, atoms):
        gn = Genome([atoms["close"], atoms["5"], atoms["close"], atoms["close"]])
        cb = genome_to_code(gn)
        assert len(cb) == 1
        assert cb[0] == Literal(5, PushInt)

    def test_empty_genome_to_codeblock(self):
        gn = Genome()
        cb = genome_to_code(gn)
        assert len(cb) == 0


class TestGeneSpawner:

    def test_random_instruction(self, simple_gene_spawner):
        assert isinstance(simple_gene_spawner.random_instruction(), Instruction)

    def test_random_literal(self, simple_gene_spawner):
        assert isinstance(simple_gene_spawner.random_literal(), Literal)

    def test_random_erc(self, simple_gene_spawner):
        assert isinstance(simple_gene_spawner.random_erc(), Literal)

    def test_random_gene(self, simple_gene_spawner):
        assert isinstance(simple_gene_spawner.random_gene(), Atom)

    def test_spawn_genome(self, simple_gene_spawner):
        gn = simple_gene_spawner.spawn_genome(10)
        assert isinstance(gn, Genome)
        assert len(gn) == 10

    def test_spawn_var_length_genome(self, simple_gene_spawner):
        gn = simple_gene_spawner.spawn_genome((8, 10))
        assert isinstance(gn, Genome)
        assert len(gn) >= 8
        assert len(gn) <= 10


class TestGenomeSimplifier:

    def test_simplify_no_change(self, simple_individual):
        evaluator = DatasetEvaluator([[]], [10])
        genome = simple_individual.genome
        err = evaluator.evaluate(simple_individual.program)

        gs = GenomeSimplifier(evaluator, simple_individual.signature)
        new_genome, new_err = gs.simplify(genome, err, 100)

        assert genome == new_genome
        assert new_err == [0.0]

    def test_simplify(self, simple_individual, atoms):
        evaluator = DatasetEvaluator([[]], [5])
        genome = simple_individual.genome
        err = evaluator.evaluate(simple_individual.program)

        gs = GenomeSimplifier(evaluator, simple_individual.signature)
        new_genome, new_err = gs.simplify(genome, err, 1000)

        assert new_genome == Genome([atoms["5"]])
        assert new_err == [0.0]
