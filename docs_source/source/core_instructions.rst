***************************
PyshGP Core Instruction Set
***************************
int_add
=======
*Takes: [int, int] - Produces: [int]*

Adds the top two ints and pushes the result.

int_sub
=======
*Takes: [int, int] - Produces: [int]*

Subtracts the top two ints and pushes the result.

int_mult
========
*Takes: [int, int] - Produces: [int]*

Multiplies the top two ints and pushes the result.

int_div
=======
*Takes: [int, int] - Produces: [int]*

Divides the top two ints and pushes the result.

int_mod
=======
*Takes: [int, int] - Produces: [int]*

Computes the modulous of the top two ints and pushes the result.

int_min
=======
*Takes: [int, int] - Produces: [int]*

Pushes the minimum of two int.

int_max
=======
*Takes: [int, int] - Produces: [int]*

Pushes the maximum of two int.

int_inc
=======
*Takes: [int] - Produces: [int]*

Increments the top int by 1.

int_dec
=======
*Takes: [int] - Produces: [int]*

Decrements the top int by 1.

int_lt
======
*Takes: [int, int] - Produces: [bool]*

Pushes true if the top int is less than the second. Pushes false otherwise.

int_lte
=======
*Takes: [int, int] - Produces: [bool]*

Pushes true if the top int is less than, or equal to, the second. Pushes false otherwise.

int_gt
======
*Takes: [int, int] - Produces: [bool]*

Pushes true if the top int is greater than the second.. Pushes false otherwise.

int_gte
=======
*Takes: [int, int] - Produces: [bool]*

Pushes true if the top int is greater than, or equal to, the second. Pushes false otherwise.

float_add
=========
*Takes: [float, float] - Produces: [float]*

Adds the top two floats and pushes the result.

float_sub
=========
*Takes: [float, float] - Produces: [float]*

Subtracts the top two floats and pushes the result.

float_mult
==========
*Takes: [float, float] - Produces: [float]*

Multiplies the top two floats and pushes the result.

float_div
=========
*Takes: [float, float] - Produces: [float]*

Divides the top two floats and pushes the result.

float_mod
=========
*Takes: [float, float] - Produces: [float]*

Computes the modulous of the top two floats and pushes the result.

float_min
=========
*Takes: [float, float] - Produces: [float]*

Pushes the minimum of two float.

float_max
=========
*Takes: [float, float] - Produces: [float]*

Pushes the maximum of two float.

float_inc
=========
*Takes: [float] - Produces: [float]*

Increments the top float by 1.

float_dec
=========
*Takes: [float] - Produces: [float]*

Decrements the top float by 1.

float_lt
========
*Takes: [float, float] - Produces: [bool]*

Pushes true if the top float is less than the second. Pushes false otherwise.

float_lte
=========
*Takes: [float, float] - Produces: [bool]*

Pushes true if the top float is less than, or equal to, the second. Pushes false otherwise.

float_gt
========
*Takes: [float, float] - Produces: [bool]*

Pushes true if the top float is greater than the second.. Pushes false otherwise.

float_gte
=========
*Takes: [float, float] - Produces: [bool]*

Pushes true if the top float is greater than, or equal to, the second. Pushes false otherwise.

float_sin
=========
*Takes: [float] - Produces: [float]*

Pushes the sin of the top float.

float_cos
=========
*Takes: [float] - Produces: [float]*

Pushes the cos of the top float.

float_tan
=========
*Takes: [float] - Produces: [float]*

Pushes the tan of the top float.

int_from_bool
=============
*Takes: [bool] - Produces: [int]*

Pushes 1 in the top boolean is true. Pushes 0 if the top boolean is false.

float_from_bool
===============
*Takes: [bool] - Produces: [float]*

Pushes 1.0 in the top boolean is true. Pushes 0.0 if the top boolean is false.

int_from_float
==============
*Takes: [float] - Produces: [int]*

Casts the top float to an integer and pushes the result.

float_from_int
==============
*Takes: [int] - Produces: [float]*

Casts the top integer to a float and pushes the result.

