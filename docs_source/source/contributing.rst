************
Contributing
************

Reporting Bugs and Feature Requests
===================================

Reporting bugs and requesting features should be done by opening issues on the
`pyshgp GitHub repository page <https://github.com/erp12/pyshgp/issues>`_.

Contributing Code
=================

Contributions to ``pyshgp`` are accepted via GitHub pull requests. If you would like
to make change to the pyshgp code base (including tests and documentation) you
must first fork `the repository <https://github.com/erp12/pyshgp>`_.

After cloning your fork, open a new branch. **Do not add your changes to**
``master``. Once you have finished making your changes, you must open a pull
request, which will be reviewed and eventually merged. If your changes are meant
to address an open GitHub issue, it would be helpful if you mentioned the issue
in the body of the pull request.

Code Reviews
------------

All contributions to pyshgp will undergo at least one manual code review done by
the project's maintainers on the GitHub page. Please be patient while maintainers
find time to review your pull requests.

Code Style
----------

Pyshgp strives to conform to `pep8 <https://www.python.org/dev/peps/pep-0008/>`_
as much as possible. Codacy has been set up to log almost all pep8 violations as
issues. Pull requests will not be accepted until all code style issues have
been resolved.

Unit Tests
----------

Test coverage is not explicitly measured or tracked for pyshgp contributions,
however, pull requests are expected to have unit tests when appropriate.

Contributing Documentation
==========================

The documentation of ``pyshgp`` is found in the ``docs`` folder. The documentation
is built with `Sphinx <http://www.sphinx-doc.org/en/stable/index.html>`_ and the
source code can be found in the ``docs_source`` folder.

As much documentation as possible is inserted from docstrings using
`autodoc <http://www.sphinx-doc.org/en/stable/ext/autodoc.html>`_. This will
allow other contributors to read documentation from the source code and will
also cut down on duplicated text.

Contributing Examples
=====================

Adding examples to ``pyshgp`` is a great way to demonstrate functionality to users
and document different use cases.

Example files should be placed in the ``examples`` folder. If possible, data
files should not be included with examples, but constructed or downloaded by
the example file.

Examples should never import ``pyshgp`` modules using relative paths. Instead
assume ``pyshgp`` has been installed as a package.

Release Pattern
===============

The GitHub repository's master branch is always kept in sync with what is
available on PyPi.

In anticipation of a new release, a "pre-version" branch will be created with
the naming convention "v##-pre" where "##" is the anticipated version.

As feature branches (and forks) are opened to address issues, they will be
reviewed via PR and merged into the "pre-version" branch.

Once the pre-version branch contains all the features required for the release
of the next version (as dictated by the project boards on the GitHub page)
the pre-version branch will be merged with master, a new release will be put on
PyPI, and a locked version branch will be created.
