********************
Pysh Instruction Set
********************

boolean_and
"""""""""""
Pushes the logical AND of the top two BOOLEANs.

boolean_or
""""""""""
Pushes the logical OR of the top two BOOLEANs.

boolean_not
"""""""""""
Pushes the logical NOT of the top BOOLEAN.

boolean_xor
"""""""""""
Pushes the logical XOR of the top two BOOLEANs.

boolean_invert_first_then_and
"""""""""""""""""""""""""""""
Pushes the logical AND of the top two BOOLEANs, with the fist argument inverted.

boolean_invert_second_then_and
""""""""""""""""""""""""""""""
Pushes the logical AND of the top two BOOLEANs, with the second argument inverted.

exec_do*range
"""""""""""""
An iteration instruction that executes the top item on the EXEC stack a number of times that depends on the top two integers, while also pushing the loop counter onto the INTEGER stack for possible access during the execution of the body of the loop. The top integer is the "destination index" and the second integer is the "current index." First the code and the integer arguments are saved locally and popped. Then the integers are compared. If the integers are equal then the current index is pushed onto the INTEGER stack and the code (which is the "body" of the loop) is pushed onto the EXEC stack for subsequent execution. If the integers are not equal then the current index will still be pushed onto the INTEGER stack but two items will be pushed onto the EXEC stack.

exec_do*count
"""""""""""""
An iteration instruction that performs a loop (the body of which is taken from the EXEC stack) the number of times indicated by the INTEGER argument, pushing an index (which runs from zero to one less than the number of iterations) onto the INTEGER stack prior to each execution of the loop body.

exec_pop
""""""""
Pops the EXEC stack. This may be thought of as a "DONT" instruction.

integer_pop
"""""""""""

float_pop
"""""""""
Pops the INTEGER stack.

code_pop
""""""""
Pops the CODE stack.

boolean_pop
"""""""""""
Pops the BOOLEAN stack.

string_pop
""""""""""
Pops the STRING stack.

exec_dup
"""""""""""""""""""""""""
Duplicates the top item on the EXEC stack. Does not pop its argument. This may be thought of as a "DO TWICE" instruction.


integer_dup
"""""""""""""""""""""""""
Duplicates the top item on the INTEGER stack. Does not pop its argument.


float_dup
"""""""""""""""""""""""""
Duplicates the top item on the FLOAT stack. Does not pop its argument.


code_dup
"""""""""""""""""""""""""
Duplicates the top item on the CODE stack. Does not pop its argument.


boolean_dup
"""""""""""""""""""""""""
Duplicates the top item on the BOOLEAN stack. Does not pop its argument.


string_dup
"""""""""""""""""""""""""



exec_swap
"""""""""""""""""""""""""



integer_swap
"""""""""""""""""""""""""



float_swap
"""""""""""""""""""""""""



code_swap
"""""""""""""""""""""""""



boolean_swap
"""""""""""""""""""""""""



string_swap
"""""""""""""""""""""""""



exec_rot
"""""""""""""""""""""""""



integer_rot
"""""""""""""""""""""""""



float_rot
"""""""""""""""""""""""""



code_rot
"""""""""""""""""""""""""



boolean_rot
"""""""""""""""""""""""""



string_rot
"""""""""""""""""""""""""



exec_flush
"""""""""""""""""""""""""



integer_flush
"""""""""""""""""""""""""



float_flush
"""""""""""""""""""""""""



code_flush
"""""""""""""""""""""""""



boolean_flush
"""""""""""""""""""""""""



string_flush
"""""""""""""""""""""""""



exec_eq
"""""""""""""""""""""""""



integer_eq
"""""""""""""""""""""""""



float_eq
"""""""""""""""""""""""""



code_eq
"""""""""""""""""""""""""



boolean_eq
"""""""""""""""""""""""""



string_eq
"""""""""""""""""""""""""



exec_stack_depth
"""""""""""""""""""""""""



integer_stack_depth
"""""""""""""""""""""""""



float_stack_depth
"""""""""""""""""""""""""



code_stack_depth
"""""""""""""""""""""""""



boolean_stack_depth
"""""""""""""""""""""""""



string_stack_depth
"""""""""""""""""""""""""



exec_yank
"""""""""""""""""""""""""



integer_yank
"""""""""""""""""""""""""



float_yank
"""""""""""""""""""""""""



code_yank
"""""""""""""""""""""""""



boolean_yank
"""""""""""""""""""""""""



string_yank
"""""""""""""""""""""""""



exec_yankdup
"""""""""""""""""""""""""



integer_yankdup
"""""""""""""""""""""""""



float_yankdup
"""""""""""""""""""""""""



code_yankdup
"""""""""""""""""""""""""



boolean_yankdup
"""""""""""""""""""""""""



string_yankdup
"""""""""""""""""""""""""



exec_shove
"""""""""""""""""""""""""



integer_shove
"""""""""""""""""""""""""



float_shove
"""""""""""""""""""""""""



code_shove
"""""""""""""""""""""""""



boolean_shove
"""""""""""""""""""""""""



string_shove
"""""""""""""""""""""""""



exec_empty
"""""""""""""""""""""""""



integer_empty
"""""""""""""""""""""""""



float_empty
"""""""""""""""""""""""""



code_empty
"""""""""""""""""""""""""



boolean_empty
"""""""""""""""""""""""""



string_empty
"""""""""""""""""""""""""



integer_add
"""""""""""""""""""""""""



float_add
"""""""""""""""""""""""""



integer_sub
"""""""""""""""""""""""""



float_sub
"""""""""""""""""""""""""



integer_mult
"""""""""""""""""""""""""



float_mult
"""""""""""""""""""""""""



integer_div
"""""""""""""""""""""""""



float_div
"""""""""""""""""""""""""



integer_mod
"""""""""""""""""""""""""



float_mod
"""""""""""""""""""""""""



integer_lt
"""""""""""""""""""""""""



float_lt
"""""""""""""""""""""""""



integer_lte
"""""""""""""""""""""""""



float_lte
"""""""""""""""""""""""""



integer_gt
"""""""""""""""""""""""""



float_gt
"""""""""""""""""""""""""



integer_gte
"""""""""""""""""""""""""



float_gte
"""""""""""""""""""""""""



integer_min
"""""""""""""""""""""""""



float_min
"""""""""""""""""""""""""



integer_max
"""""""""""""""""""""""""



float_max
"""""""""""""""""""""""""



integer_inc
"""""""""""""""""""""""""



float_inc
"""""""""""""""""""""""""



integer_dec
"""""""""""""""""""""""""



float_dec
"""""""""""""""""""""""""



float_sin
"""""""""""""""""""""""""



float_cos
"""""""""""""""""""""""""



float_tan
"""""""""""""""""""""""""



integer_from_float
"""""""""""""""""""""""""



integer_from_boolean
"""""""""""""""""""""""""



float_from_integer
"""""""""""""""""""""""""



foat_from_boolean
"""""""""""""""""""""""""



string_from_integer
"""""""""""""""""""""""""



string_from_float
"""""""""""""""""""""""""



string_from_boolean
"""""""""""""""""""""""""



