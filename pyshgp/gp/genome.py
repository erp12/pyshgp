"""The :mod:`genome` module defines classes related to Genomesself.

The ``Genome`` class defines Genomes as flat, linear representations of Push
programs. The ``GenomeSpawner`` class is a factory of random genes (``Atoms``)
and random ``Genomes``.

"""
from collections import MutableSequence
from typing import Callable, Sequence, Union, Tuple, Optional, Any

import numpy as np

from pyshgp.push.interpreter import ProgramSignature, Program
from pyshgp.push.type_library import infer_literal
from pyshgp.push.atoms import Atom, Closer, Literal, Instruction, CodeBlock
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.gp.evaluation import Evaluator
from pyshgp.utils import DiscreteProbDistrib, Saveable, Copyable
from pyshgp.monitoring import VerbosityConfig, DEFAULT_VERBOSITY_LEVELS, log


class Opener:
    """Marks the start of one or more CodeBlock."""

    __slots__ = ["count"]

    def __init__(self, count: int):
        self.count = count

    def dec(self):
        """Decrements the count by 1."""
        self.count -= 1


def _has_opener(l: Sequence) -> bool:
    return sum([isinstance(_, Opener) for _ in l]) > 0


class Genome(MutableSequence, Saveable, Copyable):
    """A flat sequence of Atoms where each Atom is a "gene" in the genome."""

    def __init__(self, atoms: Sequence[Atom] = None):
        self.list = []
        if atoms is not None:
            for el in atoms:
                self.append(el)

    def __getitem__(self, i: int) -> Any:
        return self.list.__getitem__(i)

    def __setitem__(self, i: int, o: Any) -> None:
        self.list.__setitem__(i, Genome._conform_element(o))

    def __delitem__(self, i: int) -> None:
        self.list.__delitem__(i)

    def __len__(self) -> int:
        return self.list.__len__()

    def __eq__(self, other):
        return isinstance(other, Genome) and self.list == other.list

    def __repr__(self):
        return "Genome" + self.list.__repr__()

    def append(self, atom: Atom) -> None:
        """Append a non-CodeBlock Atom to the end of the Genome."""
        self.list.append(Genome._conform_element(atom))

    def insert(self, index: int, atom: Atom) -> None:
        """Insert Atom before index."""
        self.list.insert(Genome._conform_element(atom))

    @staticmethod
    def _conform_element(el: Any) -> Atom:
        if isinstance(el, CodeBlock):
            raise ValueError("Cannot add CodeBlock to genomes. Genomes must be kept flat.")
        return el

    def to_code_block(self) -> CodeBlock:
        """Translate into nested CodeBlocks.

        These CodeBlocks can be considered the Push program representation of
        the Genome which can be executed by a PushInterpreter and evaluated
        by an Evaluator.

        """
        plushy_buffer = []
        for atom in self:
            plushy_buffer.append(atom)
            if isinstance(atom, Instruction) and atom.code_blocks > 0:
                plushy_buffer.append(Opener(atom.code_blocks))

        push_buffer = []
        while True:
            # If done with plush but unclosed opens, recur with one more close.
            if len(plushy_buffer) == 0 and _has_opener(push_buffer):
                plushy_buffer.append(Closer())
            # If done with plush and all opens closed, return push.
            elif len(plushy_buffer) == 0:
                return CodeBlock(*push_buffer)
            else:
                atom = plushy_buffer[0]
                # If next instruction is a close, and there is an open.
                if isinstance(atom, Closer) and _has_opener(push_buffer):
                    ndx, opener = [(ndx, el) for ndx, el in enumerate(push_buffer) if isinstance(el, Opener)][-1]
                    post_open = push_buffer[ndx + 1:]
                    pre_open = push_buffer[:ndx]
                    if opener.count == 1:
                        push_buffer = pre_open + [post_open]
                    else:
                        opener.dec()
                        push_buffer = pre_open + [post_open, opener]
                # If next instruction is a close, and there is no open.
                elif not isinstance(atom, Closer):
                    push_buffer.append(atom)
                del plushy_buffer[0]

    def make_str(self) -> str:
        """Create one simple str representation of the Genome."""
        return " ".join([str(gene) for gene in self])


