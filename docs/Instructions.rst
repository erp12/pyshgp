.. sidebar:: Useful Links

 * `Evolutionary Parameters <Evolutionary_Parameters.html>`_
 * `Instruction Set <Instructions.html>`_
 * `Examples <Examples.html>`_

********************
Pysh Instruction Set
********************

Standard Instruction Set
########################

boolean_and
"""""""""""
Pushes the logical AND of the top two booleans.


boolean_or
""""""""""
Pushes the logical OR of the top two booleans.


boolean_not
"""""""""""
Pushes the logical NOT of the top boolean.


boolean_xor
"""""""""""
Pushes the logical XOR of the top two booleans.


boolean_invert_first_then_and
"""""""""""""""""""""""""""""
Pushes the logical AND of the top two booleans, with the fist argument inverted.


boolean_invert_second_then_and
""""""""""""""""""""""""""""""
Pushes the logical AND of the top two booleans, with the second argument inverted.


boolean_from_integer
""""""""""""""""""""
Pushes the top integer casted to a boolean. If integer is 0, boolean is false. True otherwise.


boolean_from_float
""""""""""""""""""
Pushes the top float casted to a boolean. If float is 0.0, boolean is false. True otherwise.


char_all_from_string
""""""""""""""""""""
Pushes every charecter of the top `string` to the `char` stack.


char_from_integer
"""""""""""""""""
Push the top `integer` converted to a `char`.


char_from_float
"""""""""""""""
Push the top `float` converted to a `char`.


char_is_letter
""""""""""""""
Pushes True if top `char` is a letter. Pushes False otherwise.


char_is_digit
"""""""""""""
Pushes True if top `char` is a digit. Pushes False otherwise.


char_is_white_space
"""""""""""""""""""
Pushes True if top `char` is a whitespace character. Pushes False otherwise.


exec_noop
"""""""""
An instruction that does nothing. (although can still be useful!)


code_noop
"""""""""
An instruction that does nothing. (although can still be useful!)


code_from_boolean
"""""""""""""""""
Takes the top boolean and stores it on the code stack.


code_from_float
"""""""""""""""
Takes the top float and stores it on the code stack.


code_from_integer
"""""""""""""""""
Takes the top integer and stores it on the code stack.


code_from_exec
""""""""""""""
Takes the top item from the exec stack (after the `code_from_exec` instruction) and stores it on the code stack.


code_append
"""""""""""
Takes the top two items from the code stack, appends them into 1 list, and pushes the result onto the code stack.


code_atom
"""""""""
Pushes True if the top item on the code stack is not a list. False otherwise.


code_car
""""""""
Pushes the first item of the list on top of the `code` stack. For example, if the top piece of code is "( A B )" then this pushes "A" (after popping the argument). If the code on top of the stack is not a list then this has no effect.


code_cdr
""""""""
Pushes a version of the list from the top of the `code` stack without its first element. For example, if the top piece of code is "( A B )" then this pushes "( B )" (after popping the argument). If the code on top of the stack is not a list then this pushes the empty list ("( )").


