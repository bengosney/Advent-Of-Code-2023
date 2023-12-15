# Standard Library
from collections.abc import Callable
from typing import Generic, TypeVar

K = TypeVar("K")
T = TypeVar("T")


class CachingDict(dict[K, T], Generic[K, T]):
    cache_factory: Callable[[K], T]

    def __init__(self, cache_factory: Callable[[K], T]) -> None:
        self.cache_factory = cache_factory
        return super().__init__()

    def __missing__(self, __key: K) -> T:
        self.__setitem__(__key, self.cache_factory(__key))
        return self[__key]


def test_caching_dict():
    test_dict = CachingDict[str, str](lambda key: f"{key}-{key}")
    assert test_dict["test"] == "test-test"
