from functools import wraps
from typing import *

T = TypeVar("T")


class NonTrueAwaitable(Generic[T]):
    """
    Awaitable object which will evaluate as non-true (for example in if
    statements) until it is awaited, at which point it returns the value that
    awaiting inner returns.
    """

    def __init__(self, inner: Awaitable[T]):
        self.inner = inner

    def __bool__(self) -> bool:
        return False

    def __await__(self):
        val = yield from self.inner.__await__()
        return val


def nta(coro_func: Callable[..., Awaitable[T]]) -> Callable[..., NonTrueAwaitable[T]]:

    @wraps(coro_func)
    def wrapper(*args, **kwargs) -> NonTrueAwaitable[T]:
        return NonTrueAwaitable(coro_func(*args, **kwargs))

    return wrapper