code_cons
"""""""""
Pushes the result of "consing" (in the Lisp sense) the second stack item onto the first stack item (which is coerced to a list if necessary). For example, if the top piece of code is "( A B )" and the second piece of code is "X" then this pushes "( X A B )" (after popping the argument).


code_do
"""""""
 Recursively invokes the interpreter on the program on top of the `code` stack. After evaluation the `code` stack is popped; normally this pops the program that was just executed, but if the expression itself manipulates the stack then this final pop may end up popping something else.


code_do*
""""""""
Like `code_do` but pops the stack before, rather than after, the recursive execution.


code_do*range
"""""""""""""
An iteration instruction that executes the top item on the `code` stack a number of times that depends on the top two integers, while also pushing the loop counter onto the `integer` stack for possible access during the execution of the body of the loop. The top integer is the "destination index" and the second integer is the "current index." First the code and the integer arguments are saved locally and popped. Then the integers are compared. If the integers are equal then the current index is pushed onto the `integer` stack and the code (which is the "body" of the loop) is pushed onto the `exec` stack for subsequent execution. If the integers are not equal then the current index will still be pushed onto the `integer` stack but two items will be pushed onto the `exec` stack -- first a recursive call to `code_do*range` (with the same code and destination index, but with a current index that has been either incremented or decremented by 1 to be closer to the destination index) and then the body code.


exec_do*range
"""""""""""""
An iteration instruction that executes the top item on the `exec` stack a number of times that depends on the top two integers, while also pushing the loop counter onto the `integer` stack for possible access during the execution of the body of the loop. This is similar to `code_do*count` except that it takes its code argument from the `exec` stack. The top integer is the "destination index" and the second integer is the "current index." First the code and the integer arguments are saved locally and popped. Then the integers are compared. If the integers are equal then the current index is pushed onto the `integer` stack and the code (which is the "body" of the loop) is pushed onto the `exec` stack for subsequent execution. If the integers are not equal then the current index will still be pushed onto the `integer` stack but two items will be pushed onto the `exec` stack -- first a recursive call to `exec_do*range` (with the same code and destination index, but with a current index that has been either incremented or decremented by 1 to be closer to the destination index) and then the body code. Note that the range is inclusive of both endpoints; a call with integer arguments 3 and 5 will cause its body to be executed 3 times, with the loop counter having the values 3, 4, and 5. Note also that one can specify a loop that "counts down" by providing a destination index that is less than the specified current index.


code_do*count
"""""""""""""
An iteration instruction that performs a loop (the body of which is taken from the `code` stack) the number of times indicated by the `integer` argument, pushing an index (which runs from zero to one less than the number of iterations) onto the `integer` stack prior to each execution of the loop body.


exec_do*count
"""""""""""""
An iteration instruction that performs a loop (the body of which is taken from the `exec` stack) the number of times indicated by the `integer` argument, pushing an index (which runs from zero to one less than the number of iterations) onto the `integer` stack prior to each execution of the loop body. This is similar to `code_do*count` except that it takes its code argument from the `exec` stack.


code_do*times
"""""""""""""
Like `code_do*count` but does not push the loop counter.


exec_do*times
"""""""""""""
Like `exec_do*count` but does not push the loop counter.


exec_while
""""""""""
Repeats the top item of the exect stack until the boolean stack has a False or is empty.


exec_do*while
"""""""""""""
Pushes the next item on the `exec` stack until the boolean stack has a False or is empty. Similar to `exec_while`, but results in one extra call to the body of the loop.


code_if
"""""""
Pushes the second item of the `code` stack to the `exec` stack if the top boolean is True. Otherwise, pushes the top item of the `code` stack to the `exec` stack.


exec_if
"""""""
Pushes the top item of the `exec` stack (after removing the `exec_if` instruction)  to the `exec` stack if the top boolean is True. Otherwise, pushes the second item of the `exec` stack to the `exec` stack. Differs from `code_if` in the source of the code and in the order of the if/then parts.


exec_when
"""""""""
If the top boolean is False, pop the top item on the `exec` stack (after `exec_when`) effectively skipping it. If top boolean is True, the top item on `exec` stack is untouched and will be evaluated next interation of the program interpretation.


code_length
"""""""""""
Pushes the length of the top item on the `code` stack to the `integer` stack.


code_list
"""""""""
Pushes the top two items of the `code` stack back onto the `code` stack in a list.


code_wrap
"""""""""
Pushes the top item of the code stack back onto the `code` stack inside of a list.


code_member
"""""""""""
Pushes True if the second item on the `code` stack is found in the top item on the code stack. Pushes False otherwise.


code_nth
""""""""
Pushes the nth item of the top item on the `code` stack. To avoid indexing out of bounds, index of nth idem comes form the top `integer` mod the length of the top `code` item.


code_nthcdr
"""""""""""
Pushes the top item on the `code` stack, without the nth item. To avoid indexing out of bounds, index of nth idem comes form the top `integer` mod the length of the top `code` item.


exec_pop
""""""""
Pops the top item off the 'exec' stack.


integer_pop
"""""""""""
Pops the top item off the 'integer' stack.


float_pop
"""""""""
Pops the top item off the 'float' stack.


