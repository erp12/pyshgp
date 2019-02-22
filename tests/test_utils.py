import pytest
from pyshgp.utils import instantiate_using


class Pair:

    def __init__(self, a, b):
        self.a = a
        self.b = b


class ThisMaybeThat:

    def __init__(self, this, that="default"):
        self.this = this
        self.that = that


def test_instantiate_using_exact():
    args = {
        "a": 1,
        "b": 2
    }
    p = instantiate_using(Pair, args)
    assert p.a == 1
    assert p.b == 2


def test_instantiate_using_extra():
    args = {
        "a": 1,
        "b": 2,
        "c": 3
    }
    p = instantiate_using(Pair, args)
    assert p.a == 1
    assert p.b == 2


def test_instantiate_using_insufficient():
    args = {
        "b": 2
    }
    with pytest.raises(TypeError):
        p = instantiate_using(Pair, args)


def test_instantiate_using_optional():
    args = {
        "this": True
    }
    tmt = instantiate_using(ThisMaybeThat, args)
    assert tmt.this
    assert tmt.that == "default"
