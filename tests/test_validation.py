import pytest
import numpy as np

from pyshgp.validation import check_1d, check_2d, check_column_types, check_num_columns


def test_check_1d_on_1d():
    assert check_1d([1, 2, 3]) == [1, 2, 3]


def test_check_1d_on_dirty_1d():
    assert check_1d([1, np.array(2), 3]) == [1, 2, 3]


def test_check_1d_on_2d():
    with pytest.raises(ValueError):
        check_1d(np.arange(10).reshape(-1, 2))


def test_check_2d_on_1d():
    with pytest.raises(ValueError):
        check_2d(np.arange(3))


def test_check_2d_on_2d():
    assert np.array_equal(check_2d(np.arange(10).reshape(-1, 2)), np.arange(10).reshape(-1, 2))


def test_check_2d_on_3d():
    with pytest.raises(ValueError):
        check_2d(np.arange(12).reshape(-1, 2, 2))


def test_check_column_types_on_int_ndarray():
    assert check_column_types(np.arange(30).reshape(-1, 3)) == [np.int64, np.int64, np.int64]


def test_check_column_types_on_nested_list():
    mock_dataset = [
        [1, "a"],
        [2, "b"],
        [3, "c"]
    ]
    assert check_column_types(mock_dataset, 1.0) == [int, str]


def test_check_column_types_on_bad_dataset():
    mock_dataset = [
        [1, "a"],
        [2, False],
        [3, "c"]
    ]
    with pytest.raises(ValueError):
        check_column_types(mock_dataset, 1.0)


def test_check_num_columns_a():
    mock_dataset = [
        [1, "a"],
        [2, "b"],
        [3, "c"]
    ]
    assert check_num_columns(mock_dataset) == 2


def test_check_num_columns_b():
    mock_dataset = np.arange(9).reshape(-1, 3)
    assert check_num_columns(mock_dataset) == 3