code_pop
""""""""
Pops the top item off the 'code' stack.


boolean_pop
"""""""""""
Pops the top item off the 'boolean' stack.


string_pop
""""""""""
Pops the top item off the 'string' stack.


char_pop
""""""""
Pops the top item off the 'char' stack.


exec_dup
""""""""
Duplicates the top item of the `exec` stack.


integer_dup
"""""""""""
Duplicates the top item of the `integer` stack.


float_dup
"""""""""
Duplicates the top item of the `float` stack.


code_dup
""""""""
Duplicates the top item of the `code` stack.


boolean_dup
"""""""""""
Duplicates the top item of the `boolean` stack.


string_dup
""""""""""
Duplicates the top item of the `string` stack.


char_dup
""""""""
Duplicates the top item of the `char` stack.


exec_swap
"""""""""
Swaps the top 2 items of the `exec` stack.


integer_swap
""""""""""""
Swaps the top 2 items of the `integer` stack.


float_swap
""""""""""
Swaps the top 2 items of the `float` stack.


code_swap
"""""""""
Swaps the top 2 items of the `code` stack.


boolean_swap
""""""""""""
Swaps the top 2 items of the `boolean` stack.


string_swap
"""""""""""
Swaps the top 2 items of the `string` stack.


char_swap
"""""""""
Swaps the top 2 items of the `char` stack.


exec_rot
""""""""
Rotates the top 3 items of the `exec` stack.


integer_rot
"""""""""""
Rotates the top 3 items of the `integer` stack.


float_rot
"""""""""
Rotates the top 3 items of the `float` stack.


code_rot
""""""""
Rotates the top 3 items of the `code` stack.


boolean_rot
"""""""""""
Rotates the top 3 items of the `boolean` stack.


string_rot
""""""""""
Rotates the top 3 items of the `string` stack.


char_rot
""""""""
Rotates the top 3 items of the `char` stack.


exec_flush
""""""""""
Empties the 'exec' stack.


integer_flush
"""""""""""""
Empties the 'integer' stack.


float_flush
"""""""""""
Empties the 'float' stack.


code_flush
""""""""""
Empties the 'code' stack.


boolean_flush
"""""""""""""
Empties the 'boolean' stack.


string_flush
""""""""""""
Empties the 'string' stack.


char_flush
""""""""""
Empties the 'char' stack.


exec_eq
"""""""
Pushes True if top two items on the `exec` stack are equal. Pushes False otherwise.


integer_eq
""""""""""
Pushes True if top two items on the `integer` stack are equal. Pushes False otherwise.


float_eq
""""""""
Pushes True if top two items on the `float` stack are equal. Pushes False otherwise.


code_eq
"""""""
Pushes True if top two items on the `code` stack are equal. Pushes False otherwise.


boolean_eq
""""""""""
Pushes True if top two items on the `boolean` stack are equal. Pushes False otherwise.


string_eq
"""""""""
Pushes True if top two items on the `string` stack are equal. Pushes False otherwise.


char_eq
"""""""
Pushes True if top two items on the `char` stack are equal. Pushes False otherwise.


exec_stack_depth
""""""""""""""""
Pushes the depth of the `exec` stack to the `integer` stack.


integer_stack_depth
"""""""""""""""""""
Pushes the depth of the `integer` stack to the `integer` stack.


float_stack_depth
"""""""""""""""""
Pushes the depth of the `float` stack to the `integer` stack.


code_stack_depth
""""""""""""""""
Pushes the depth of the `code` stack to the `integer` stack.


boolean_stack_depth
"""""""""""""""""""
Pushes the depth of the `boolean` stack to the `integer` stack.


string_stack_depth
""""""""""""""""""
Pushes the depth of the `string` stack to the `integer` stack.


char_stack_depth
""""""""""""""""
Pushes the depth of the `char` stack to the `integer` stack.


exec_yank
"""""""""
Yanks an item from deep in the `exec` stack, using the top `integer` to indicate how deep.


integer_yank
""""""""""""
Yanks an item from deep in the `integer` stack, using the top `integer` to indicate how deep.


float_yank
""""""""""
Yanks an item from deep in the `float` stack, using the top `integer` to indicate how deep.


