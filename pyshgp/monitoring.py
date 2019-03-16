"""Verbosity configuration."""
from typing import Union, Callable
from logging import info, debug


# @TODO: Add verbosity of serach config
# @TODO: Add verbosity of start time, end time, and runtime.

class VerbosityConfig:
    """Collection of indicators for what should be logged in a run."""

    def __init__(self,
                 solution_found: Union[bool, Callable] = False,
                 generation: Union[bool, Callable] = False,
                 every_n_generations: int = 1,
                 simplification: Union[bool, Callable] = False,
                 simplification_step: Union[bool, Callable] = False,
                 program_trace: Union[bool, Callable] = False):
        self.solution_found = solution_found
        self.generation = generation
        self.every_n_generations = every_n_generations
        self.simplification = simplification
        self.simplification_step = simplification_step
        self.program_trace = program_trace


DEFAULT_VERBOSITY_LEVELS = [
    VerbosityConfig(),
    VerbosityConfig(
        solution_found=info,
        generation=info,
        every_n_generations=5,
        simplification=info,
        simplification_step=debug
    ),
    VerbosityConfig(
        solution_found=info,
        generation=info,
        simplification=info,
        simplification_step=info,
        program_trace=debug
    )
]
