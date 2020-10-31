import os
import pickle

from collections.abc import Mapping
from copy import copy
from sys import getsizeof
from tempfile import NamedTemporaryFile
from typing import TypeVar

from pytest import raises

from samplesheet import CaselessDict
from samplesheet import FrozenDict

T = TypeVar("T")


def round_trip_pickle(obj: T) -> T:
    temp = NamedTemporaryFile("w", delete=False)
    with open(temp.name, "wb") as handle:
        pickle.dump(obj, handle)
    with open(temp.name, "rb") as handle:
        rehydrated = pickle.load(handle)
    os.remove(temp.name)
    return rehydrated


class TestCaselessDict(object):
    def test_isinstance(self):
        assert isinstance(FrozenDict(), Mapping)

    def test_accepts_type_params(self):
        FrozenDict[int, int]({1: 1})

    def test__setitem__(self):
        with raises(TypeError):
            exec("CaselessDict()[1] = 2")

    def test__delitem__(self):
        with raises(TypeError):
            exec("del CaselessDict({1: 2})[1]")

    def test_pop(self):
        with raises(AttributeError):
            exec("CaselessDict({1: 2}).pop(1)")

    def test_popitem(self):
        with raises(AttributeError):
            exec("CaselessDict({1: 2}).popitem()")

    def test_clear(self):
        with raises(AttributeError):
            exec("CaselessDict({1: 2}).clear()")

    def test_update(self):
        with raises(AttributeError):
            exec("CaselessDict({1: 2}).update(1, 3)")

    def test_setdefault(self):
        with raises(AttributeError):
            exec("CaselessDict({1: 2}).setdefault(1)")

    def test__contains__(self):
        assert "key" in CaselessDict({"key": "value"})
        assert "key" in CaselessDict(key="value")
        assert "key" in CaselessDict(KEY="value")  # Case invariant
        assert "keY" in CaselessDict(KEY="value")  # Case invariant
        assert "KeY" in CaselessDict(KEY="value")  # Case invariant
        assert "key" in CaselessDict({"KEY": "value"})
        assert "key" not in CaselessDict()

        assert 2 in CaselessDict({2: "value"})
        assert 2 not in CaselessDict()

    def test__copy__(self):
        mapping = CaselessDict({2: 3, 4: 5, "lower": "UPPER"})
        assert mapping == copy(mapping)
        assert mapping.get(2) == copy(mapping).get(2)
        assert mapping.get(4) == copy(mapping).get(4)
        assert mapping.get(5) == copy(mapping).get(5)
        assert mapping.get("LOWER") == copy(mapping).get("lower")

    def test__eq__(self):
        CaselessDict({1: 2}) == CaselessDict({1: 2})
        CaselessDict({1: 2}) != CaselessDict({3: 4})
        CaselessDict({1: 2, "lower": "UPPER"}) != CaselessDict({3: 4, "LOWER": "UPPER"})

    def test__getitem__(self):
        assert CaselessDict({1: 2})[1] == 2
        assert CaselessDict({1: 2, "lower": "UPPER"})["LOWER"] == "UPPER"
        with raises(KeyError):
            CaselessDict()[1]

    def test__hash__(self):
        assert hash(CaselessDict()) == hash(CaselessDict())
        assert hash(CaselessDict({1: 2})) != hash(CaselessDict())
        assert hash(CaselessDict({"lower": "UPPER"})) == hash(CaselessDict({"lower": "UPPER"}))
        assert hash(CaselessDict({"lower": "UPPER"})) == hash(CaselessDict({"LOWER": "UPPER"}))

    def test__iter__(self):
        keyvalues = [(1, 2), (3, 4)]
        mapping = CaselessDict(keyvalues)
        for (actual_key, expected_key) in zip(mapping, dict(keyvalues).keys()):
            assert actual_key == expected_key

    def test__len__(self):
        assert len(CaselessDict()) == 0
        assert len(CaselessDict({1: 2})) == 1
        assert len(CaselessDict({1: 2, 3: 4})) == 2

    def test__nonzero__(self):
        assert not bool(CaselessDict())
        assert bool(CaselessDict({1: 2}))
        assert bool(CaselessDict({1: 2, 3: 4}))

    def test__reduce__(self):
        mapping = CaselessDict({1: 2, 3: 4, "hello": "hi"})
        assert round_trip_pickle(mapping) == mapping

    def test__repr__(self):
        assert repr(CaselessDict()) == "CaselessDict({})"
        assert repr(CaselessDict({1: 2})) == "CaselessDict({1: 2})"
        assert repr(CaselessDict({1: 2, 3: 4})) == "CaselessDict({1: 2, 3: 4})"

    def test__sizeof__(self):
        assert getsizeof(CaselessDict()) <= getsizeof(CaselessDict({1: 2, 3: 4}))

    def test__str__(self):
        assert str(CaselessDict()) == "CaselessDict({})"
        assert str(CaselessDict({1: 2})) == "CaselessDict({1: 2})"
        assert str(CaselessDict({1: 2, 3: 4})) == "CaselessDict({1: 2, 3: 4})"

    def test_fromkeys(self):
        assert CaselessDict.fromkeys([1, 2, 3], default=3) == CaselessDict({1: 3, 2: 3, 3: 3})
        assert CaselessDict.fromkeys([1, 2, 3], default=None) == CaselessDict(
            {1: None, 2: None, 3: None}
        )

    def test_copy(self):
        mapping = CaselessDict({2: 3, 4: 5, "lower": "UPPER"})
        assert mapping == mapping.copy()
        updated = CaselessDict({2: 3, 4: 10, "lower": "UPPER"})
        assert updated == mapping.copy({4: 10})
        updated = CaselessDict({2: 3, 4: 5, 6: 7, "lower": "UPPER"})
        assert updated == mapping.copy({6: 7})
        updated = CaselessDict({2: 3, 4: 5, 6: 7, 8: 9, "lower": "UPPER"})
        assert updated == mapping.copy({6: 7, 8: 9})
        updated = CaselessDict({2: 3, 4: 5, 6: 7, 8: 9, "lower": "UPDATED"})
        assert updated == mapping.copy({6: 7, 8: 9, "LOWER": "UPDATED"})

    def test_get(self):
        assert CaselessDict({1: 2}).get(1) == 2
        assert CaselessDict().get(1) == None
        assert CaselessDict().get(1, default=2) == 2
        assert CaselessDict({"lower": "UPPER"}).get("LOWER") == "UPPER"

    def test_items(self):
        keyvalues = [(1, 2), (3, 4)]
        assert list(CaselessDict(keyvalues).items()) == keyvalues

    def test_keys(self):
        keyvalues = [(1, 2), (3, 4)]
        assert list(CaselessDict(keyvalues).keys()) == list(dict(keyvalues).keys())

    def test_updated(self):
        mapping = CaselessDict({2: 3, 4: 5, "lower": "UPPER"})
        assert mapping.updated(4, 10) == CaselessDict({2: 3, 4: 10, "lower": "UPPER"})
        assert mapping.updated(6, 7) == CaselessDict({2: 3, 4: 5, 6: 7, "lower": "UPPER"})
        assert mapping.updated("LOWER", "UPDATED") == CaselessDict(
            {2: 3, 4: 5, "lower": "UPDATED"}
        )

    def test_values(self):
        keyvalues = [(1, 2), (3, 4)]
        assert list(CaselessDict(keyvalues).values()) == list(dict(keyvalues).values())


