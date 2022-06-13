from collections import abc
from typing import AbstractSet
from typing import Any
from typing import ClassVar
from typing import Collection
from typing import Dict
from typing import Generator
from typing import Generic
from typing import Hashable
from typing import ItemsView
from typing import Iterator
from typing import KeysView
from typing import List
from typing import Mapping
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union
from typing import ValuesView
from typing import cast
from sys import getsizeof, maxsize

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
StringType = Union[bytes, str]
NoneInt = Optional[int]
NoneStr = Optional[str]


class CaselessDict(Generic[K, V]):
    """A dictionary with case-insensitive string getters."""

    underlying: ClassVar[Type[Dict]] = dict

    def __init__(
        self, *args: Union[Mapping[K, V], Collection[Tuple[K, V]]], **kwargs: Dict[K, V]
    ) -> None:
        self._map: Dict[K, V] = self.underlying(*args, **kwargs)
        self._caseless: Dict[StringType, StringType] = {
            k.lower(): k for k, v in self._map.items() if isinstance(k, (bytes, str))
        }
        self._hash: int = -1

    def __contains__(self, key: K) -> bool:
        """Test if <key> is contained within this mapping."""
        return (
            self._caseless[key.lower()] in self._map
            if (isinstance(key, (bytes, str)) and key.lower() in self._caseless)
            else key in self._map
        )

    def __copy__(self) -> "CaselessDict":
        """Return a shallow copy of this mapping."""
        return type(self)(self.items())

    def __eq__(self, other: Any) -> bool:
        """Test if <other> is equal to this class instance."""
        return (
            (hash(self) == hash(other)) & (self.items() == other.items())
            if (isinstance(other, type(self)) and hasattr(other, "__hash__"))
            else False
        )

    def __getitem__(self, key: K) -> Any:
        """Return a value indexed with <key>."""
        if isinstance(key, (bytes, str)) and key.lower() in self._caseless:
            return self._map[cast(K, self._caseless[key.lower()])]
        else:
            return self._map[key]

    def __hash__(self) -> int:
        """Return a hash of this dictionary using all key-value pairs."""
        if self._hash == -1 and self:
            current: int = 0
            for (key, value) in self.items():
                if isinstance(key, (bytes, str)):
                    current ^= hash((key.lower(), value))
                else:
                    current ^= hash((key, value))
            current ^= maxsize
            self._hash = current
        return self._hash

    def __iter__(self) -> Iterator[K]:
        """Return an iterator over the keys."""
        return iter(self._map.keys())

    def __len__(self) -> int:
        """Return the length of the mapping."""
        return len(self._map)

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __nonzero__(self) -> bool:
        """Test if this mapping is of non-zero length."""
        return bool(self._map)

    def __reduce__(self) -> Tuple[Type["CaselessDict"], Tuple[List[Tuple[K, V]]]]:
        """Return a recipe for pickling."""
        return (type(self), (list(self.items()),))

    def __repr__(self) -> str:
        """Return a representation of this class instance."""
        return f"{self.__class__.__qualname__}({repr(self._map)})"

    def __sizeof__(self) -> int:
        """Return the size of this class instance."""
        return getsizeof(self._map)

    def __str__(self) -> str:
        """Return a string representation of this class."""
        return self.__repr__()

    @classmethod
    def fromkeys(cls, keys: Collection[K], default: V) -> "CaselessDict":
        """Build a mapping from a set of keys with a default value."""
        return cls([(key, default) for key in keys])

    def copy(self, mapping: Optional[Dict[K, V]] = None) -> "CaselessDict":
        """Return a shallow copy of this mapping."""
        overrides: Dict[K, V] = {}
        if mapping is not None:
            for k, v in mapping.items():
                if isinstance(k, (bytes, str)) and k.lower() in self._caseless:
                    overrides[cast(K, self._caseless[k.lower()])] = v
                else:
                    overrides[k] = v
        return type(self)((list(self.items())) + list(overrides.items()))

    def get(self, key: K, default: Optional[Any] = None) -> Union[Any, V]:
        """Return a value indexed with <key> but if that key is not present, return <default>."""
        if isinstance(key, (bytes, str)) and key.lower() in self._caseless:
            caseless_key: K = cast(K, self._caseless[key.lower()])
            return self._map.get(caseless_key, default)
        else:
            return self._map.get(key, default)

    def items(self) -> ItemsView[K, V]:
        """Return this mapping as a list of paired key-values."""
        return self._map.items()

    def keys(self) -> KeysView[Hashable]:
        """Return the keys in insertion order."""
        return self._map.keys()

    def updated(self, key: K, value: V) -> "CaselessDict":
        """Return a shallow copy of this mapping with an key-value pair."""
        return self.copy({key: value})

    def values(self) -> ValuesView[V]:
        """Return the values in insertion order."""
        return self._map.values()


