The :mod:`push` sub-package contains an implementation of the Push language.
This includes an instruction set, interpreter, and random Push code generation
utilities.

The following paragraph has been taken from the Push language
`homepage <http://faculty.hampshire.edu/lspector/push.html>`_.

  Push is a programming language designed for evolutionary computation, to be
  used as the programming language within which evolving programs are expressed.
  Push features a stack-based execution architecture in which there is a
  separate stack for each data type. In Push, "code" itself is a data type,
  allowing programs to manipulate their own code as they run and thereby to
  implement arbitrary and potentially novel control structures. This
  expressiveness is combined with syntactic minimality: the only syntax rule is
  that parentheses must be balanced. It is therefore trivial to generate and
  transform syntactically valid Push programs.
