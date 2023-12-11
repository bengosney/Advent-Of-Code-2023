# Standard Library
from collections.abc import Callable
from typing import Any, Generic, TypeVar

K = TypeVar("K")
T = TypeVar("T")


class CachingDict(dict[K, T], Generic[K, T]):
    cache_factory: Callable[[Any], T]

    def __init__(self, cache_factory: Callable[[Any], T]) -> None:
        self.cache_factory = cache_factory
        return super().__init__()

    def __missing__(self, __key: K) -> T:
        dict.__setitem__(self, __key, self.cache_factory(__key))
        return self[__key]


def test_caching_dict():
    test_dict = CachingDict[str, str](lambda key: f"{key}-{key}")
    assert test_dict["test"] == "test-test"
