"""Module for validating data and raising informative errors."""
from typing import Sequence, Tuple
import numpy as np
import pandas as pd


def check_1d(seq: Sequence) -> Sequence:
    """Check given seq is one-dimensional. Raise error if can't be easily transformed."""
    e = ValueError("Too many dimensions.")
    for ndx, el in enumerate(seq):
        if isinstance(el, (list, tuple)):
            if len(el) > 1:
                raise e
            seq[ndx] = el[0]
        elif isinstance(el, (np.ndarray, pd.Series)):
            if el.size > 1:
                raise e
            if isinstance(el, np.ndarray):
                seq[ndx] = el.reshape(1, -1)[0][0]
            else:
                seq[ndx] = el[0]
    return seq


def check_2d(seq: Sequence) -> Sequence:
    """Check given seq is two-dimensional. Raise error if can't be easily transformed."""
    for ndx, el in enumerate(seq):
        if not isinstance(el, (list, tuple, np.ndarray, pd.Series)):
            raise ValueError("Too few dimensions.")
        seq[ndx] = check_1d(el)
    return seq


def check_column_types(seq: Sequence, certainty_proportion: float = 0.2) -> Sequence[type]:
    """Check all elements of each column are of the same type."""
    output_types = None
    for ndx in range(min(int(len(seq) * certainty_proportion) + 1, len(seq) - 1)):
        el = seq[ndx]
        el_types = [type(val) for val in el]
        if output_types is None:
            output_types = el_types
        else:
            if len(output_types) != len(el_types):
                raise ValueError("Found inconsistent number of columns.")
            for i, output_type in enumerate(output_types):
                if output_type != el_types[i]:
                    raise ValueError("Found inconsistent types in column.")
    return output_types


def check_num_columns(seq: Sequence, certainty_proportion: float = 0.2) -> int:
    """Return the number of columns of in the dataset."""
    num_columns = None
    for ndx in range(min(int(len(seq) * certainty_proportion) + 1, len(seq) - 1)):
        el_len = len(list(seq[ndx]))
        if num_columns is None:
            num_columns = el_len
        else:
            if num_columns != el_len:
                raise ValueError("Found inconsistent number of columns.")
    return num_columns


def check_X_y(X, y) -> Tuple[Sequence, Sequence, int, Sequence]:
    """Check the given X and y datasets are prepared to be passed to a PushEstimator.

    Inspired by the scikit-learn function with the same name.
    https://scikit-learn.org/stable/modules/generated/sklearn.utils.check_X_y.html#sklearn.utils.check_X_y

    """
    X = check_2d(X)
    y = check_2d(y)
    X_column_count = check_num_columns(X)
    y_dim_types = check_column_types(y)
    return X, y, X_column_count, y_dim_types


def check_is_fitted(estimator, attribute):
    """Check the given estimator has already been fit.

    Inspired by the scikit-learn function with the same name.
    https://scikit-learn.org/stable/modules/generated/sklearn.utils.validation.check_is_fitted.html#sklearn.utils.validation.check_is_fitted
    """
    if not hasattr(estimator, 'fit'):
        raise TypeError("{e} is not an estimator.".format(e=estimator))

    if not hasattr(estimator, attribute):
        raise ValueError(
            "Estimator has not been fit yet. Call 'fit' with appropriate arguments before using this method."
        )


class PushError(Exception):
    """Error raised during Push program execution."""

    @classmethod
    def no_type(cls, thing):
        """Raise PushError when no PushType can be found for something."""
        return cls("Unkown PushType for {th}.".format(th=thing))

    @classmethod
    def failed_coerce(cls, thing, push_type):
        """Raise PushError when something fails to coerce to a PushType."""
        return cls("Could not convert {typ1} {th} to {typ2}.".format(
            th=thing,
            typ1=type(thing),
            typ2=push_type
        ))

    @classmethod
    def empty_character(cls):
        """Raise PushError when Character is made from empty string."""
        return cls("Character object cannot be created from empty string.")

    @classmethod
    def long_character(cls):
        """Raise PushError when Character is made from string length more than 1."""
        return cls("Character object cannot be created from string of length > 1.")
