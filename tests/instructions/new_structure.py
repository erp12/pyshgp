

common_tests = [
    [
        {'_integer': [1, 2, 3]},
        {'_integer': [1, 2]},
        '_integer_pop'
    ],
    [
        {'_boolean': [True]},
        {'_boolean': []},
        '_boolean_pop'
    ],
    [
        {'_string': ['A']}
        {'_string': ['A', 'A']}
        '_boolean_pop'
    ],
    [
        {'_float': [1.5, 2.3]}
        {'_float': [2.3, 1.5]}
        '_float_swap'
    ],
    [
        {'_integer': [1, 2, 3]}
        {'_integer': [2, 3, 1]}
        '_integer_rot'
    ]
]

for test in common_tests:
    assert t_u.run_test(*test)
