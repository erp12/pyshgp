import pytest
import numpy as np

from pyshgp.push.types import PushType, PushInt, PushStr, Char
from pyshgp.validation import PushError


class TestPushType:

    def test_is_instance(self, core_type_lib):
        assert PushInt.is_instance(5)
        assert PushInt.is_instance(np.int64(100))
        assert not PushInt.is_instance("Foo")
        assert not PushInt.is_instance(np.str_("Bar"))

        assert not PushStr.is_instance(5)
        assert not PushStr.is_instance(np.int64(100))
        assert PushStr.is_instance("Foo")
        assert PushStr.is_instance(np.str_("Bar"))

    def test_default_coerce(self, core_type_lib):
        assert PushInt.coerce(5) == 5
        assert PushInt.coerce(np.int64(100)) == 100
        assert PushInt.coerce("123") == 123
        assert PushInt.coerce(5.1) == 5

    def test_custom_coerce(self, point_cls, to_point_func):
        PushPoint = PushType("point", (point_cls, ), coercion_func=to_point_func)
        assert PushPoint.coerce([1, 2, 3]) == point_cls(1.0, 2.0)
        assert PushPoint.coerce(("1.2", "3.4")) == point_cls(1.2, 3.4)


class TestChar:

    def test_empty_char(self):
        with pytest.raises(PushError):
            Char("")

    def test_long_char(self):
        with pytest.raises(PushError):
            Char("abc")
