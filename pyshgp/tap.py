"""The ``Tap`` and ``TapManager`` abstractions allow for users to inject side effects into PyshGP runs.

These side effects could be print statements for monitoring, writing to log files, or sending messages to
external systems when certain events occur. A ``Tap`` can inject a side effect before a function call, after a
function call, or both. Any function or method defined in PyshGP or your application code can be tapped with the
``@tap`` decorator defined in the module.

The taps provided in PyshGP are sufficient for most use cases, but user can define and register their
own ``Tap`` objects via inheritance and method overrides.

"""
import csv
import inspect
import json
import os
from datetime import datetime

import numpy as np
from abc import ABC
from functools import wraps
from typing import Dict, Sequence, Optional, MutableMapping


class Tap(ABC):
    """A debugging/logging abstraction to a function and collects its arguments and returned.

    The methods of a ``Tap`` should be side effects. It is not recommended to make state changes from with a ``Tap`` if
    that state will change code behavior.
    """

    def pre(self, id: str, args, kwargs):
        """Perform a particular side-effect directly before the associated function/method is called.

        Parameters
        ----------
        id : str
            The ID of the tap, generated based off of the name qualified name of the function.
        args : list
            The positional of the function call. For methods, ``args[0]`` is the class instance.
        kwargs : dict
            The keyword args of the function call.

        """
        pass

    def post(self, id: str, args, kwargs, returned):
        """Perform a particular side-effect directly before the associated function/method is called.

        Parameters
        ----------
        id : str
            The ID of the tap, generated based off of the name qualified name of the function.
        args : list
            The positional of the function call. For methods, ``args[0]`` is the class instance.
        kwargs : dict
            The keyword args of the function call.
        returned : Any
            The returned value of the function call.

        """
        pass

    def do(self, id: str, *args, **kwargs):
        """Perform a particular side-effect when called.

        Parameters
        ----------
        id : str
            The ID of the tap.

        """
        pass


