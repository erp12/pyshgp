# TerpreT Problems

Publication can be found here:
https://arxiv.org/abs/1608.04428

## Prepend zero

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