class FrozenDict(Generic[K, V]):
    """A dictionary without mutator methods."""

    underlying: ClassVar[Type[Dict]] = dict

    def __init__(
        self, *args: Union[Mapping[K, V], Collection[Tuple[K, V]]], **kwargs: Dict[K, V]
    ) -> None:
        self._map: Dict[K, V] = self.underlying(*args, **kwargs)
        self._hash: int = -1

    def __contains__(self, key: K) -> bool:
        """Test if <key> is contained within this mapping."""
        return key in self._map

    def __copy__(self) -> "FrozenDict":
        """Return a shallow copy of this mapping."""
        return type(self)(self.items())

    def __eq__(self, other: Any) -> bool:
        """Test if <other> is equal to this class instance."""
        return (
            (hash(self) == hash(other)) & (self.items() == other.items())
            if (isinstance(other, type(self)) and hasattr(other, "__hash__"))
            else False
        )

    def __getitem__(self, key: K) -> Any:
        """Return a value indexed with <key>."""
        return self._map[key]

    def __hash__(self) -> int:
        """Return a hash of this dictionary using all key-value pairs."""
        if self._hash == -1 and self:
            current: int = 0
            for pair in self.items():
                current ^= hash(pair)
            current ^= maxsize
            self._hash = current
        return self._hash

    def __iter__(self) -> Iterator[K]:
        """Return an iterator over the keys."""
        return iter(self._map.keys())

    def __len__(self) -> int:
        """Return the length of the mapping."""
        return len(self._map)

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __nonzero__(self) -> bool:
        """Test if this mapping is of non-zero length."""
        return bool(self._map)

    def __reduce__(self) -> Tuple[Type["FrozenDict"], Tuple[List[Tuple[K, V]]]]:
        """Return a recipe for pickling."""
        return (type(self), (list(self.items()),))

    def __repr__(self) -> str:
        """Return a representation of this class instance."""
        return f"{self.__class__.__qualname__}({repr(self._map)})"

    def __sizeof__(self) -> int:
        """Return the size of this class instance."""
        return getsizeof(self._map)

    def __str__(self) -> str:
        """Return a string representation of this class."""
        return self.__repr__()

    @classmethod
    def fromkeys(cls, keys: Collection[K], default: V) -> "FrozenDict":
        """Build a mapping from a set of keys with a default value."""
        return cls([(key, default) for key in keys])

    def copy(self, mapping: Optional[Dict[K, V]] = None) -> "FrozenDict":
        """Return a shallow copy of this mapping."""
        if mapping is None:
            return type(self)(list(self.items()))
        else:
            return type(self)((list(self.items())) + list(mapping.items()))

    def get(self, key: K, default: Optional[Any] = None) -> Union[Any, V]:
        """Return a value indexed with <key> but if that key is not present, return <default>."""
        return self._map.get(key, default)

    def items(self) -> ItemsView[K, V]:
        """Return this mapping as a list of paired key-values."""
        return self._map.items()

    def keys(self) -> KeysView[Hashable]:
        """Return the keys in insertion order."""
        return self._map.keys()

    def updated(self, key: K, value: V) -> "FrozenDict":
        """Return a shallow copy of this mapping with an key-value pair."""
        return self.copy({key: value})

    def values(self) -> ValuesView[V]:
        """Return the values in insertion order."""
        return self._map.values()
