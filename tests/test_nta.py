import pytest

import nta

pytestmark = [pytest.mark.asyncio, pytest.mark.usefixtures("debug")]


@pytest.fixture(params=[True, False])
def debug(event_loop, request):
    original = event_loop.get_debug()
    try:
        event_loop.set_debug(request.param)
        yield

    finally:
        event_loop.set_debug(original)


async def test_class():

    async def inner():
        return 42

    def intermediary():
        return nta.NonTrueAwaitable(inner())

    coro = intermediary()
    assert not coro
    assert await coro == 42


async def test_decorator():

    @nta.nta
    async def func():
        return 42

    coro = func()
    assert not coro
    assert await coro == 42