class LogFileTap(Tap):
    """A ``Tap`` for writing log files.

    Parameters
    ----------
    root : str
        The root directory for putting log files (and directories).

    """

    # @todo Make log timestamps configurable.

    def __init__(self, root: str):
        self.root = root

    def dir(self, id: str) -> str:
        """Generate the directory for log files associated with the given function ID."""
        return os.path.join(self.root, id.replace(".", os.path.sep))

    def path(self, id: str, filename: str) -> str:
        """Generate the path for the log files with the given name under the directory for the given function ID."""
        return os.path.join(self.dir(id), filename)

    def log(self, id: str, filename: str, line: str):
        """Write a line to a log file. Includes a timestamp for each log entry.

        Parameters
        ----------
        id : str
            The ID of the function being tapped. This is used to generate a directory for the log file.
        filename : str
            The name of the log file.
        line : str
            The line of text to write to the log file.

        """
        path = self.path(id, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(self.path(id, filename), "a") as f:
            f.write(str(datetime.now()))
            f.write("\t")
            f.write(line)
            f.write("\n")


class CsvTap(LogFileTap):
    """A ``Tap`` for writing CSV files.

    Parameters
    ----------
    root : str
        The root directory for putting log files (and directories).
    column_names : Sequence[str]
        The column names to put in the header of the CSV file.

    """

    def __init__(self, root: str, column_names: Sequence[str]):
        super().__init__(root)
        self.column_names = column_names

    def log(self, id: str, filename: str, row: Dict):
        """Write a to a CSV file.

        Parameters
        ----------
        id : str
            The ID of the function being tapped. This is used to generate a directory for the log file.
        filename : str
            The name of the CSV file.
        row : dict
            A dictionary that will be written as a row in the CSV. The keys should be in the
            CsvTap's list of ``column_names``.

        """
        path = self.path(id, filename)
        is_new = not os.path.exists(path)
        if is_new:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a") as f:
            writer = csv.DictWriter(f, fieldnames=self.column_names)
            if is_new:
                writer.writeheader()
            writer.writerow(row)


class JsonLinesTap(LogFileTap):
    """A ``Tap`` for writing JSON lines files.

    Parameters
    ----------
    root : str
        The root directory for putting log files (and directories).

    """

    def __init__(self, root: str):
        super().__init__(root)

    def log(self, id: str, filename: str, row: Dict):
        """Write a JSON object to a line of a JSON lines file.

        Parameters
        ----------
        id : str
            The ID of the function being tapped. This is used to generate a directory for the log file.
        filename : str
            The name of the JSON file.
        row : dict
            A dictionary that will be written as a row in the file.

        """
        path = self.path(id, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a") as f:
            f.writelines([json.dumps(row)])


class StdOutRun(Tap):
    """A ``Tap`` that prints information from a ``SearchAlgorithm`` run to stdout.

    Parameters
    ----------
    pre_print_config : bool, optional
        If True, print the PushConfig before each run. Default False.
    pre_print_atoms : bool, optional
        If True, print all the atoms used to generate programs before each run. Default False.
    post_print_best : bool, optional
        If True, print a summary about the best program found at the end of each run. Default False.

    """

    def __init__(self, *,
                 pre_print_config: bool = False,
                 pre_print_atoms: bool = False,
                 post_print_best: bool = False):
        self.pre_print_config = pre_print_config
        self.pre_print_atoms = pre_print_atoms
        self.post_print_best = post_print_best

    def pre(self, id: str, args, kwargs, obj=None):
        """Print run config and/or all atoms to stdout."""
        search = args[0]
        if self.pre_print_config:
            print("Search Configuration:")
            attrs = ["signature", "evaluator", "spawner", "population_size", "max_generations", "error_threshold",
                     "initial_genome_size", "simplification_steps", "parallel_context", "selection", "variation"]
            for attr in attrs:
                print(attr + ":", getattr(search.config, attr))
        if self.pre_print_atoms:
            print("Instructions:")
            print(", ".join([i for i in search.config.spawner.instruction_set.keys()]))
            print("Literals:")
            print(search.config.spawner.literals)
            print("ERC Generators:")
            print(search.config.spawner.erc_generators)

    def post(self, id: str, args, kwargs, returned, obj=None):
        """Print a summary of the run result to stdout."""
        search = args[0]
        if search.is_solved():
            print("Solution found.")
        else:
            print("No solution found.")

        if self.post_print_best:
            print("Best individual found:")
            print("Genome:", search.best_seen.genome)
            print("Program:", search.best_seen.program)
            print("Error vector:", search.best_seen.error_vector)
            print("Total error:", search.best_seen.total_error)


class StdOutSearchStepTap(Tap):
    """A ``Tap`` that prints stats from a step (aka generation) of a ``SearchAlgorithm`` run."""

    def __init__(self, every_n_steps: int):
        self.every_n_steps = every_n_steps

    def pre(self, id: str, args, kwargs, obj=None):
        """Print population stats before the next step of the run."""
        search = args[0]
        generation = search.generation
        if generation % self.every_n_steps == 0:
            print(" | ".join([
                str(datetime.now()),
                "GENERATION: {g}".format(
                    g=generation
                ),
                "ERRORS: best={b}, median={m}, diversity={e_d}".format(
                    b=search.population.best().total_error,
                    m=search.population.median_error(),
                    e_d=search.population.error_diversity()
                ),
                "INDIVIDUALS: n={ps}, avg_genome_length={gn_len}".format(
                    ps=len(search.population),
                    gn_len=search.population.mean_genome_length()
                ),
            ]))


class StdOutSimplification(Tap):
    """A ``Tap`` that prints a summary of Genome simplification."""

    def pre(self, id: str, args, kwargs, obj=None):
        """Print a notification that genome simplification is starting."""
        genome = args[1]
        print("Simplifying genome of length {ln} with total error {er}.".format(
            ln=len(genome),
            er=np.sum(args[2])
        ))

    def post(self, id: str, args, kwargs, returned, obj=None):
        """Print a summary of the result of genome simplification."""
        gn, errs = returned
        print("Simplified genome to length {ln} and total error {er}.".format(
            ln=len(gn),
            er=np.sum(errs.sum())
        ))


class StdOutSimplificationStep(Tap):
    """A ``Tap`` that prints a notification of a successful Genome simplification step."""

    def post(self, id: str, args, kwargs, returned, obj=None):
        """Print a notification of a successful step of Genome simplification."""
        orig_gn = args[1]
        new_gn = returned[0]
        orig_len = len(orig_gn)
        new_len = len(new_gn)
        if new_len < orig_len:
            print("Simplified genome by {diff} to length {ln}.".format(
                diff=orig_len - new_len,
                ln=new_len
            ))


class TapManager:
    """Stores a mapping of function ID to ``Tap`` object than can be used to inject side effects around functions.

    The ``TapManger`` class is treated as a singleton and should not be instanced. Its methods are static and the state
    they manage is shared between all usages of ``Taps``.

    Function IDs are a fully qualified identifier for a function. They are generated as the concatenation
    of the module name the function is defined in (ie. ``my_package.my_module``) and the qualified name of the function
    definition (ie. ``MyClass.my_method``). The final function ID would be ``my_package.my_module.MyClass.my_method``.

    """

    _taps: MutableMapping[str, Tap] = {}

    # @todo multiple Taps per ID? CompositeTap type?

    @staticmethod
    def register(id: str, tap: Tap):
        """Register a ``Tap`` to be performed when the function with the associated ID is called."""
        TapManager._taps[id] = tap

    @staticmethod
    def unregister(id: str):
        """Unregister the ``Tap`` associated with given ID."""
        if id in TapManager._taps:
            del TapManager._taps[id]

    @staticmethod
    def get(id: str) -> Optional[Tap]:
        """Return the ``Tap`` associated with given ID or ``None`` if no tap is registered."""
        if id in TapManager._taps:
            return TapManager._taps[id]
        return None

    @staticmethod
    def do(id: str, *args, **kwargs):
        """Perform the ``do`` method of the tap registered under the given ID.

        This can be called from any location.
        """
        if id in TapManager._taps:
            TapManager._taps[id].do(id, *args, **kwargs)
        else:
            raise KeyError("No Tap registered in TapManager with id " + id)


def tap(fn):
    """Decorate a function/method to call any associated taps that have been registered in the ``TapManager``.

    Functional behavior is not changed.

    """
    fn_id = inspect.getmodule(fn).__name__ + "." + fn.__qualname__

    @wraps(fn)
    def tapped(*args, **kwargs):
        tap = TapManager.get(fn_id)
        if tap is not None:
            tap.pre(fn_id, args, kwargs)
        result = fn(*args, **kwargs)
        if tap is not None:
            tap.post(fn_id, args, kwargs, result)
        return result

    return tapped


def set_verbosity(level: int):
    """Register some ``Tap`` objects in the ``TapManger`` that print to stdout during an evolutionary run.

    Verbosity level 0 prints nothing to stdout.

    Verbosity level 1 prints minimal run configuration as well as population statistics every 5 generations.

    Verbosity level 2+ prints full run configuration, population statics every generation, and traces the genome
    simplification process.

    """
    if level > 0:
        TapManager.register("pyshgp.gp.genome.GenomeSimplifier.simplify", StdOutSimplification())

    if level == 1:
        TapManager.register("pyshgp.gp.search.SearchAlgorithm.step", StdOutSearchStepTap(every_n_steps=5))
        TapManager.register("pyshgp.gp.search.SearchAlgorithm.run", StdOutRun(pre_print_config=True,
                                                                              pre_print_atoms=False,
                                                                              post_print_best=False))
    if level > 1:
        TapManager.register("pyshgp.gp.search.SearchAlgorithm.step", StdOutSearchStepTap(every_n_steps=1))
        TapManager.register("pyshgp.gp.search.SearchAlgorithm.run", StdOutRun(pre_print_config=True,
                                                                              pre_print_atoms=True,
                                                                              post_print_best=True))
        TapManager.register("pyshgp.gp.genome.GenomeSimplifier._step", StdOutSimplificationStep())