str_concat
==========
*Takes: [str, str] - Produces: [str]*

Concatenates the top two strs and pushes the resulting string.

str_insert_str
==============
*Takes: [str, str, int] - Produces: [str]*

Inserts str into the top str at index `n` and pushes
            the resulting string. The value for `n` is taken from the int stack.

str_from_first_char
===================
*Takes: [str] - Produces: [str]*

Pushes a str of the first character of the top string.

str_from_last_char
==================
*Takes: [str] - Produces: [str]*

Pushes a str of the last character of the top string.

str_from_nth_char
=================
*Takes: [str, int] - Produces: [str]*

Pushes a str of the nth character of the top string. The top integer denotes nth position.

str_contains_str
================
*Takes: [str, str] - Produces: [bool]*

Pushes true if the next str is in the top string. Pushes false otherwise.

str_index_of_str
================
*Takes: [str, str] - Produces: [int]*

Pushes the index of the next str in the top string. If not found, pushes -1.

str_split_on_str
================
*Takes: [str, str] - Produces: Arbitrary number of str values.*

Pushes multiple strs produced by splitting the top str on the top str.

str_replace_first_str
=====================
*Takes: [str, str, str] - Produces: [str]*

Pushes the str produced by replaceing the first occurrence of the
            top str with the second str.

str_replace_n_str
=================
*Takes: [str, str, str, int] - Produces: [str]*

Pushes the str produced by replaceing the first `n` occurrences of the
            top str with the second str. The value for `n` is the top int.

str_replace_all_str
===================
*Takes: [str, str, str] - Produces: [str]*

Pushes the str produced by replaceing all occurrences of the
            top str with the second str.

str_remove_first_str
====================
*Takes: [str, str] - Produces: [str]*

Pushes the str produced by removing the first occurrence of the top str.

str_remove_n_str
================
*Takes: [str, str, int] - Produces: [str]*

Pushes the str produced by remvoing the first `n` occurrences of the
            top str. The value for `n` is the top int.

str_remove_all_str
==================
*Takes: [str, str] - Produces: [str]*

Pushes the str produced by removing all occurrences of the top str.

str_occurrences_of_str
======================
*Takes: [str, str] - Produces: [int]*

Pushes the number of times the top str occurs in the top str to the int stack.

char_concat
===========
*Takes: [char, char] - Produces: [str]*

Concatenates the top two chars and pushes the resulting string.

str_insert_char
===============
*Takes: [str, char, int] - Produces: [str]*

Inserts char into the top str at index `n` and pushes
            the resulting string. The value for `n` is taken from the int stack.

char_from_first_char
====================
*Takes: [str] - Produces: [char]*

Pushes a char of the first character of the top string.

char_from_last_char
===================
*Takes: [str] - Produces: [char]*

Pushes a char of the last character of the top string.

char_from_nth_char
==================
*Takes: [str, int] - Produces: [char]*

Pushes a char of the nth character of the top string. The top integer denotes nth position.

str_contains_char
=================
*Takes: [str, char] - Produces: [bool]*

Pushes true if the next char is in the top string. Pushes false otherwise.

str_index_of_char
=================
*Takes: [str, char] - Produces: [int]*

Pushes the index of the next char in the top string. If not found, pushes -1.

str_split_on_char
=================
*Takes: [str, char] - Produces: Arbitrary number of str values.*

Pushes multiple strs produced by splitting the top str on the top char.

str_replace_first_char
======================
*Takes: [str, char, char] - Produces: [str]*

Pushes the str produced by replaceing the first occurrence of the
            top char with the second char.

str_replace_n_char
==================
*Takes: [str, char, char, int] - Produces: [str]*

Pushes the str produced by replaceing the first `n` occurrences of the
            top char with the second char. The value for `n` is the top int.

str_replace_all_char
====================
*Takes: [str, char, char] - Produces: [str]*

Pushes the str produced by replaceing all occurrences of the
            top char with the second char.

str_remove_first_char
=====================
*Takes: [str, char] - Produces: [str]*

