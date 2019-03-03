## Fitting Literals

### Goals

- GeneSpawners can spawn two types of literals Literals.
  - Some Literals are provided by users and don't require fitting.
  - Some Literals are ERCs produced by ERC generator functions.
- Fitting ERC Literals to their optimal value is difficult via evolution.
- If some sort of stochastic optimization periodically applied to Literals might help.

### To Do

- [ ] Add a Literal subclass for `ErcLiteral`.
- [ ] Add a search config param for `literal_optimization_interval`.
- [ ] Create an ErcOptimization framework.
- [ ] Every `n` generations pause evolution to perform literal optimization.
  - Select a parent.
  - Identify the ERCs in the genome.
  - Perform some kind of stochastic optimization
  - Put the optimized genome in the next generation.
  - Repeat until population is full and resume evolution for another `n` generations.

## Strategy For Parallelism

### Goals

- Abstractly, evaluation is embarrassingly parallel. PyshGP should attempt to approach this in practice.
- External tooling (libraries and infrastructure) should be kept to minimum.
- Minimize the amount of serialization

### To Do

- [ ] Remove all lambdas and nested functions from the instruction definitions.
  - This will likely require the use of partials
- [ ] Ensure no lambdas and nested functions exist in classes involved in evaluation.
- [ ] Add multiprocessing pool to search algorithm configuration.
- [ ] Broadcast data and population once.
- [ ] Perform evaluation, and collect results.


## Logging

### Goals

- Implement system which produces log files for analysis

### To Do

- [ ] Add optional log directory to search config
- [ ] Create a directory for logs at start of each run.
- [ ] Create a `metadata.json` file in each run log directory
  - Datetime run started
  - Serialized search algorithm config
  - Success / Failure
  - Best program found
  - problem or some other name
- Create an `individuals.csv` pipe delimited log file
  - `id`, `generation`, `genome`, `error_vector`
  - Update with population at each generation.
- Create an `ancestry.csv` pipe delimited log file
  - `parent_id`, `child_id`, `generation`, `selection_method`, `variation_method`
  - Edge list of evolutionary lineage.


## User Defined Types/Stacks

### Goals

- Users should be able to define their own PushTypes which get associated Stacks.
- This is meant to aid in domain-specific applications (ie. NeuroEvolution, Quantum Algorithms, etc)
