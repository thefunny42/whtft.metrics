from whtft.metrics import Metrics
import pytest


@pytest.mark.asyncio
async def test_measure_inc(mocker):
    patch = mocker.patch("prometheus_client.metrics.Counter.inc")

    metrics = Metrics("test")

    @metrics.measure()
    async def my_function(fail=False):
        "My great function"
        if fail:
            raise ValueError()

    await my_function(fail=False)

    patch.assert_called()
    patch.reset_mock()

    with pytest.raises(ValueError):
        await my_function(fail=True)

    patch.assert_called()


def test_app():
    metrics = Metrics("test")

    assert metrics.app is not None