Pushes the str produced by removing the first occurrence of the top char.

str_remove_n_char
=================
*Takes: [str, char, int] - Produces: [str]*

Pushes the str produced by remvoing the first `n` occurrences of the
            top char. The value for `n` is the top int.

str_remove_all_char
===================
*Takes: [str, char] - Produces: [str]*

Pushes the str produced by removing all occurrences of the top char.

str_occurrences_of_char
=======================
*Takes: [str, char] - Produces: [int]*

Pushes the number of times the top char occurs in the top str to the int stack.

str_reverse
===========
*Takes: [str] - Produces: [str]*

Takes the top string and pushes it reversed.

str_head
========
*Takes: [str, int] - Produces: [str]*

Pushes a string of the first `n` characters from the top string. The value
        for `n` is the top int mod the length of the string.

str_tail
========
*Takes: [str, int] - Produces: [str]*

Pushes a string of the last `n` characters from the top string. The value
        for `n` is the top int mod the length of the string.

str_append_char
===============
*Takes: [str, char] - Produces: [str]*

Appends the top char to the top string pushes the resulting string.

str_rest
========
*Takes: [str] - Produces: [str]*

Pushes the top str without its first character.

str_but_last
============
*Takes: [str] - Produces: [str]*

Pushes the top str without its last character.

str_drop
========
*Takes: [str, int] - Produces: [str]*

Pushes the top str without its first `n` character. The value for `n`
        is the top int mod the length of the string.

str_but_last_n
==============
*Takes: [str, int] - Produces: [str]*

Pushes the top str without its last `n` character. The value for `n`
        is the top int mod the length of the string.

str_length
==========
*Takes: [str] - Produces: [int]*

Pushes the length of the top str to the int stack.

str_make_empty
==============
*Takes: [] - Produces: [str]*

Pushes an empty string.

str_is_empty_string
===================
*Takes: [str] - Produces: [bool]*

Pushes True if top string is empty. Pushes False otherwise.

str_remove_nth
==============
*Takes: [str, int] - Produces: [str]*

Pushes the top str with the nth character removed.

str_set_nth
===========
*Takes: [str, char, int] - Produces: [str]*

Pushes the top str with the nth character set to the top character.

str_strip_whitespace
====================
*Takes: [str] - Produces: [str]*

Pushes the top str with trailing and leading whitespace stripped.

char_is_whitespace
==================
*Takes: [char] - Produces: [bool]*

Pushes True if the top Char is whitespace. Pushes False otherwise.

char_is_letter
==============
*Takes: [char] - Produces: [bool]*

Pushes True if the top Char is a letter. Pushes False otherwise.

char_is_digit
=============
*Takes: [char] - Produces: [bool]*

Pushes True if the top Char is a numeric digit. Pushes False otherwise.

str_from_bool
=============
*Takes: [bool] - Produces: [str]*

Pushes the top bool converted into a str.

str_from_int
============
*Takes: [int] - Produces: [str]*

Pushes the top int converted into a str.

str_from_float
==============
*Takes: [float] - Produces: [str]*

Pushes the top float converted into a str.

str_from_char
=============
*Takes: [char] - Produces: [str]*

Pushes the top char converted into a str.

char_from_bool
==============
*Takes: [bool] - Produces: [char]*

Pushes the char "T" if the top bool is True. If the top
        bool is False, pushes the char "F".

char_from_ascii_int
===================
*Takes: [int] - Produces: [char]*

Pushes the top int converted into a Character by using the int mod 128 as an ascii value.

_char_from_float
================
*Takes: [float] - Produces: [char]*

Pushes the top float converted into a Character by flooring
        the float to an int, taking the int mod 128, and using it as an ascii value.

chars_from_str
==============
*Takes: [str] - Produces: Arbitrary number of char values.*

Pushes each character of the top str to the char stack in reverse order.

bool_and
========
*Takes: [bool, bool] - Produces: [bool]*

Pushes the result of and-ing the top two booleans.

bool_or
=======
*Takes: [bool, bool] - Produces: [bool]*

