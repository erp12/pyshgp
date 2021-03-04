# PyshGP

[![PyPI version](https://badge.fury.io/py/pyshgp.svg)](https://badge.fury.io/py/pyshgp)
![PyshGP Tests](https://github.com/erp12/pyshgp/workflows/PyshGP%20Tests/badge.svg)

Push Genetic Programming in Python

> WARNING: The public API of this package may see breaking changes until the 1.0 version. 

## Motivation

### What is PushGP?

Push is programming language that plays nice with evolutionary computing / genetic programming. It is a stack-based language that features 1 stack per data type, including code. Programs are represented by lists of instructions, which modify the values on the stacks. Instructions are executed in order.

More information about PushGP can be found on the [Push Redux](https://erp12.github.io/push-redux/) the [Push Homepage](http://faculty.hampshire.edu/lspector/push.html) and the [Push Language Discourse](https://Push-language.hampshire.edu).

### Why use PushGP?

PushGP is a leading software synthesis (sometimes called "programming by example") system. It utilized stochastic (typically evolutionary) search methods to produce programs that are capable of manipulating all the common data types, control structures, and data structures. It is easily extendable to specific use cases and has seen impressive human-competitive coding results. PushGP has [discovered novel quantum computer programs](http://faculty.hampshire.edu/lspector/aqcp/) previously unknown to human programers, and has achieved human competitive results in [finding algebraic terms in the study of finite algebras](http://www.cs.bham.ac.uk/~wbl/biblio/gecco2008/docs/p1291.pdf).

In contrast to the majority of other ML/AI methods, PushGP does not require the transformation of data into numeric structures. PushGP does not optimize a set of numeric parameters using a gradient, but rather attempts to intelligently search the space of programs. The result is a system where the primary output is a program written in the Turing complete Push language.

PushGP has proven itself to be one of the most power "general program synthesis" frameworks. Like most evolutionary search frameworks, it usually requires an extremely high runtime, however it can solve problems that few other programming-by-example system can solve.

Additional references on the successes of PushGP:

- [On the difficulty of benchmarking inductive program synthesis methods](https://dl.acm.org/citation.cfm?id=3082533)
- [General Program Synthesis Benchmark Suite](https://dl.acm.org/citation.cfm?id=2754769)
- [The Push3 execution stack and the evolution of control](https://dl.acm.org/citation.cfm?id=1068292)

### Goals of PyshGP

Previous PushGP frameworks have focused on supporting genetic programming and software synthesis research. One of the leading PushGP projects is [Clojush](https://github.com/lspector/Clojush), which is written in Clojure and heavily focused on the experimentation needed to further the research field.

`Pyshgp` aims to bring PushGP to a wider range of users and use cases. Many popular ML/AI frameworks are written in Python, and with `pyshgp` it is much easier to compare PushGP with other methods or build ML pipelines that contain PushGP and other models together.

Although PushGP is constantly changing through research and publication, `pyshgp` is meant to be a slowly changing, more stable, PushGP framework. It is still possible to use `pyshgp` for research and development, however accepted contributions to the main repository will be extensively benchmarked, tested, and documented.

##  Installing pyshgp

`pyshgp` is compatible with python 3.7.x and up.

### Install from pip

```sh
pip install pyshgp
```
- That's it! Read through the docs and examples to learn more.

### Build From source

- Clone the repo
- cd into the `pyshgp` repo directory
- run `pip install . --upgrade`
- That's it! Read through the docs and examples to learn more.

### Running Tests

Run the following command from project root directory. Make sure all the packages from `requirements-with-dev.txt` are installed in the instance of python you are using.

```sh
python -m pytest
```

Or run tests continuously (on save) during development using [pytest-watch](https://github.com/joeyespo/pytest-watch).

```sh
ptw 
``` 

## Documentation

Example usages of `pyshgp` can be found: 

- In the `examples/` [folder of the pyshgp Github repository](https://github.com/erp12/pyshgp/tree/master/examples).
- In the minimal [demo repository](https://github.com/erp12/pyshgp-demo).

The full `pyshgp` API can be found on [official website](http://erp12.github.io/pyshgp).

## Pysh Roadmap / Contributing

PyshGP is nearly ready for its 1.0 release. The main outstanding items ares:

- Extensive benchmarking to make sure pyshgp has the program-finding capabilities we expect from a contemporary PushGP system.
- More feedback on the API must be gathered before we commit to not making any breaking changes.

For information about contributing, see the [Contributing Guide](http://erp12.github.io/pyshgp/html/contributing.html).