class GeneSpawner:
    """A factory of random Genes (Atoms) and Genomes.

    When  spawning a random gene, the result can be one of three types of Atoms.
    An Instruction, a Closer, or a Literal. If the Atom is a Literal, it may
    be one of the supplied Literals, or it may be the result of running one of
    the Ephemeral Random Constant generators.

    Reference for ERCs:
    "A field guide to genetic programming", Section 3.1
    Riccardo Poli and William B. Langdon and Nicholas Freitag McPhee,
    http://www.gp-field-guide.org.uk/

    Parameters
    ----------
    instruction_set : pyshgp.push.instruction_set.InstructionSet
        InstructionSet containing instructions to use when spawning genes and
        genomes.
    literals : Sequence[pyshgp.push.instruction_set.atoms.Literal, Any]
        A list of Literal objects to pull from when spawning genes and genomes.
        If an element of ``literals`` is not an instance of Literal, an attempt
        to wrap the value in a Literal will be made.
    erc_generator : Sequence[Callable]
        A list of functions (aka Ephemeral Random Constant generators). When one
        of these functions is called, the output is placed in a Literal and
        returned as the spawned gene.
    distribution : pyshgp.utils.DiscreteProbDistrib, optional
        A probability distribution describing how frequently to produce
        Instructions, Closers, Literals, and ERCs. The default is "proportional"
        which gives all Instructions, Literals, and ERC generators equal probability.
        If "proportional", the likelyhood of producing a Closer is the same as
        the likelyhood of producing an Instruction with opens a code block.

    Attributes
    ----------
    instruction_set : pyshgp.push.instruction_set.InstructionSet
        InstructionSet containing instructions to use when spawning genes and
        genomes.
    literals : Sequence[pyshgp.push.instruction_set.atoms.Literal]
        A list of Literal objects to pull from when spawning genes and genomes.
    erc_generator : Sequence[Callable]
        A list of functions (aka Ephemeral Random Constant generators). When one
        of these functions is called, the output is placed in a Literal and
        returned as the spawned gene.
    distribution : pyshgp.utils.DiscreteProbDistrib
        A probability distribution describing how frequently to produce
        Instructions, Closers, Literals, and ERCs.

    """

    def __init__(self,
                 instruction_set: InstructionSet,
                 literals: Sequence[Union[Literal, Any]],
                 erc_generators: Sequence[Callable],
                 distribution: DiscreteProbDistrib = "proportional"):
        self.instruction_set = instruction_set
        self.type_library = instruction_set.type_library
        self.literals = [lit if isinstance(lit, Literal) else infer_literal(lit, self.type_library) for lit in literals]
        self.erc_generators = erc_generators

        if distribution == "proportional":
            self.distribution = (
                DiscreteProbDistrib()
                .add("instruction", len(instruction_set))
                .add("close", sum([i.code_blocks for i in instruction_set.values()]))
                .add("literal", len(literals))
                .add("erc", len(erc_generators))
            )
        else:
            self.distribution = distribution

    def random_instruction(self) -> Instruction:
        """Return a random Instruction from the InstructionSet.

        Returns
        -------
        pushgp.push.atoms.Instruction
            A randomly selected Literal.

        """
        return np.random.choice(list(self.instruction_set.values()))

    def random_literal(self) -> Literal:
        """Return a random Literal from the set of Literals.

        Returns
        -------
        pushgp.push.atoms.Literal
            A randomly selected Literal.

        """
        lit = np.random.choice(self.literals)
        if not isinstance(lit, Literal):
            lit = infer_literal(lit, self.type_library)
        return lit

    def random_erc(self) -> Literal:
        """Materialize a random ERC generator into a Literal and return it.

        Returns
        -------
        pushgp.push.atoms.Literal
            A Literal whose value comes from running a ERC generator function.

        """
        erc_value = np.random.choice(self.erc_generators)()
        if not isinstance(erc_value, Literal):
            erc_value = infer_literal(erc_value, self.type_library)
        return erc_value

    def spawn_atom(self) -> Atom:
        """Return a random Atom based on the GenomeSpawner's distribution.

        Returns
        -------
        pushgp.push.atoms.Atom
            An random Atom. Either an Instruction, Closer, or Literal.

        """
        atom_type = self.distribution.sample()
        if atom_type == "instruction":
            return self.random_instruction()
        elif atom_type == "close":
            return Closer()
        elif atom_type == "literal":
            return self.random_literal()
        elif atom_type == "erc":
            return self.random_erc()
        else:
            raise ValueError("GenomeSpawner distribution bad atom type {t}".format(t=str(atom_type)))

    def spawn_genome(self, size: Union[int, Sequence[int]]) -> Genome:
        """Return a random Genome based on the GenomeSpawner's distribution.

        The genome will contain the specified number of Atoms if size is an
        integer. If size is a pair of integers, the genome will be of a random
        size in the range of the two integers.

        Parameters
        ----------
        size
            The resulting genome will contain this many Atoms if size is an
            integer. If size is a pair of integers, the genome will be of a random
            size in the range of the two integers.

        Returns
        -------
        pushgp.gp.genome.Genome
            A Genome with random contents of a given size.

        """
        if isinstance(size, Sequence):
            size = np.random.randint(size[0], size[1]) + 1

        gn = Genome()
        for ndx in range(size):
            gn.append(self.spawn_atom())

        return gn


