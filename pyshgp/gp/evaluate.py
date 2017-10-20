"""
TODO: Write module docstring
"""
import numpy as np
from sklearn.metrics import mean_squared_error, accuracy_score


def evaluate_with_function(individual, error_function, max_error=1e10):
    """Evaluates the individual by passing it's program to the error
    function. Sets the ``error_vec`` and ``total_error`` attributes.

    Parameters
    ----------
    error_function : function
        The error function which takes a push program as input and Returns
        an error vector.
    """
    errs = error_function(individual.program)
    individual.error_vector = errs
    try:
        individual.total_error = sum(individual.error_vector)
    except OverflowError as e:
        individual.total_error = max_error
    return individual


def evaluate_for_regression(individual, X, y, penalty=1e5):
    """Evaluates the given individual on the given dataset.

    Parameters
    ----------
    individual : Individual
        Individual to evaluate.

    X : {array-like, sparse matrix}, shape = (n_samples, n_features)
        Samples.

    y : {array-like, sparse matrix}, shape = (n_samples, 1)
        Target values.
    """
    preds = []
    error_vec = []
    for i in range(X.shape[0]):
        y_hat = individual.run_program(X[i], ['_float'])[0]
        preds.append(y_hat)
        if y_hat is None:
            error_vec.append(penalty)
        else:
            error_vec.append(abs(float(y_hat) - y[i]))
    individual.error_vector = error_vec
    p = [i if i is not None else (-1 * penalty) for i in preds]
    individual.total_error = mean_squared_error(y, p)
    return individual


def evaluate_for_classification(individual, X, y, penalty=1e5):
    """Evaluates the given individual on the given dataset.

    Parameters
    ----------
    individual : Individual
        Individual to evaluate.

    X : {array-like, sparse matrix}, shape = (n_samples, n_features)
        Samples.

    y : {array-like, sparse matrix}, shape = (n_samples, 1)
        Target values.
    """
    n_classes = len(np.unique(y))
    preds = []
    error_vec = []
    for i in range(X.shape[0]):
        output_vector = individual.run_program(X[i], ['_float']*n_classes)
        not_none = [x for x in output_vector if x is not None]
        if len(not_none) == 0:
            preds.append(None)
            error_vec.append(penalty)
        else:
            y_hat = output_vector.index(max(not_none))
            preds.append(y_hat)
            error_vec.append(int(y_hat != y[i]))
    individual.error_vector = error_vec
    p = [i if i is not None else (-1 * penalty) for i in preds]
    individual.total_error = 1 - accuracy_score(y, p)
    return individual