class TestFrozenDict(object):
    def test_isinstance(self):
        assert isinstance(FrozenDict(), Mapping)

    def test_accepts_type_params(self):
        FrozenDict[int, int]({1: 1})

    def test__setitem__(self):
        with raises(TypeError):
            exec("FrozenDict()[1] = 2")

    def test__delitem__(self):
        with raises(TypeError):
            exec("del FrozenDict({1: 2})[1]")

    def test_pop(self):
        with raises(AttributeError):
            exec("FrozenDict({1: 2}).pop(1)")

    def test_popitem(self):
        with raises(AttributeError):
            exec("FrozenDict({1: 2}).popitem()")

    def test_clear(self):
        with raises(AttributeError):
            exec("FrozenDict({1: 2}).clear()")

    def test_update(self):
        with raises(AttributeError):
            exec("FrozenDict({1: 2}).update(1, 3)")

    def test_setdefault(self):
        with raises(AttributeError):
            exec("FrozenDict({1: 2}).setdefault(1)")

    def test__contains__(self):
        assert "key" in FrozenDict({"key": "value"})
        assert "key" in FrozenDict(key="value")
        assert "key" not in FrozenDict()
        assert "key" not in FrozenDict({"KEY": "value"})
        assert "key" not in FrozenDict(KEY="value")

        assert 2 in FrozenDict({2: "value"})
        assert 2 not in FrozenDict()

    def test__copy__(self):
        mapping = FrozenDict({2: 3, 4: 5})
        assert mapping == copy(mapping)
        assert mapping.get(2) == copy(mapping).get(2)
        assert mapping.get(4) == copy(mapping).get(4)
        assert mapping.get(5) == copy(mapping).get(5)

    def test__eq__(self):
        FrozenDict({1: 2}) == FrozenDict({1: 2})
        FrozenDict({1: 2}) != FrozenDict({3: 4})

    def test__getitem__(self):
        assert FrozenDict({1: 2})[1] == 2
        with raises(KeyError):
            FrozenDict()[1]

    def test__hash__(self):
        assert hash(FrozenDict()) == hash(FrozenDict())
        assert hash(FrozenDict({1: 2})) != hash(FrozenDict())

    def test__iter__(self):
        keyvalues = [(1, 2), (3, 4)]
        mapping = FrozenDict(keyvalues)
        for (actual_key, expected_key) in zip(mapping, dict(keyvalues).keys()):
            assert actual_key == expected_key

    def test__len__(self):
        assert len(FrozenDict()) == 0
        assert len(FrozenDict({1: 2})) == 1
        assert len(FrozenDict({1: 2, 3: 4})) == 2

    def test__nonzero__(self):
        assert not bool(FrozenDict())
        assert bool(FrozenDict({1: 2}))
        assert bool(FrozenDict({1: 2, 3: 4}))

    def test__reduce__(self):
        mapping = FrozenDict({1: 2, 3: 4, "hello": "hi"})
        assert round_trip_pickle(mapping) == mapping

    def test__repr__(self):
        assert repr(FrozenDict()) == "FrozenDict({})"
        assert repr(FrozenDict({1: 2})) == "FrozenDict({1: 2})"
        assert repr(FrozenDict({1: 2, 3: 4})) == "FrozenDict({1: 2, 3: 4})"

    def test__sizeof__(self):
        assert getsizeof(FrozenDict()) <= getsizeof(FrozenDict({1: 2, 3: 4}))

    def test__str__(self):
        assert str(FrozenDict()) == "FrozenDict({})"
        assert str(FrozenDict({1: 2})) == "FrozenDict({1: 2})"
        assert str(FrozenDict({1: 2, 3: 4})) == "FrozenDict({1: 2, 3: 4})"

    def test_fromkeys(self):
        assert FrozenDict.fromkeys([1, 2, 3], default=3) == FrozenDict({1: 3, 2: 3, 3: 3})
        assert FrozenDict.fromkeys([1, 2, 3], default=None) == FrozenDict(
            {1: None, 2: None, 3: None}
        )

    def test_copy(self):
        mapping = FrozenDict({2: 3, 4: 5})
        assert mapping == mapping.copy()
        updated = FrozenDict({2: 3, 4: 10})
        assert updated == mapping.copy({4: 10})
        updated = FrozenDict({2: 3, 4: 5, 6: 7})
        assert updated == mapping.copy({6: 7})
        updated = FrozenDict({2: 3, 4: 5, 6: 7, 8: 9})
        assert updated == mapping.copy({6: 7, 8: 9})

    def test_get(self):
        assert FrozenDict({1: 2}).get(1) == 2
        assert FrozenDict().get(1) == None
        assert FrozenDict().get(1, default=2) == 2

    def test_items(self):
        keyvalues = [(1, 2), (3, 4)]
        assert list(FrozenDict(keyvalues).items()) == keyvalues

    def test_keys(self):
        keyvalues = [(1, 2), (3, 4)]
        assert list(FrozenDict(keyvalues).keys()) == list(dict(keyvalues).keys())

    def test_updated(self):
        mapping = FrozenDict({2: 3, 4: 5})
        assert mapping.updated(4, 10) == FrozenDict({2: 3, 4: 10})
        assert mapping.updated(6, 7) == FrozenDict({2: 3, 4: 5, 6: 7})

    def test_values(self):
        keyvalues = [(1, 2), (3, 4)]
        assert list(FrozenDict(keyvalues).values()) == list(dict(keyvalues).values())
