# _*_ coding: utf_8 _*_
"""
@author: Eddie

This examples performs the famous, yet simple, classification of iris species
based on measurements of 150 iris flowers. This example is intended to
demonstrate the use of class voting instructions in classification problems.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

from pyshgp.push.interpreter import PushInterpreter
from pyshgp.gp.base import SimplePushGPEvolver, CLASSIFICATION_ATOM_GENERATORS


iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target,
                                                    test_size=0.3)


def iris_error_func(program):
    error_vec = []
    for i in range(X_train.shape[0]):
        interpreter = PushInterpreter(X_train[i])
        outputs = interpreter.run_push(program)
        keys = [k for k in outputs.keys() if str(k[:6]) == 'class-']
        if len(keys) == 0:
            error_vec.append(1000000)
        else:
            y_hat_s = max(keys, key=(lambda key: outputs[key]))
            y_hat = int(y_hat_s[6:])
            y_true = y_train[i]
            error_vec.append(abs(y_hat - y_true))
    return error_vec


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=2,
                              atom_generators=CLASSIFICATION_ATOM_GENERATORS,
                              max_generations=50, population_size=300)
    evo.fit(iris_error_func, 4, {'class-0' : 0,
                                 'class-1' : 0,
                                 'class-2' : 0})
