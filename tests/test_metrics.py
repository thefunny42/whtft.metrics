import pytest

from whtft.metrics import Metrics


@pytest.mark.asyncio
async def test_measure_async_inc(mocker):
    patch = mocker.patch("prometheus_client.metrics.Counter.inc")

    metrics = Metrics("test")

    @metrics.measure()
    async def my_async_function(fail=False):
        "My great function"
        if fail:
            raise ValueError()

    await my_async_function(fail=False)

    patch.assert_called()
    patch.reset_mock()

    with pytest.raises(ValueError):
        await my_async_function(fail=True)

    patch.assert_called()


def test_measure_inc(mocker):
    patch = mocker.patch("prometheus_client.metrics.Counter.inc")

    metrics = Metrics("test")

    @metrics.measure()
    def my_function(fail=False):
        "My great function"
        if fail:
            raise ValueError()

    my_function(fail=False)

    patch.assert_called()
    patch.reset_mock()

    with pytest.raises(ValueError):
        my_function(fail=True)

    patch.assert_called()


def test_app():
    metrics = Metrics("test")

    assert metrics.app is not None
