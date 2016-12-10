# TerpreT Problems

Publication can be found here:
https://arxiv.org/abs/1608.04428

## Invert

Move from left to right along the tape and invert all
the binary symbols, halting at the first blank cell.

### Solution
```
[float_empty, _input0, foat_from_boolean, exec_if, [exec_do*vector_boolean], [float_empty, boolean_eq]]
```

### Timings
```
Solution Found on Generation 12
Evaluation Times (each gen): [11.699, 15.189, 14.068, 15.572, 14.792, 15.013, 15.935, 19.321, 15.004, 14.049, 14.151, 16.525, 15.66, 15.938]
Selection/Variations Times (each gen): [1.178, 1.656, 1.59, 1.789, 1.628, 1.663, 1.819, 1.717, 1.605, 1.52, 1.765, 1.648, 1.721]
Average Evaluation Timing of Generation: 15.208
Average Selection/Variations Timing of Generation: 1.638
```

## Prepend zero

Insert a “0” symbol at the start of the tape and shift
all other symbols rightwards one cell. Halt at the
first blank cell.

### Solution
```
[char_stack_depth_INSTR, string_from_integer_INSTR, _input0_INPT_INSTR, string_concat_INSTR]
```

### Timings
```
Solution Found on Generation 5
Evaluation Times (each gen): [5.154, 5.81, 6.289, 6.329, 6.299, 6.669, 23.121]
Selection/Variations Times (each gen): [1.301, 3.286, 3.32, 2.97, 2.854, 1.713]
Average Evaluation Timing of Generation: 8.525
Average Selection/Variations Timing of Generation: 2.574
```


## 2-bit controlled shift register

Given input registers (r1, r2, r3), output (r1, r2, r3)
if r1 == 0 otherwise output (r1, r3, r2) (i.e. r1 is
a control bit stating whether r2 and r3 should be
swapped).

### Solution
```
[_input2_INPT_INSTR, exec_shove_INSTR, [_input1_INPT_INSTR], _input0_INPT_INSTR]
```

### Timings
```
Solution Found on Generation 7
Evaluation Times (each gen): [5.707, 5.641, 6.939, 6.685, 6.361, 6.283, 7.295, 7.688, 8.103]
Selection/Variations Times (each gen): [1.141, 2.837, 3.019, 2.823, 2.794, 2.917, 2.706, 2.647]
Average Evaluation Timing of Generation: 6.745
Average Selection/Variations Timing of Generation: 2.611
```

## Full Adder

### Solution
```
[_input2, code_member, string_empty_string, _input0, vector_boolean_replace, exec_do*while, [integer_eq, boolean_invert_first_then_and, foat_from_boolean, integer_empty, vector_integer_emptyvector, exec_do*range, [exec_do*while, [boolean_pop, char_eq, _input0, boolean_pop], float_eq, vector_string_contains, code_from_boolean, float_eq, exec_dup, [boolean_from_float, code_empty, code_if, vector_boolean_append, vector_boolean_first, vector_float_eq, code_if, float_lte, print_boolean, _input0, _input2, code_member, char_is_white_space], integer_lt, exec_stack_depth, integer_lte, exec_yank, vector_boolean_pushall, vector_string_contains], _input1, exec_shove, [boolean_from_integer, boolean_not, vector_integer_emptyvector, code_do*count, _input1, exec_shove, [], _input0, integer_lte, exec_yank, vector_boolean_replace], code_do]]
```

## 2-bit Ader

### Solution
```

```

## Access

Access the kth element of a contiguous array. 

### Solution
```
[_input1, _input0, vector_integer_nth]
```

### Timings
```
Solution Found on Generation 13
Evaluation Times (each gen): [11.234, 18.403, 21.729, 27.779, 37.879, 39.385, 40.288, 43.934, 42.329, 41.703, 40.959, 41.827, 41.795, 42.762, 41.698]
Selection/Variations Times (each gen): [1.449, 2.694, 2.047, 1.953, 1.918, 1.689, 1.682, 1.685, 1.843, 1.809, 1.821, 1.9, 1.802, 1.872]
Average Evaluation Timing of Generation: 35.58
Average Selection/Variations Timing of Generation: 1.869
```

## Decrement

Decrement all elements in a contiguous array.

### Solution
```
[_input0, exec_do*vector_integer, integer_dec]
```

### Timings
```
Solution Found on Generation 2
Evaluation Times (each gen): [4.503, 6.82, 6.787, 7.592]
Selection/Variations Times (each gen): [2.278, 2.057, 18.767]
Average Evaluation Timing of Generation: 6.426
Average Selection/Variations Timing of Generation: 7.701
```
