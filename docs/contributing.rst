************
Contributing
************


Reporting Bugs and Feature Requests
===================================

Reporting bugs and requesting features should be done by opening issues on the
`pyshgp GitHub repository page <https://github.com/erp12/pyshgp/issues>`_.

Contributing Code
=================

Contributions to pyshgp are accepted via GitHub pull requests. If you would like
to make change to the pyshgp code base (including tests and documentation) you
must first fork `the repository <https://github.com/erp12/pyshgp>`_.

After cloning your fork, open a new branch. **Do not add your changes to
``master``.** If your changes are meant to address an open GitHub issue, it
would be helpful if you named your branch starting witht the issue number.

Once you have finished making your changes, you must open a pull request, which
will be reviewed and eventually merged.

Code Reviews
------------

All contributions to pyshgp will undergo 2 code reviews. The first is an
automated code review performed by `Codacy <https://www.codacy.com/>`_. The
second will be a manual code review done by project's maintainers on the GitHub
page.

Both code reviews will be done on the GitHub page for the open pull request.

Code Style
----------

Pyshgp strives to conform to `pep8 <https://www.python.org/dev/peps/pep-0008/>`_
as much as possible. Codacy has been set up to log almost all pep8 violations as
issues. Pull requests will not be accepted until all code style issues have
been resolved.

Unit Tests
----------

Pyshgp uses Codacy to track code covereage. Pull requests are expected to have
unit tests that cover at least 90% of their code. Pull requests that do not
contain appropriate unit tests will not be merged.

Other Issues
------------

Codacy tracks a number of other types of issues. Currently only the types of
issues listed above will definitively prevent a pull request from being accepted
but the pyshgp maintainers will review the Codacy issues and diff of the pull
request to determine what needs to be addressed before merging.

Contributing Documentation
==========================

The documentation of pyshgp is found in the ``docs`` folder. The documentation
is built with `Sphinx <http://www.sphinx-doc.org/en/stable/index.html>`_.

As much documentation as possible is inserted from docstrings using
`autodoc <http://www.sphinx-doc.org/en/stable/ext/autodoc.html>`_. This will
allow other contributers to read documentation from the source code and will
also cut down on duplicated source code.

Contributing Examples
=====================

Adding examples to pyshgp is a great way to demonstrate functionality to users
and document different use cases.

Example files should be placed in the ``examples`` folder. If possible, data
files should not be included with examples, but constructed or downloaded by
the example file.

Exampls should never import pyshgp modules using relative paths. Instead assume
pyshgp has been installed as a package.
