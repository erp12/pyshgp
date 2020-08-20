***********************
Configuring PushGP Runs
***********************

The primary abstraction for starting PushGP runs with PyshGP is to instantiate a
``PushEstimator`` and call the ``fit()`` method with a dataset of training cases. The
estimator can be configured to use different search algorithms, selection methods,
variation operators, and other hyperparameters. This guide demonstrates a variety
of different ways a ``PushEstimator`` could be configured to change the way
programs are synthesized in PyshGP.

At a minimum, a ``GeneSpawner`` must be provided when creating a ``PushEstimator``. The
spawner is used to generate random genomes during the initialization of an evolutionary
population and random genes during mutation operations. The genes might be produced by
the spawner are samples from a set of inputs, literals, ephemeral random constant
generators, and the ``InstructionSet``.

If only a ``GeneSpawner`` is provided, the hyperparameters of the ``PushEstimator``
will be the defaults listed in the API. See :ref:`api-gp`.

.. code-block:: python

  from pyshgp.gp.estimators import PushEstimator
  from pyshgp.gp.genome import GeneSpawner

  spawner = GeneSpawner(
      n_inputs=1,
      instruction_set="core",
      literals=[],
      erc_generators=[lambda: random.randint(0, 10)]
  )

  est = PushEstimator(spawner=spawner)
  est.fit(X, y)

The ``PushEstimator`` can be further configured with the top-level hyperparameters
that apply directly to the estimator. Examples include ``populaiton_size``,
``max_generations``, and ``initial_genome_size``. More information about these
hyperparameters can be found in the API. See :ref:`api-gp`.

.. code-block:: python

  from pyshgp.gp.estimators import PushEstimator

  est = PushEstimator(
      spawner=spawner,
      populaiton_size=1000,
      max_generations=300,
      initial_genome_size=(40, 200),
      simplification_steps=1000
  )
  est.fit(X, y)


Evolutionary Components
=======================

PyshGP aims to be extensive as much as possible. It is expected that users will want
to implement their own components (selection methods, variation operators, etc) and
use them in coordination with the abstractions provided by PyshGP. To accomplish this,
the ``PushEstimator`` accepts instances of various abstract base classes. Users can
choose to use instances of concrete sub-classes provided by PyshGP, or implement their own.

.. code-block:: python

  from pyshgp.gp.estimators import PushEstimator
  from pyshgp.gp.selection import Lexicase
  from pyshgp.gp.variation import VariationOperator

  class ReverseMutation(VariationOperator):
      """A mutation that reverses the parent genome."""

      def __init__(self):
          super().__init__(1)

      def produce(self, parents: Sequence[Genome], spawner: GeneSpawner) -> Genome:
          return Genome.create(parents[0][::-1])


  est = PushEstimator(
      spawner=spawner,
      selector=Lexicase(epsilon=True),      # This selector has its own configuration.
      variation_strategy=ReverseMutation(),
      population_size=300
  )


This design is in direct conflict with the sci-kit learn philosophy of designing estimators,
where hyperparameters are simple values and all of the configuration exists in the estimator.
In order to bring the ``PushEstimator`` back into towards a simpler (and narrower) API, most
the evolutionary components can be set with a string that corresponds to the name of a
reasonable "preset" value. For example, ``selector="lexicase"`` is the same as ``selector=Lexicase()``.

The following sections describe common ways of configuring the different components
of evolution.


Parent Selection
-----------------

Parent selection is controlled by an instance of a ``Selector`` type, and it's used to
select one or more individuals from evolutionary population. Different selectors apply
different "selection pressure" which guides evolution differently.

The preset selectors that can be referenced by name are:

- ``"roulette"`` : Fitness proportionate selection, also known as roulette wheel selection.
- ``"tournament"`` : Tournament selection. Default tournament size is 7.
- ``"lexicase"`` : Lexicase selection. Default ``epsilon=False``.
- ``"epsilon-lexicase"`` : Epsilon lexicase selection.
- ``"elite"`` : Selects the best ``n`` individuals by total error.


Variation Strategy
------------------

A variation operator is a transformation from parent genomes to a child genome. A
variation pipeline is a variation operator composed of other variation operators
that are applied in a sequence. A variation strategy is a variation operator that
composed of other variation operators that are each associated with a probability.

The preset variation operators that can be referenced by name are:

- ``"deletion"`` : Deletes random genes.
- ``"addition"`` : Adds random genes at random points.
- ``"alternation"`` : Pulls genes from a parent and randomly switches which parent it is pulling from.
- ``"genesis"`` : Creates entirely new random genomes.
- ``"cloning"`` : Returns the parent's genome unchanged.
- ``"umad"`` : Uniform mutation by addition and deletion.
- ``"umad-shrink"`` : Variant of UMAD that biases towards more deletion than addition.
- ``"umad-grow"`` : Variant of UMAD that biases towards more addition than deletion.

For a reference on UMAD, see `this paper <https://dl.acm.org/citation.cfm?id=3205455.3205603>`_.

When configuring a ``PushEstimator``, you can specify a variation strategy containing multiple
possible operators to apply with some probability. For example, the following configuration will
use ``Alternation`` 70% of the time and ``Genesis`` the other 30% of the time.

.. code-block:: python

  from pyshgp.gp.estimators import PushEstimator
  from pyshgp.gp.variation import VariationOperator, Alternation

  est = PushEstimator(
      spawner=spawner,
      variation_strategy=(
        VariationStrategy()
        .add(Alternation(alternation_rate=0.01, alignment_deviation=10), 0.7)
        .add(Genesis(size=(20, 100)), 0.3)
      )
  )


Search Algorithms
-----------------

Documentation TBD.