Pushes the result of or-ing the top two booleans.

bool_not
========
*Takes: [bool] - Produces: [bool]*

Pushes the inverse of the boolean.

bool_xor
========
*Takes: [bool, bool] - Produces: [bool]*

Pushes the result of xor-ing the top two booleans.

bool_invert_first_then_and
==========================
*Takes: [bool, bool] - Produces: [bool]*

"Pushes the result of and-ing the top two booleans after inverting the
        top boolean.

bool_second_first_then_and
==========================
*Takes: [bool, bool] - Produces: [bool]*

"Pushes the result of and-ing the top two booleans after inverting the
        second boolean.

bool_from_int
=============
*Takes: [int] - Produces: [bool]*

If the top int is 0, pushes False. Pushes True for any other int value.

bool_from_float
===============
*Takes: [float] - Produces: [bool]*

If the top float is 0.0, pushes False. Pushes True for any other float value.

noop
====
*Takes: [] - Produces: []*

A noop SimpleInstruction which does nothing.

noop_open
=========
*Takes: [] - Produces: [] - Opens 1 code blocks*

A noop SimpleInstruction which does nothing. Opens a code block.

code_is_code_block
==================
*Takes: [code] - Produces: [bool]*

Push True if top item on code stack is a CodeBlock. False otherwise.

code_is_singular
================
*Takes: [code] - Produces: [bool]*

Push True if top item on code stack is a not CodeBlock. False otherwise.

code_length
===========
*Takes: [code] - Produces: [int]*

If the top code item is a CodeBlock, pushes its length, otherwise pushes 1.

code_first
==========
*Takes: [code] - Produces: [code]*

If the top code item is a CodeBlock, pushes its first element.

code_last
=========
*Takes: [code] - Produces: [code]*

If the top code item is a CodeBlock, pushes its last element.

code_rest
=========
*Takes: [code] - Produces: [code]*

If the top code item is a CodeBlock, pushes it to the code stack without its first element.

code_but_last
=============
*Takes: [code] - Produces: [code]*

If the top code item is a CodeBlock, pushes it to the code stack without its last element.

code_wrap
=========
*Takes: [code] - Produces: [code]*

Wraps the top item on the code stack in a CodeBlock.

code_list
=========
*Takes: [code, code] - Produces: [code]*

Wraps the top two items on the code stack in a CodeBlock.

code_combine
============
*Takes: [code, code] - Produces: [code]*

Combines the top two items on the code stack in a CodeBlock.
        If one items is a CodeBlock, the other item is appended to it. If both
        items are CodeBlocks, they are concatenated together.

code_do
=======
*Takes: [code] - Produces: [exec]*

Moves the top element of the code stack to the exec stack for execution.

code_do_dup
===========
*Takes: [code] - Produces: [exec, code]*

Copies the top element of the code stack to the exec stack for execution.

code_do_then_pop
================
*Takes: PushState - Produces: PushState*

Pushes a `code_pop` JitInstructionRef and the top item of the
        code stack to the exec stack. Result is the top code item executing before
        it is removed from the code stack.

code_do_range
=============
*Takes: PushState - Produces: PushState*

Evaluates the top item on the code stack for each step along
        the range `i` to `j`. Both `i` and `j` are taken from the int stack.

exec_do_range
=============
*Takes: PushState - Produces: PushState - Opens 1 code blocks*

Evaluates the top item on the exec stack for each step along
        the range `i` to `j`. Both `i` and `j` are taken from the int stack.
        Differs from code_do_range only in the source of the code and the
        recursive call.

code_do_count
=============
*Takes: PushState - Produces: PushState*

Evaluates the top item on the code stack `n` times, where
        `n` comes from the `n` comes from the top of the int stack.

exec_do_count
=============
*Takes: PushState - Produces: PushState - Opens 1 code blocks*

Evaluates the top item on the exec stack `n` times, where
        `n` comes from the `n` comes from the top of the int stack. Differs from
        code.do*count only in the source of the code and the recursive call.

