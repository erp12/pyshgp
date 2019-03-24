*************
Release Notes
*************

A summary of changes made between each PyshGP release.

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
