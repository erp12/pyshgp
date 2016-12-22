
## Benchmarks (Timings in seconds)

These reports are based on single runs that I chose to document because they *seem* to be around the standard runtime for each problem. This should be replaced with a less anecdotal investigation.


| Problem        | Solution Generation | Workers | Avg Generation Evaluation Time | Avg Generation Selection/Variations Time |
|----------------|---------------------|---------|--------------------------------|------------------------------------------|
| Odd            | 9                   | 8       | 18.433s                        | 3.611s                                   |
| Iris           | 5                   | 8       | 88.807s                        | 6.082s                                   |
| Sextic         | 7                   | 8       | 20.954s                        | 25.864s                                  |
| RSWN           | 21                  | 16      | 53.077s                        | 19.628s                                  |
| String Demo    | 10                  | 8       | 1.516s                         | 0.486s                                   |
| Int Regression | 2                   | 8       | 2.601s                         | 2.42s                                    |

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