code_yank
"""""""""
Yanks an item from deep in the `code` stack, using the top `integer` to indicate how deep.


boolean_yank
""""""""""""
Yanks an item from deep in the `boolean` stack, using the top `integer` to indicate how deep.


string_yank
"""""""""""
Yanks an item from deep in the `string` stack, using the top `integer` to indicate how deep.


char_yank
"""""""""
Yanks an item from deep in the `char` stack, using the top `integer` to indicate how deep.


exec_yankdup
""""""""""""
Yanks a copy of an item from deep in the `exec` stack, using the top `integer` to indicate how deep.


integer_yankdup
"""""""""""""""
Yanks a copy of an item from deep in the `integer` stack, using the top `integer` to indicate how deep.


float_yankdup
"""""""""""""
Yanks a copy of an item from deep in the `float` stack, using the top `integer` to indicate how deep.


code_yankdup
""""""""""""
Yanks a copy of an item from deep in the `code` stack, using the top `integer` to indicate how deep.


boolean_yankdup
"""""""""""""""
Yanks a copy of an item from deep in the `boolean` stack, using the top `integer` to indicate how deep.


string_yankdup
""""""""""""""
Yanks a copy of an item from deep in the `string` stack, using the top `integer` to indicate how deep.


char_yankdup
""""""""""""
Yanks a copy of an item from deep in the `char` stack, using the top `integer` to indicate how deep.


exec_shove
""""""""""
Shoves an item deep in the `exec` stack, using the top `integer` to indicate how deep.


integer_shove
"""""""""""""
Shoves an item deep in the `integer` stack, using the top `integer` to indicate how deep.


float_shove
"""""""""""
Shoves an item deep in the `float` stack, using the top `integer` to indicate how deep.


code_shove
""""""""""
Shoves an item deep in the `code` stack, using the top `integer` to indicate how deep.


boolean_shove
"""""""""""""
Shoves an item deep in the `boolean` stack, using the top `integer` to indicate how deep.


string_shove
""""""""""""
Shoves an item deep in the `string` stack, using the top `integer` to indicate how deep.


char_shove
""""""""""
Shoves an item deep in the `char` stack, using the top `integer` to indicate how deep.


exec_empty
""""""""""
Pushes True if the `exec` stack is empty. Pushes False otherwise.


integer_empty
"""""""""""""
Pushes True if the `integer` stack is empty. Pushes False otherwise.


float_empty
"""""""""""
Pushes True if the `float` stack is empty. Pushes False otherwise.


code_empty
""""""""""
Pushes True if the `code` stack is empty. Pushes False otherwise.


boolean_empty
"""""""""""""
Pushes True if the `boolean` stack is empty. Pushes False otherwise.


string_empty
""""""""""""
Pushes True if the `string` stack is empty. Pushes False otherwise.


char_empty
""""""""""
Pushes True if the `char` stack is empty. Pushes False otherwise.


integer_add
"""""""""""
Pushes the result of adding the top two integers.


float_add
"""""""""
Pushes the result of adding the top two floats.


integer_sub
"""""""""""
Pushes the difference of the top two integers.


float_sub
"""""""""
Pushes the difference of the top two floats.


integer_mult
""""""""""""
Pushes the product of the top two integers.


float_mult
""""""""""
Pushes the product of the top two floats.


integer_div
"""""""""""
Pushes the quotient of the top two integers.


float_div
"""""""""
Pushes the quotient of the top two floats.


integer_mod
"""""""""""
Pushes the result of the second integer modulous the first integer.


float_mod
"""""""""
Pushes the result of the second float modulous the first float.


integer_lt
""""""""""
Push a boolean based on if the second integer is less than the top integer.


float_lt
""""""""
Push a boolean based on if the second float is less than the top float.


integer_lte
"""""""""""
Push a boolean based on if the second integer is less than, or equal to, the top integer.


float_lte
"""""""""
Push a boolean based on if the second float is less than, or equal to, the top float.


integer_gt
""""""""""
Push a boolean based on if the second integer is greater than the top integer.


float_gt
""""""""
Push a boolean based on if the second float is greater than the top float.