code_do_times
=============
*Takes: PushState - Produces: PushState*

Evaluates the top item on the code stack `n` times, where
        `n` comes from the `n` comes from the top of the int stack.

exec_do_times
=============
*Takes: PushState - Produces: PushState - Opens 1 code blocks*

Evaluates the top item on the code stack `n` times, where
        `n` comes from the `n` comes from the top of the int stack.

exec_while
==========
*Takes: PushState - Produces: PushState - Opens 1 code blocks*

Evaluates the top item on the exec stack repeated until the top
        bool is no longer True.

exec_do_while
=============
*Takes: PushState - Produces: PushState - Opens 1 code blocks*

Evaluates the top item on the exec stack repeated until the top
        bool is no longer True.

code_map
========
*Takes: PushState - Produces: PushState*

Evaluates the top item on the exec stack for each element of the top
        CodeBlock on the code stack. If the top code item is not a CodeBlock, it is wrapped
        into one.

code_if
=======
*Takes: [bool, code, code] - Produces: [exec]*

If the top boolean is true, execute the top element of the code
        stack and skip the second. Otherwise, skip the top element of the
        code stack and execute the second.

exec_if
=======
*Takes: [bool, exec, exec] - Produces: [exec] - Opens 2 code blocks*

If the top boolean is true, execute the top element of the exec
        stack and skip the second. Otherwise, skip the top element of the
        exec stack and execute the second.

code_when
=========
*Takes: PushState - Produces: PushState*

Evalutates the top code item if the top bool is True.
        Otherwise the top code is popped.

exec_when
=========
*Takes: PushState - Produces: PushState - Opens 1 code blocks*

Pops the next item on the exec stack without evaluating it
        if the top bool is False. Otherwise, has no effect.

code_member
===========
*Takes: [code, code] - Produces: [bool]*

Pushes True if the second code item is a found within the top code item.
        If the top code item is not a CodeBlock, it is wrapped.

code_nth
========
*Takes: [code, int] - Produces: [code]*

Pushes nth item of the top element on the code stack. If
        the top item is not a CodeBlock it is wrapped in a CodeBlock.

make_empty_code_block
=====================
*Takes: [] - Produces: [code]*

Pushes an empty CodeBlock to the code stack.

is_empty_code_block
===================
*Takes: [code] - Produces: [bool]*

Pushes true if top code item is an empty CodeBlock. Pushes
        false otherwise.

code_size
=========
*Takes: [code] - Produces: [int]*

Pushes the total size of the top item on the code stack. If
        the top item is a CodeBlock, this includes the size of all the CodeBlock's
        elements recusively.

code_extract
============
*Takes: [code, int] - Produces: [code]*

Traverses the top code item depth first and returns the nth
        item based on the top int.

code_insert
===========
*Takes: [code, code, int] - Produces: [code]*

Traverses the top code item depth first and inserts the
        second code item at position `n`. The value of `n` is the top int.

code_first_position
===================
*Takes: [code, code] - Produces: [int]*

Pushes the first position of the second code item within
        the top code item. If not found, pushes -1. If the top code item is not
        a CodeBlock, this instruction returns 0 if the top two code elements are
        equal and -1 otherwise.

code_reverse
============
*Takes: [code] - Produces: [code]*

Pushes the top code item reversed. No effect if top code
        item is not a CodeBlock.

print_bool
==========
*Takes: [bool] - Produces: [stdout]*

Prints the top bool.

print_int
=========
*Takes: [int] - Produces: [stdout]*

Prints the top int.

print_char
==========
*Takes: [char] - Produces: [stdout]*

Prints the top char.

print_float
===========
*Takes: [float] - Produces: [stdout]*

Prints the top float.

print_str
=========
*Takes: [str] - Produces: [stdout]*

Prints the top str.

print_code
==========
*Takes: [code] - Produces: [stdout]*

Prints the top code.

print_exec
==========
*Takes: [exec] - Produces: [stdout]*

Prints the top exec.

bool_pop
========
*Takes: [bool] - Produces: []*

Pops the top bool.

