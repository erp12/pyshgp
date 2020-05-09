## Fitting Literals

#### Goals

- GeneSpawners can spawn two types of literals Literals.
  - Some Literals are provided by users and don't require fitting.
  - Some Literals are ERCs produced by ERC generator functions.
- Fitting ERC Literals to their optimal value is difficult via evolution.
- If some sort of stochastic optimization periodically applied to Literals might help.

#### To Do

- [ ] Add a Literal subclass for `ErcLiteral`.
- [ ] Add a search config param for `literal_optimization_interval`.
- [ ] Create an ErcOptimization framework.
- [ ] Every `n` generations pause evolution to perform literal optimization.
  - Select a parent.
  - Identify the ERCs in the genome.
  - Perform some kind of stochastic optimization
  - Put the optimized genome in the next generation.
  - Repeat until population is full and resume evolution for another `n` generations.
