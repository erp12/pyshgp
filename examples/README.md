
## Benchmarks (Timings in seconds)

These reports are based on single runs that I chose to document because they *seem* to be around the standard runtime for each problem. This should be replaced with a less anecdotal investigation.

### Odd With 8 Cores

```
Solution found on generation 9
Evaluation Times (each gen): [7.165, 14.708, 14.512, 23.707, 14.897, 25.362, 20.563, 21.878, 23.107]
Selection/Variations Times (each gen): [1.754, 2.777, 5.133, 3.313, 5.118, 3.459, 3.472, 3.864]
Average Evaluation Timing of Generation: 18.433
Average Selection/Variations Timing of Generation: 3.611
```

### Iris With 8 Cores

```
Solution found on generation 5
Evaluation Times (each gen): [64.735, 95.176, 81.068, 85.371, 117.684]
Selection/Variations Times (each gen): [3.589, 4.748, 10.568, 5.424]
Average Evaluation Timing of Generation: 88.807
Average Selection/Variations Timing of Generation: 6.082
```

### Sextic With 8 Cores

```
Solution found on generation 7
Evaluation Times (each gen): [13.284, 10.446, 12.817, 14.331, 18.142, 24.143, 36.481, 27.931, 31.012]
Selection/Variations Times (each gen): [12.796, 7.714, 18.109, 16.376, 17.844, 42.242, 45.71, 46.124]
Average Evaluation Timing of Generation: 20.954
Average Selection/Variations Timing of Generation: 25.864
```

### Replace Space With Newline With 16 cores

```
Solution found on generation 21
Evaluation Times (each gen): [37.398, 42.174, 43.109, 35.547, 32.694, 39.119, 38.609, 54.275, 57.33, 63.246, 57.28, 64.719, 61.829, 52.758, 67.201, 56.008, 56.007, 59.255, 55.868, 58.813, 52.972, 57.122, 77.44]
Selection/Variations Times (each gen): [5.497, 22.865, 12.645, 9.958, 12.473, 10.667, 26.854, 17.874, 21.007, 13.448, 19.012, 21.041, 30.612, 21.282, 12.36, 21.495, 31.493, 24.653, 29.559, 18.59, 17.665, 30.761]
Average Evaluation Timing of Generation: 53.077
Average Selection/Variations Timing of Generation: 19.628
```

### String Demo

```
Solution found on generation 10
Evaluation Times (each gen): [1.537, 1.119, 1.622, 1.471, 1.636, 1.748, 1.496, 1.537, 1.651, 1.635, 1.359, 1.387]
Selection/Variations Times (each gen): [0.251, 0.332, 0.43, 0.521, 0.52, 0.539, 0.517, 0.626, 0.566, 0.388, 0.66]
Average Evaluation Timing of Generation: 1.516
Average Selection/Variations Timing of Generation: 0.486
```

## Solutions

These solutions have undergone basic simplification. It is likely that they could be simplified further.

### Odd

```
[exec_yank_INSTR, string_stack_depth_INSTR, integer_empty_INSTR, char_pop_INSTR, code_if_INSTR, code_do*range_INSTR, string_empty_INSTR, integer_yank_INSTR, exec_yank_INSTR, string_stack_depth_INSTR, integer_empty_INSTR, string_empty_INSTR, integer_empty_INSTR, string_empty_INSTR, integer_empty_INSTR, string_empty_INSTR, integer_empty_INSTR, _input0_INPT_INSTR, boolean_yank_INSTR]
```

### Iris

```
[0.5805125769239845, _input0_INPT_INSTR, vote2_float_CLASS_INSTR, _input0_INPT_INSTR, vote2_float_CLASS_INSTR, float_inc_INSTR, vote1_float_CLASS_INSTR, _input0_INPT_INSTR, 0.9650029510267347, vote2_float_CLASS_INSTR, vote1_float_CLASS_INSTR]
```

### Sextic

```
[_input0_INPT_INSTR, _input0_INPT_INSTR, float_dup_INSTR, float_mult_INSTR, float_div_INSTR, _input0_INPT_INSTR, _input0_INPT_INSTR, float_mult_INSTR, float_add_INSTR, _input0_INPT_INSTR, float_swap_INSTR, float_dup_INSTR, float_mult_INSTR, float_mult_INSTR, float_mult_INSTR]
```

### Replace Space With Newline

```
[_input0_INPT_INSTR, string_split_at_space_INSTR, string_concat_INSTR, c_space, c_space, string_concat_INSTR, string_concat_INSTR, string_concat_INSTR, string_concat_INSTR, string_concat_INSTR, string_concat_INSTR, string_concat_INSTR, string_concat_INSTR, float_stack_depth_INSTR, _input0_INPT_INSTR, string_char_at_INSTR, string_length_INSTR, char_eq_INSTR, float_stack_depth_INSTR, _input0_INPT_INSTR, c_newline, integer_shove_INSTR, string_replace_char_INSTR]
```

### String Demo

```
[integer_stack_depth_INSTR, integer_dup_INSTR, integer_stack_depth_INSTR, integer_sub_INSTR, string_head_INSTR, string_dup_INSTR, string_concat_INSTR]
```