bool_dup
========
*Takes: [bool] - Produces: [bool, bool]*

Duplicates the top bool.

bool_dup_times
==============
*Takes: [int, bool] - Produces: Arbitrary number of bool values.*

Duplicates the top bool `n` times where `n` is from the int stack.

bool_swap
=========
*Takes: [bool, bool] - Produces: [bool, bool]*

Swaps the top two bools.

bool_rot
========
*Takes: [bool, bool, bool] - Produces: [bool, bool, bool]*

Rotates the top three bools.

bool_flush
==========
*Takes: PushState - Produces: PushState*

Empties the bool stack.

bool_eq
=======
*Takes: [bool, bool] - Produces: [bool]*

Pushes True if the top two bool are equal. Otherwise pushes False.

bool_stack_depth
================
*Takes: PushState - Produces: [int]*

Pushes the size of the bool stack to the int stack.

bool_yank
=========
*Takes: PushState - Produces: PushState*

Yanks a bool from deep in the stack based on an index from the int stack and puts it on top.

bool_yank_dup
=============
*Takes: PushState - Produces: PushState*

Yanks a copy of a bool deep in the stack based on an index from the int stack and puts it on top.

bool_shove
==========
*Takes: PushState - Produces: PushState*

Shoves the top bool deep in the stack based on an index from the int stack.

bool_shove_dup
==============
*Takes: PushState - Produces: PushState*

Shoves a copy of the top bool deep in the stack based on an index from the int stack.

bool_is_empty
=============
*Takes: PushState - Produces: [bool]*

Pushes True if the bool stack is empty. Pushes False otherwise.

int_pop
=======
*Takes: [int] - Produces: []*

Pops the top int.

int_dup
=======
*Takes: [int] - Produces: [int, int]*

Duplicates the top int.

int_dup_times
=============
*Takes: [int, int] - Produces: Arbitrary number of int values.*

Duplicates the top int `n` times where `n` is from the int stack.

int_swap
========
*Takes: [int, int] - Produces: [int, int]*

Swaps the top two ints.

int_rot
=======
*Takes: [int, int, int] - Produces: [int, int, int]*

Rotates the top three ints.

int_flush
=========
*Takes: PushState - Produces: PushState*

Empties the int stack.

int_eq
======
*Takes: [int, int] - Produces: [bool]*

Pushes True if the top two int are equal. Otherwise pushes False.

int_stack_depth
===============
*Takes: PushState - Produces: [int]*

Pushes the size of the int stack to the int stack.

int_yank
========
*Takes: PushState - Produces: PushState*

Yanks a int from deep in the stack based on an index from the int stack and puts it on top.

int_yank_dup
============
*Takes: PushState - Produces: PushState*

Yanks a copy of a int deep in the stack based on an index from the int stack and puts it on top.

int_shove
=========
*Takes: PushState - Produces: PushState*

Shoves the top int deep in the stack based on an index from the int stack.

int_shove_dup
=============
*Takes: PushState - Produces: PushState*

Shoves a copy of the top int deep in the stack based on an index from the int stack.

int_is_empty
============
*Takes: PushState - Produces: [bool]*

Pushes True if the int stack is empty. Pushes False otherwise.

char_pop
========
*Takes: [char] - Produces: []*

Pops the top char.

char_dup
========
*Takes: [char] - Produces: [char, char]*

Duplicates the top char.

char_dup_times
==============
*Takes: [int, char] - Produces: Arbitrary number of char values.*

Duplicates the top char `n` times where `n` is from the int stack.

char_swap
=========
*Takes: [char, char] - Produces: [char, char]*

Swaps the top two chars.

char_rot
========
*Takes: [char, char, char] - Produces: [char, char, char]*

Rotates the top three chars.

char_flush
==========
*Takes: PushState - Produces: PushState*

Empties the char stack.

char_eq
=======
*Takes: [char, char] - Produces: [bool]*

Pushes True if the top two char are equal. Otherwise pushes False.

char_stack_depth
================
*Takes: PushState - Produces: [int]*

