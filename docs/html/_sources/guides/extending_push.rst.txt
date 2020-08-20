******************************
Extending the Push Interpreter
******************************

PyshGP is capable of synthesizing programs which manipulate primitive data types,
and simple collections, out-of-the-box. However, it is also common to want to synthesize
programs which leverage problem-specific data type. PyshGP's push insterpreter
is extensible, and supports the registration of addition data types and instructions.

This guide will demonstrate how to add support for an additional data type and some
related instructions. These extensions are performed at the user-level and don't require
any changes to the ``pyshgp`` source code.

We will be registering a Push type that corresponds to the ``Point`` class, defined below.

.. code-block:: python

  class Point:
      def __init__(self, x: float, y: float):
          self.x = x
          self.y = y

      def __repr__(self):
        return "Point<{x},{y}>".format(x=self.x, y=self.y)

Push Types
==========

A ``PushType`` is an object that encapsulates all the information about which values
should be considered the same "type" during Push program evaluation. The behavior of
a ``PushType`` is minimal: ``is_instance()`` and ``coerce()``.

Typically, a ``PushType`` simply refers to one or more Python types. Type checking and
coercion are delegated to the underlying Python types. For example, the ``PushInt`` object
(an instance of ``PushType``) defines an integer as any instance of the types
``(int, np.int64, np.int32, np.int16, np.int8)``. To coerce a value to a valid ``PushInt``,
the built-in constructor ``int`` is used.

For our ``Point`` type, we need to define a sub-class of ``PushType``. In our class
definition, we declare a name for our type and the underlying python types. In this case,
we will name our ``PushType`` as ``"point"`` and the underlying types will be a tuple containing
one element: the ``Point`` class. We also will set some flags that tell the Push interpreter
what kind of runtime constraints apply to the type. For example, if we set ``is_collection=True``
the push interpreter will treat our type as an unbounded collection of values (ie. list, dict) and
will limit it's size during evolution to avoid resource utilization issues.

The default ``is_instance`` behavior is to check the value against the given underlying
Python types. This behavior is well suited for our ``Point`` type, so we will not override.

The default ``coerce`` behavior is to pass the value to the constructor of the first
underlying Python type. The constructor of ``Point`` requires two arguments, so we
need custom coercion behavior.

Our ``PushType`` sub-class for ``Point`` objects, might look like this:

.. code-block:: python

  from pyshgp.push.types import PushType

  class PointPushType(PushType):
    def __init__(self):
        super().__init__(name="point",           # The name of the type, and the corresponding stack.
                         python_types=(Point,),  # The underlying Python types
                         is_collection=False,    # Indicates the type is not a data structure of unknown size.
                         is_numeric=False)       # Indicates the type is not a number.

    # override
    def coerce(self, value):
        return Point(float(value[0]), float(value[1]))


The Type Library
================

Before starting executing a Push program, the Push interpreter must be configured with a
set of ``PushTypes``, called a ``PushTypeLibrary``. The ``PushTypeLibrary`` is used to
produce the correct stacks before program evaluation and validate that the instructions
specified in the ``InstructionSet`` will supported.

By default, all the core types are registered into a ``PushTypeLibrary`` but that can
be disable using ``register_core=False`` which will result in only the exec and code
stacks getting registered.

.. code-block:: python

  from pyshgp.push.type_library import PushTypeLibrary

  lib = PushTypeLibrary()
  lib.supported_stacks()  # {'bool', 'char', 'code', 'exec', 'float', 'int', 'str'}

  lib2 = PushTypeLibrary(register_core=False)
  lib2.supported_stacks()  # {'code', 'exec'}

User defined ``PushType`` objects (such as ``PointPushType`` from above) can be
registered using the ``register()`` and ``register_list()`` methods.

.. code-block:: python

  type_lib = PushTypeLibrary()
  type_lib.register(PushPoint) # Returns reference to the library for chaining calls to register.
  type_lib.supported_stacks()  # {'bool', 'char', 'code', 'exec', 'float', 'int', 'point', 'str'}


Custom Push Instructions
========================

Once we register our custom Push types into the type library, our Push interpreter
will be able to accept instances of our type. However, there will not be any
Push instructions to create and manipulate the instances of our type. To address this,
we can define custom Push instructions.

To learn more about what Push instructions are, see :ref:`push-instructions`.

For a guide on how to define custom instructions, see :ref:`push-instruction-definition`.

Below we define a couple Push instructions that work with out ``Point`` type.

.. code-block:: python

  from pyshgp.push.instruction import SimpleInstruction

  def point_distance(p1, p2):
      """Return a tuple containing the distance between two points."""
      delta_x = p2.x - p1.x
      delta_y = p2.y - p1.y
      return sqrt(pow(delta_x, 2.0) + pow(delta_y, 2.0)),

  def point_from_floats(f1, f2):
      """Return a tuple containing a Point made from two floats."""
      return Point(f1, f2),

  point_distance_insrt = SimpleInstruction(
      "point_dist", point_distance,
      ["point", "point"], ["float"], 0
  )
  point_from_floats_instr = SimpleInstruction(
      "point_from_floats", point_from_floats,
      ["float", "float"], ["point"], 0
  )


The Instruction Set
===================

When creating Push Interpreter, or genetic programming ``Spawner``, PyshGP requires an
``InstructionSet`` that holds all the Push instructions that can appear in Push programs.

To declare an ``InstructionSet``, we must provide a ``TypeLibrary``. All instructions that get
registered into the ``InstructionSet`` will be validated against the ``TypeLibrary`` to ensure
that it will be possible to execute the instruction.

When creating a new ``InstructionSet``, we can automatically register all the core instructions
(built into ``pyshgp``) that are supported by the ``TypeLibrary`` by using passing ``register_core=True``.
Additional instructions can be registered using methods like ``register()`` and ``register_all()``.

Below we create an ``InstructionSet`` that contains our custom instructions.

.. code-block:: python

  from pyshgp.push.instruction_set import InstructionSet

  i_set = InstructionSet(type_library=type_lib, register_core=True)
  i_set.register(point_distance_insrt)
  i_set.register(point_from_floats_instr)


To start a genetic programming run with our custom ``InstructionSet``, we will pass it to the ``Spawner``
and interpreter.

.. code-block:: python

    spawner = GeneSpawner(
        n_inputs=2,
        instruction_set=i_set,
        literals=[2.0],
        erc_generators=[]
    )

    est = PushEstimator(
        spawner=spawner,
        population_size=100,
        max_generations=50,
        simplification_steps=500,
        interpreter=PushInterpreter(instruction_set)
    )

    # Start the run
    est.fit(X, y)
