# Errors

```
Traceback (most recent call last):
  File "/home/erp12/pyshgp/examples/software/replace_space_with_newline.py", line 99, in <module>
    evo.fit(error_function, 1, ['_integer'])
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/pyshgp/gp/evolvers.py", line 173, in fit
    self.print_monitor(g)
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/pyshgp/gp/base.py", line 223, in print_monitor
    '| Lowest Error:', self.population.lowest_error(),
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/pyshgp/gp/population.py", line 294, in lowest_error
    return np.min(np.fromiter(gnrtr, np.float))
OverflowError: int too large to convert to float
```


```
Traceback (most recent call last):
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/multiprocess/pool.py", line 119, in worker
    result = (True, func(*args, **kwds))
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/multiprocess/pool.py", line 44, in mapstar
    return list(map(*args))
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/pathos/helpers/mp_helper.py", line 15, in <lambda>
    func = lambda args: f(*args)
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/pyshgp/gp/population.py", line 163, in f
    return evaluate_with_function(i, error_function)
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/pyshgp/gp/evaluate.py", line 18, in evaluate_with_function
    errs = error_function(individual.program)
  File "/home/erp12/pyshgp/examples/software/double_letters.py", line 42, in error_function
    interpreter.run(program, [case[0]], [], debug)
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/pyshgp/push/interpreter.py", line 236, in run
    self.eval_push(print_steps)
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/pyshgp/push/interpreter.py", line 205, in eval_push
    self.eval_atom(top_exec)
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/pyshgp/push/interpreter.py", line 161, in eval_atom
    instruction.execute(self.state)
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/pyshgp/push/instruction.py", line 50, in execute
    self.func(state)
  File "/home/erp12/anaconda3/lib/python3.5/site-packages/pyshgp/push/instructions/numbers.py", line 449, in integer_from_float
    new_int = int(state['_float'].ref(0))
ValueError: cannot convert float NaN to integer
```