Pushes the size of the char stack to the int stack.

char_yank
=========
*Takes: PushState - Produces: PushState*

Yanks a char from deep in the stack based on an index from the int stack and puts it on top.

char_yank_dup
=============
*Takes: PushState - Produces: PushState*

Yanks a copy of a char deep in the stack based on an index from the int stack and puts it on top.

char_shove
==========
*Takes: PushState - Produces: PushState*

Shoves the top char deep in the stack based on an index from the int stack.

char_shove_dup
==============
*Takes: PushState - Produces: PushState*

Shoves a copy of the top char deep in the stack based on an index from the int stack.

char_is_empty
=============
*Takes: PushState - Produces: [bool]*

Pushes True if the char stack is empty. Pushes False otherwise.

float_pop
=========
*Takes: [float] - Produces: []*

Pops the top float.

float_dup
=========
*Takes: [float] - Produces: [float, float]*

Duplicates the top float.

float_dup_times
===============
*Takes: [int, float] - Produces: Arbitrary number of float values.*

Duplicates the top float `n` times where `n` is from the int stack.

float_swap
==========
*Takes: [float, float] - Produces: [float, float]*

Swaps the top two floats.

float_rot
=========
*Takes: [float, float, float] - Produces: [float, float, float]*

Rotates the top three floats.

float_flush
===========
*Takes: PushState - Produces: PushState*

Empties the float stack.

float_eq
========
*Takes: [float, float] - Produces: [bool]*

Pushes True if the top two float are equal. Otherwise pushes False.

float_stack_depth
=================
*Takes: PushState - Produces: [int]*

Pushes the size of the float stack to the int stack.

float_yank
==========
*Takes: PushState - Produces: PushState*

Yanks a float from deep in the stack based on an index from the int stack and puts it on top.

float_yank_dup
==============
*Takes: PushState - Produces: PushState*

Yanks a copy of a float deep in the stack based on an index from the int stack and puts it on top.

float_shove
===========
*Takes: PushState - Produces: PushState*

Shoves the top float deep in the stack based on an index from the int stack.

float_shove_dup
===============
*Takes: PushState - Produces: PushState*

Shoves a copy of the top float deep in the stack based on an index from the int stack.

float_is_empty
==============
*Takes: PushState - Produces: [bool]*

Pushes True if the float stack is empty. Pushes False otherwise.

str_pop
=======
*Takes: [str] - Produces: []*

Pops the top str.

str_dup
=======
*Takes: [str] - Produces: [str, str]*

Duplicates the top str.

str_dup_times
=============
*Takes: [int, str] - Produces: Arbitrary number of str values.*

Duplicates the top str `n` times where `n` is from the int stack.

str_swap
========
*Takes: [str, str] - Produces: [str, str]*

Swaps the top two strs.

str_rot
=======
*Takes: [str, str, str] - Produces: [str, str, str]*

Rotates the top three strs.

str_flush
=========
*Takes: PushState - Produces: PushState*

Empties the str stack.

str_eq
======
*Takes: [str, str] - Produces: [bool]*

Pushes True if the top two str are equal. Otherwise pushes False.

str_stack_depth
===============
*Takes: PushState - Produces: [int]*

Pushes the size of the str stack to the int stack.

str_yank
========
*Takes: PushState - Produces: PushState*

Yanks a str from deep in the stack based on an index from the int stack and puts it on top.

str_yank_dup
============
*Takes: PushState - Produces: PushState*

Yanks a copy of a str deep in the stack based on an index from the int stack and puts it on top.

str_shove
=========
*Takes: PushState - Produces: PushState*

Shoves the top str deep in the stack based on an index from the int stack.

str_shove_dup
=============
*Takes: PushState - Produces: PushState*

Shoves a copy of the top str deep in the stack based on an index from the int stack.

str_is_empty
============
*Takes: PushState - Produces: [bool]*

Pushes True if the str stack is empty. Pushes False otherwise.

code_pop
========
*Takes: [code] - Produces: []*

Pops the top code.