class GenomeSimplifier:
    """Simplifies a genome while preserving, or improving, its error.

    Genomes, and Push programs, can contain superfluous Push code. This extra
    code often has no effect on the program behavior, but occasionally it can
    introduce subtle errors or behaviors that is not covered by the training
    cases. Removing the superfluous code makes genomes (and thus programs)
    smaller and easier to understand. More importantly, simplification can
    imporve the generalization of the given genome/program.

    The process of geneome simplification is iterative and closely resembles
    simple hill climbing. For each iteration, the simplifier will randomly
    select a small number of random genes to remove. The Genome is re-evaluated
    and if its error gets worse, the change is reverted. After repeating this
    for some number of steps, the resulting genome will be the same size or
    smaller while containing the same (or better) error value.

    Reference:
    "Improving generalization of evolved programs through automatic simplification"
    Thomas Helmuth, Nicholas Freitag McPhee, Edward Pantridge, and Lee Spector. 2017.
    In Proceedings of the Genetic and Evolutionary Computation Conference (GECCO '17).
    ACM, New York, NY, USA, 937-944. DOI: https://doi.org/10.1145/3071178.3071330

    https://dl.acm.org/citation.cfm?id=3071178.3071330

    """

    # @TODO: Add noop swaps to simplification.

    def __init__(self,
                 evaluator: Evaluator,
                 program_signature: ProgramSignature,
                 verbosity_config: Optional[VerbosityConfig] = None):
        self.evaluator = evaluator
        self.program_signature = program_signature
        self.verbosity_config = verbosity_config

    def _remove_rand_genes(self, genome: Genome) -> Genome:
        gn = genome.copy(deep=True)
        n_genes_to_remove = min(np.random.randint(1, 4), len(genome) - 1)
        ndx_of_genes_to_remove = np.random.choice(np.arange(len(gn)), n_genes_to_remove, replace=False)
        ndx_of_genes_to_remove[::-1].sort()
        for ndx in ndx_of_genes_to_remove:
            del gn[ndx]
        return gn

    def _errors_of_genome(self, genome: Genome) -> np.ndarray:
        cb = genome.to_code_block()
        program = Program(cb, self.program_signature)
        return self.evaluator.evaluate(program)

    def _step(self, genome: Genome, errors_to_beat: np.ndarray) -> Tuple[Genome, np.ndarray]:
        new_gn = self._remove_rand_genes(genome)
        new_errs = self._errors_of_genome(new_gn)
        if np.sum(new_errs) <= np.sum(errors_to_beat):
            if self.verbosity_config.simplification_step >= self.verbosity_config.log_level:
                log(
                    self.verbosity_config.simplification_step,
                    "Simplified to length {ln}.".format(ln=len(new_gn))
                )
            return new_gn, new_errs
        return genome, errors_to_beat

    def simplify(self,
                 genome: Genome,
                 original_errors: np.ndarray,
                 steps: int = 2000) -> Tuple[Genome, np.ndarray]:
        """Simplify the given genome while maintaining error.

        Parameters
        ----------
        genome
            The Genome to simplifiy.
        original_errors
            Error vector of the genome to simplify.
        steps
            Number of simplification iterations to perform. Default is 2000.

        Returns
        -------
        pushgp.gp.genome.Genome
            A Genome with random contents of a given size.

        """
        if self.verbosity_config is None:
            self.verbosity_config = DEFAULT_VERBOSITY_LEVELS[0]
        if self.verbosity_config.simplification_step >= self.verbosity_config.log_level:
            log(
                self.verbosity_config.simplification,
                "Simplifying genome of length {ln}.".format(ln=len(genome))
            )
        gn = genome
        errs = original_errors
        for step in range(steps):
            gn, errs = self._step(gn, errs)
            if len(gn) == 1:
                break

        if self.verbosity_config.simplification_step >= self.verbosity_config.log_level:
            log(
                self.verbosity_config.simplification,
                "Simplified genome length {ln}.".format(ln=len(gn))
            )
            log(
                self.verbosity_config.simplification,
                "Simplified genome total error {te}.".format(te=np.sum(errs))
            )

        return gn, errs
