"""The :mod:`individual` module defines an Individaul in an evolutionary population.

Individuals are made up of Genomes, which are the linear Push program
representations which can be manipulated by seach algorithms.

"""
from typing import Union

import numpy as np

from pyshgp.push.atoms import CodeBlock
from pyshgp.gp.genome import Genome


class Individual:
    """An individual in an evolutionary population.

    Attributes
    ----------
    genome : Genome
        The Genome of the Individual.
    program : CodeBlock
        The CodeBlock produced by translating the Individual's genome.
    error_vector : np.array
        An array of error values produced by evaluating the Individual's program.
    total_error : float
        The sum of all error values in the Individaul's error_vector.
    error_vector_bytes:
        Hashable Byte representation of the individual's error vector.

    """

    __slots__ = ["_genome", "_program", "_error_vector", "_total_error", "_error_vector_bytes"]

    def __init__(self, genome: Genome = Genome):
        self._genome = genome
        self._program = None
        self._error_vector = None
        self._total_error = None
        self._error_vector_bytes = None

    @property
    def genome(self) -> Genome:
        """Plush Genome of individual."""
        return self._genome

    @genome.setter
    def genome(self, value: Genome):
        self._genome = value

    @property
    def program(self) -> CodeBlock:
        """Push program of individual. Taken from Plush genome."""
        if self._program is None:
            self._program = self.genome.to_code_block()
        return self._program

    @program.setter
    def program(self, value: CodeBlock):
        raise AttributeError("Cannot set program directly. Must set genome.")

    @property
    def error_vector(self) -> np.ndarray:
        """Numpy array of numeric error values."""
        return self._error_vector

    @error_vector.setter
    def error_vector(self, error_vector: np.ndarray):
        self._error_vector = error_vector

    @property
    def total_error(self) -> Union[np.int64, np.float64]:
        """Numeric sum of the error vector."""
        if self._total_error is None:
            try:
                self._total_error = np.sum(self.error_vector)
            except OverflowError:
                self._total_error = np.inf
        return self._total_error

    @total_error.setter
    def total_error(self, value: Union[np.int64, np.float64]):
        raise AttributeError("Cannot set total_error directly. Must set error_vector.")

    @property
    def error_vector_bytes(self):
        """Hashable Byte representation of the individual's error vector."""
        if self._error_vector_bytes is None:
            self._error_vector_bytes = self._error_vector.data.tobytes()
        return self._error_vector_bytes

    @error_vector_bytes.setter
    def error_vector_bytes(self, value):
        raise AttributeError("Cannot set error_vector_bytes directly. Must set error_vector.")

    def __lt__(self, other):
        return self.total_error < other.total_error
