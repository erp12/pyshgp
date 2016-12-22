
# Benchmarks (Timings in seconds)

These reports are based on single runs that I chose to document because they *seem* to be around the standard runtime for each problem. This should be replaced with a less anecdotal investigation.


| Problem        | Solution Generation | Workers | Avg Generation Evaluation Time | Avg Generation Selection/Variations Time |
|----------------|---------------------|---------|--------------------------------|------------------------------------------|
| Odd            | 9                   | 8       | 18.433                         | 3.611                                    |
| Iris           | 5                   | 8       | 88.807                         | 6.082                                    |
| Sextic         | 5                   | 8       | 13.491                         | 23.73                                    |
| RSWN           | 21                  | 16      | 53.077                         | 19.628                                   |
| String Demo    | 10                  | 8       | 1.863                          | 0.404                                    |
| Int Regression | 8                   | 8       | 3.141                          | 6.027                                    |

# Solutions

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
[_input0, _float_dup, _input0, _float_mult, _input0, _float_mult, _float_sub, _float_dup, _float_mult]
```

### Replace Space With Newline

```
[_input0_INPT_INSTR, string_split_at_space_INSTR, string_concat_INSTR, c_space, c_space, string_concat_INSTR, string_concat_INSTR, string_concat_INSTR, string_concat_INSTR, string_concat_INSTR, string_concat_INSTR, string_concat_INSTR, string_concat_INSTR, float_stack_depth_INSTR, _input0_INPT_INSTR, string_char_at_INSTR, string_length_INSTR, char_eq_INSTR, float_stack_depth_INSTR, _input0_INPT_INSTR, c_newline, integer_shove_INSTR, string_replace_char_INSTR]
```

### String Demo

```
[_string_stack_depth, _input0, _string_dup, _string_stack_depth, _integer_sub, _string_head, _string_dup, _string_concat]
```

### Integer Regression

```
[_input0, 2, _integer_sub, _input0, _integer_mult, _input0, _integer_mult, _input0, _integer_sub]
```