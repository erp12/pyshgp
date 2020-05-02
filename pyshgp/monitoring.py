"""Verbosity configuration."""
from typing import Union, Callable

import logging

# @TODO: Add logging of search config to verbosity
# @TODO: Add logging of start time, end time, and runtime to verbosity


class VerbosityConfig:
    """Collection of indicators for what should be logged in a run."""

    def __init__(self,
                 solution_found: Union[bool, int] = False,
                 generation: Union[bool, int] = False,
                 every_n_generations: int = 1,
                 simplification: Union[bool, int] = False,
                 simplification_step: Union[bool, int] = False,
                 program_trace: Union[bool, int] = False):
        self.log_level = logging.getLogger().getEffectiveLevel()
        self.update_log_level()
        self.solution_found = solution_found
        self.generation = generation
        self.every_n_generations = every_n_generations
        self.simplification = simplification
        self.simplification_step = simplification_step
        self.program_trace = program_trace

    def update_log_level(self):
        """Store the log level set by the user."""
        self.log_level = logging.getLogger().getEffectiveLevel()


DEFAULT_VERBOSITY_LEVELS = [
    VerbosityConfig(),
    VerbosityConfig(
        solution_found=logging.INFO,
        generation=logging.INFO,
        every_n_generations=5,
        simplification=logging.INFO,
        simplification_step=logging.DEBUG
    ),
    VerbosityConfig(
        solution_found=logging.INFO,
        generation=logging.INFO,
        simplification=logging.INFO,
        simplification_step=logging.INFO,
        program_trace=logging.DEBUG
    )
]


def log_function(level: int) -> Callable:
    """Return corresponding log function."""
    _lvl2func = {
        10: logging.debug,
        20: logging.info,
        30: logging.warning,
        40: logging.error,
        50: logging.critical,
    }
    return _lvl2func.get(level, None)


def log(level: int, msg, *args, **kwargs):
    """Log the given message at the given log level. See ``logger`` lib."""
    f = log_function(level)
    if f is not None:
        f(msg, *args, **kwargs)
