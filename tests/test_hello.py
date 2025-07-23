import pytest

from src.swe_bench_v2.hello import hello_fn, a_hello_fn


def test_hello():
    hello = hello_fn()
    assert hello.name == "Wei"
    assert hello.content == "Hello, World!"


@pytest.mark.asyncio
async def test_a_hello():
    hello = await a_hello_fn()
    assert hello.name == "Wei"
    assert hello.content == "Hello, World!"
