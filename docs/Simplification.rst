********************************
Automatic Genome Simplification
********************************

Like many PushGP systems, ``pyshgp`` supports automatic simplification of Push
programs. Simplification refers to the process of removing elements from a
program in order to make it easier to interpret and improves generalization.
In ``pyshgp`` this is done through the simplification of an Individual's plush
genome.

Plush genes can be flagged as "silent" which causes them to not appear in the
translated programs. Plush genes can also have their atom (instruction or
literal) replaced with a "no-op" instruction which does not have effect when
executed.

Automatic Genome Simpflicication in ``pyshgp`` is done via a hill climbing
algorithm which selects between 1 and 3 random genes. These genes are either
randomly silenced or replaced with no-ops. The resulting genome is then
translated into a program and evaluated. If the new total error of the program
is greater than the origional program, the change to the genes is reverted.
