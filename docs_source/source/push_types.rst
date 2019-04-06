*****************
Push Types
*****************

A ``PushType`` is a named collection of Python types which is used to determine if multiple items should be considered the same type during Push program execution. For example, the provided ``PushType`` that denotes which values should be considered integers is the ``PushInt``. It is named ``"int"`` and has the underlying types of ``(int, numpy.int64, numpy.int32, numpy.int16, numpy.int8)``.

Instructions which pull values from the integer stack will expect all elements to be of one of the underlying types.

A ``PushType`` can test if a value is an instance of one of the underlying types with the ``is_instance()`` method.

.. code-block:: python

  import numpy as np
  from pyshgp.push.types import PushInt, PushStr

  PushInt.is_instance(5)               # True
  PushInt.is_instance(np.int64(100))   # True
  PushInt.is_instance("Foo")           # False
  PushInt.is_instance(np.str_("Bar"))  # False

  PushStr.is_instance(5)               # False
  PushStr.is_instance(np.int64(100))   # False
  PushStr.is_instance("Foo")           # True
  PushStr.is_instance(np.str_("Bar"))  # True

The core set of ``PushTypes`` include ``PushInt``, ``PushFloat``, ``PushStr``, ``PushBool``, and ``PushChar``. Custom push types can be defined by instantiating new instances of the ``PushType`` class.

.. code-block:: python

  class Point:
      def __init__(self, x: float, y: float):
          self.x = x
          self.y = y

      def __repr__(self):
        return "Point<{x},{y}>".format(x=self.x, y=self.y)

  PushPoint = PushType("point", (Point, ))


Push Type Coercion
==================

The first type listed in the underlying types is considered the canonical type of the ``PushType``. During Push program execution, type conversions will result in instances of the canonical type.

Push types can take an optional argument called a "coercion function." This function must take a single input of any type and attempt to coerce it into the canonical type. Coercion functions can (and probably should) throw errors if the input value cannot be coerced into the canonical type.

The coercion function is used in the ``coerce`` method of the ``PushType``.

.. code-block:: python

  def to_point(thing: Any) -> Point:
    return Point(float(thing[0]), float(thing[1]))

  PushPoint = PushType("point", (Point, ), coercion_func=to_point)

  PushPoint.coerce([5, -1])  # Point<5.0,-1.0>

The constructor of the canonical type is used as the coercion function if no coercion function is provided.


Push Type Libraries
===================

The Push language operates using one stack per defined ``PushType``. All literal values evaluated by the Push interpreter, or produced by a Push instruction, are placed on their corresponding stack for use by other instructions.

A ``PushTypeLibrary`` is a collection of ``PushType`` objects that is used to produce the correct stacks before program evaluation and validate that the instructions specified in the ``InstructionSet`` will supported.

If you want to use a PushGP Estimator or Search Algorithm that synthesizes program which manipulate custom data types (using custom instructions) you will have to provide the system with a ``InstructionSet`` which holds a custom``PushTypeLibrary``.

By default, all the core types are registered into a ``PushTypeLibrary`` but that can be disable using ``register_core=False`` which will result in only the exec and code stacks getting registered.

.. code-block:: python

  from pyshgp.push.type_library import PushTypeLibrary

  lib = PushTypeLibrary()
  lib.supported_stacks()  # {'bool', 'char', 'code', 'exec', 'float', 'int', 'str'}

  lib2 = PushTypeLibrary(register_core=False)
  lib2.supported_stacks()  # {'code', 'exec'}

User defined ``PushType`` objects (such as ``PushPoint`` from above) can be registered using the ``register()`` and ``register_list()`` methods.

.. code-block:: python

  lib = PushTypeLibrary()
  lib.register(PushPoint) # Returns reference to the library for chaining calls to register.
  lib.supported_stacks()  # {'bool', 'char', 'code', 'exec', 'float', 'int', 'point', 'str'}

As a shorthand, you can use the ``create_and_register`` method of the ``PushTypeLibrary`` to create and new ``PushType`` and immediately register it.

.. code-block:: python

  lib = (
    PushTypeLibrary(register_core=False)
    .create_and_register("point", (Point, ), coercion_func=to_point)
  )
  lib.supported_stacks()  # {'code', 'exec', 'point'}