code_dup
========
*Takes: [code] - Produces: [code, code]*

Duplicates the top code.

code_dup_times
==============
*Takes: [int, code] - Produces: Arbitrary number of code values.*

Duplicates the top code `n` times where `n` is from the int stack.

code_swap
=========
*Takes: [code, code] - Produces: [code, code]*

Swaps the top two codes.

code_rot
========
*Takes: [code, code, code] - Produces: [code, code, code]*

Rotates the top three codes.

code_flush
==========
*Takes: PushState - Produces: PushState*

Empties the code stack.

code_eq
=======
*Takes: [code, code] - Produces: [bool]*

Pushes True if the top two code are equal. Otherwise pushes False.

code_stack_depth
================
*Takes: PushState - Produces: [int]*

Pushes the size of the code stack to the int stack.

code_yank
=========
*Takes: PushState - Produces: PushState*

Yanks a code from deep in the stack based on an index from the int stack and puts it on top.

code_yank_dup
=============
*Takes: PushState - Produces: PushState*

Yanks a copy of a code deep in the stack based on an index from the int stack and puts it on top.

code_shove
==========
*Takes: PushState - Produces: PushState*

Shoves the top code deep in the stack based on an index from the int stack.

code_shove_dup
==============
*Takes: PushState - Produces: PushState*

Shoves a copy of the top code deep in the stack based on an index from the int stack.

code_is_empty
=============
*Takes: PushState - Produces: [bool]*

Pushes True if the code stack is empty. Pushes False otherwise.

exec_pop
========
*Takes: [exec] - Produces: [] - Opens 1 code blocks*

Pops the top exec.

exec_dup
========
*Takes: [exec] - Produces: [exec, exec] - Opens 1 code blocks*

Duplicates the top exec.

exec_dup_times
==============
*Takes: [int, exec] - Produces: Arbitrary number of exec values. - Opens 1 code blocks*

Duplicates the top exec `n` times where `n` is from the int stack.

exec_swap
=========
*Takes: [exec, exec] - Produces: [exec, exec] - Opens 2 code blocks*

Swaps the top two execs.

exec_rot
========
*Takes: [exec, exec, exec] - Produces: [exec, exec, exec] - Opens 3 code blocks*

Rotates the top three execs.

exec_flush
==========
*Takes: PushState - Produces: PushState*

Empties the exec stack.

exec_eq
=======
*Takes: [exec, exec] - Produces: [bool]*

Pushes True if the top two exec are equal. Otherwise pushes False.

exec_stack_depth
================
*Takes: PushState - Produces: [int]*

Pushes the size of the exec stack to the int stack.

exec_yank
=========
*Takes: PushState - Produces: PushState*

Yanks a exec from deep in the stack based on an index from the int stack and puts it on top.

exec_yank_dup
=============
*Takes: PushState - Produces: PushState*

Yanks a copy of a exec deep in the stack based on an index from the int stack and puts it on top.

exec_shove
==========
*Takes: PushState - Produces: PushState - Opens 1 code blocks*

Shoves the top exec deep in the stack based on an index from the int stack.

exec_shove_dup
==============
*Takes: PushState - Produces: PushState - Opens 1 code blocks*

Shoves a copy of the top exec deep in the stack based on an index from the int stack.

exec_is_empty
=============
*Takes: PushState - Produces: [bool]*

Pushes True if the exec stack is empty. Pushes False otherwise.

code_from_bool
==============
*Takes: [bool] - Produces: [code]*

Moves the top bool to the code stack.

code_from_int
=============
*Takes: [int] - Produces: [code]*

Moves the top int to the code stack.

code_from_char
==============
*Takes: [char] - Produces: [code]*

Moves the top char to the code stack.

code_from_float
===============
*Takes: [float] - Produces: [code]*

Moves the top float to the code stack.

code_from_str
=============
*Takes: [str] - Produces: [code]*

Moves the top str to the code stack.

code_from_exec
==============
*Takes: [exec] - Produces: [code] - Opens 1 code blocks*

Moves the top exec to the code stack.

