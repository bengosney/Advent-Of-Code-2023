# Standard Library
from collections.abc import Callable, Iterable
from functools import wraps
from typing import TypeVar

# Third Party
import pytest


def no_input_skip(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except FileNotFoundError:
            pytest.skip("Input file not found")

    return wrapper


T = TypeVar("T")


def collect_and(function: Callable[[Iterable[T]], T]):
    def decorator_collect_and(func):
        @wraps(func)
        def wrapper_collect_and(*args, **kwargs):
            return function(func(*args, **kwargs))

        return wrapper_collect_and

    return decorator_collect_and
