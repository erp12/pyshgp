import pytest
import numpy as np

from pyshgp.push.types import PushInt, PushStr, push_type_of, push_type_for_type


def test_push_type_of_python_int():
    assert push_type_of(5) == PushInt


def test_push_type_of_numpy_int():
    assert push_type_of(np.int64(5)) == PushInt


def test_push_type_of_python_str():
    assert push_type_of("Hello") == PushStr


def test_push_type_for_type_python_int():
    assert push_type_for_type(int) == PushInt


def test_push_type_for_type_numpy_int():
    assert push_type_for_type(np.int64) == PushInt


def test_push_type_for_type_python_str():
    assert push_type_for_type(str) == PushStr


def test_push_type_for_type_numpy_str():
    assert push_type_for_type(np.str_) == PushStr
