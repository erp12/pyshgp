*************
Release Notes
*************

A summary of changes made between each PyshGP release.


v0.1.6 - June 1, 2020
===============================

API changes
-------------------------------

- Added a ``Program`` abstraction to better encapsulate (almost) everything needed to run a Push program consistently.
- Added parallelism controls to ``PushEstimator`` and ``SearchAlgorithm``.
- Added collection size cap to PushConfig to prevent programs from taking up huge amounts of memory.
- Added ``TapManager`` and ``Taps`` for logging and monitoring.
- Fixed ``exclude_stacks`` option of ``register_core_by_stack``.


Internals
-------------------------------

- Fixed DatasetEvaluator support for pandas data structures.
- Refactored ``Selector`` to use ``SimpleMultiSelectorMixin``.
- Added more constraints to push execution.


Development / Repository
-------------------------------

- Added tox.
- Fixed many doc typos.
- Added some utility scripts for making deployment of new releases easier.
- Updated CI to include multiple python versions.
- Migrated CI/CD to GitHub actions.


Known Issues
-------------------------------

None yet.

Report issues on `the Github issues page <https://github.com/erp12/pyshgp/issues>`_.

Credits
-------------------------------

This release would not have been possible without the following contributors:

- Github user `epicfaace <https://github.com/epicfaace>`_.
  - Reporting and fixing typos.
- Github user `vargonis <https://github.com/vargonis>`_.
  - Reporting failure of Push execution constraints.


v0.1.5 - April 19, 2019
===============================

API changes
-------------------------------

- Separated "types" and "stacks" in a more logical way. Various arguments have been renamed.
- Made verbosity config easier to configure and use.
- Add optional argument to ``PushStack`` for pushing initial values. Useful for custom fitness functions.
- Added the ``PushTypeLibrary`` abstraction. Read more at link below.

.. toctree::
   :maxdepth: 1

   push_types

Internals
-------------------------------

- Changed how core instructions can be added to instruction sets.
- Added support for smaller numpy ints than int64.
- Improved performance with respect to monitoring/verbosity.
- Fixed rarely occurring non-deterministic type matching.


Development / Repository
-------------------------------

- Added ``tutorials/point_distance.py`` example to demonstrate custom types.
- Added documentation article push types.
- Moved style checking from tests to CI


Known Issues
-------------------------------

- Programs that have literal values of custom types are not be serializable to JSON.

Report issues on `the Github <https://github.com/erp12/pyshgp/issues>`_.

Credits
-------------------------------

This release would not have been possible without the following contributors:

- Blossom Metevier.

  - Reported lack of support for smaller numpy int types.
  - Demonstrated the annoyance of style checking in tests.

- Julian Oks

  - Demonstrated a need for ``PushState`` initial values argument.



v0.1.4 - March 23, 2019
===============================

API changes
-------------------------------

- Changed ``PushState.pretty_print()`` signature from argument annotation to default.

Internals
-------------------------------

- Removed variable annotations from codebase to make pyshgp compatible with Python 3.5 again.
- Fixed overflow error in dup_times instructions (`#108 <https://github.com/erp12/pyshgp/issues/108>`_)
- ``TakesStateInstruction`` allows for tuple return values
- If push program input value is Atom subtype, it will no longer be wrapped in a ``Literal``.
- Removed incorrect numpy string types.
- All exceptions when evaluating atoms will be caught and raised after printing which atom was being evaluated.

Development / Repository
-------------------------------

- Added documentation article on instructions.
- Added documentation showing all core instruction docstrings.
- Tuned string tutorial examples to take less time for CI testing.
- Fixed typos in README.md
- Added this release notes page :)


Known Issues
-------------------------------

None yet. Report issues on `the Github <https://github.com/erp12/pyshgp/issues>`_.

Credits
-------------------------------

This release would not have been possible without the following contributors:

- Blossom Metevier.

  - Reported the incompatibility with Python 3.5 due to variable annotations.

- Lee Spector

  - Feedback on README file.

- Michael Garcia

  - Reporting the lack of documentation on defining and registering custom instructions.



v0.1.3 - March 12, 2019
===============================

API changes
-------------------------------

- Added last_str_from_stdout option to PushEstimator. If True, the last string type output of a program will be taken from the PushState's stdout attribute after program evaluation finishes.
- Added validation and verbosity controls. Estimator has minimal verbosity options (0, 1, or 2). SearchAlgorithm can take a fully configurable VerbosityConfig.

Internals
-------------------------------

- Removed a source of infinite loops instructions.

Development / Repository
-------------------------------

- Added "Replace Space With Newline" example file.
- Improved verbosity of example problems.
- Mentioned tests in README.
- Added license file.

Known Issues
-------------------------------

None yet. Report issues on `the Github <https://github.com/erp12/pyshgp/issues>`_.

Credits
-------------------------------

This release would not have been possible without the following contributors:

- Github user `RedBeansAndRice <https://github.com/RedBeansAndRice>`_.
  - Reporting issues with example files not conforming to API changes.