integer_gte
"""""""""""
Push a boolean based on if the second integer is greater than, or equal to, the top integer.


float_gte
"""""""""
Push a boolean based on if the second float is greater than, or equal to, the top float.


integer_min
"""""""""""
Pushes the minimum of the top two integers.


float_min
"""""""""
Pushes the minimum of the top two floats.


integer_max
"""""""""""
Pushes the maximum of the top two integers.


float_max
"""""""""
Pushes the maximum of the top two floats.


integer_inc
"""""""""""
Pushes the result of incrementing the top integer by 1.


float_inc
"""""""""
Pushes the result of incrementing the top float by 1.0.


integer_dec
"""""""""""
Pushes the result of decrementing the top integer by 1.


float_dec
"""""""""
Pushes the result of decrementing the top float by 1.0.


float_sin
"""""""""
Puses the sin of the top float.


float_cos
"""""""""
Pushes the cos of the top float.


float_tan
"""""""""
Pushes the tangent of the top float.


integer_from_float
""""""""""""""""""
Pushes the top float cast to an integer.


integer_from_boolean
""""""""""""""""""""
Pushes the top boolean cast to an integer.


integer_from_string
"""""""""""""""""""
Pushes the top string cast to an integer.


integer_from_char
"""""""""""""""""
Pushes the top `char` cast to an `integer`.


float_from_integer
""""""""""""""""""
Push the top integer cast to a float.


foat_from_boolean
"""""""""""""""""
Pushes top boolean cast to a float.


float_from_string
"""""""""""""""""
Pushes the top string cast to an float.


float_from_char
"""""""""""""""
Pushes the top `char` cast to an `float`.


string_from_integer
"""""""""""""""""""
Casts the top integer to a string and pushes the result onto the string stack.


string_from_float
"""""""""""""""""
Casts the top float to a string and pushes the result onto the string stack.


string_from_boolean
"""""""""""""""""""
Casts the top boolean to a string and pushes the result onto the string stack.


string_concat
"""""""""""""
Pops top 2 strings, and pushes result of concatenating those strings to the string stack.


string_head
"""""""""""
Pushed a string of the first i chars in s. i is top integer. s is top string.


string_tail
"""""""""""
Pushed a string of the last i chars in s. i is top integer. s is top string.


string_split_at_index
"""""""""""""""""""""
Pushes 2 strings from top string being split at index given by top integer.


string_split_at_str
"""""""""""""""""""
Pushes all strings resulting from the second string being split on top string.


string_split_at_char
""""""""""""""""""""
Pushes all strings resulting from the top `string` being split on top `char`.


string_split_at_space
"""""""""""""""""""""
Pushes all strings resulting from spliting top string on space characters.


string_length
"""""""""""""
Pushes integer equal to length of top string.


string_reverse
""""""""""""""
Pushes top string reversed.


string_char_at
""""""""""""""
Pushes string of character in top string at index given by top integer.


string_empty_string
"""""""""""""""""""
Pushes True if top string is an emptry string. Pushes False otherwise.


string_contains
"""""""""""""""
Pushes True if the top string is a substring of the second string. False otherwise.


string_replace
""""""""""""""
Replaces all instances of second string with the top string in the third string. Pushes the result.


string_from_char
""""""""""""""""
Pushed the top `char` to the `string` stack.


string_append_char
""""""""""""""""""
Appends the top `char` to the top `string` and pushes result to the `string` stack.


string_first
""""""""""""
Pushes the first `char` of the top `string`.


string_last
"""""""""""
Pushes the last `char` of the top `string`.


string_nth
""""""""""
Pushes the nth `char` of the top `string`. n is the top `integer` mod the length of the top `string`.


string_replace_char
"""""""""""""""""""
Pushes the top `string` with all occurences of second `char` replaced with the top `char`.


string_replace_first_char
"""""""""""""""""""""""""
Pushes the top `string` with the first occurence of second `char` replaced with the top `char`.


string_remove_char
""""""""""""""""""
Pushes the top `string` with all occurences of top `char` removed.


Special Instructions
####################

.. toctree::
   :maxdepth: 1

   custom_instructions
