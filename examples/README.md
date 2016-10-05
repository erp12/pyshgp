# Interesting Problem Solutions

## Odd

```
CLOJUSH:
(boolean_stackdepth exec_do*range (exec_if () (exec_empty code_null code_quote ())))
(boolean_stackdepth code_stackdepth boolean_frominteger code_fromboolean exec_do*range (exec_when (boolean_empty code_empty)))

PYSH:
['_code_stack_depth', '_exec_do*range', ['_exec_empty', '_integer_yankdup']]
['_exec_do*times', ['_integer_empty']]

```


## Computational Timings

### STRING

#### With concurrent

Average Evaluation Timing of Generation: 1.59
Average Selection/Variations Timing of Generation: 0.53

#### Without Concurrent

Average Evaluation Timing of Generation: 0.974
Average Selection/Variations Timing of Generation: 0.389


### INTEGER REGRESSION (50 test cases)

#### With concurrent

Average Evaluation Timing of Generation: 2.396
Average Selection/Variations Timing of Generation: 1.681

#### Without Concurrent

Average Evaluation Timing of Generation: 4.681
Average Selection/Variations Timing of Generation: 1.563


### RSWN

#### With concurrent

Average Evaluation Timing of Generation: 17.376
Average Selection/Variations Timing of Generation: 3.265

#### Without concurrent

Average Evaluation Timing of Generation: 31.837
Average Selection/Variations Timing of Generation: 3.575

#### Solutions

Clojush found following solution at generation 45
`(\space in1 \newline string_replacechar print_string \space in1 string_removechar char_allfromstring char_stackdepth)`