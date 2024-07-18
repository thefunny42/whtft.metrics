import asyncio
from functools import wraps

import prometheus_client

__version__ = "0.1.0"


class Metrics:

    def __init__(self, prefix: str):
        self.prefix = prefix

    @property
    def app(self):
        return prometheus_client.make_asgi_app()

    def new(self, name: str, doc: str | None):
        doc = doc or name
        success = prometheus_client.Counter(f"{self.prefix}_{name}", f"{doc}")
        failure = prometheus_client.Counter(
            f"{self.prefix}_{name}_failures", f"{doc} failures"
        )
        return (success, failure)

    def measure(self, name: str | None = None, doc: str | None = None):

        def decorator(func):

            success, failure = self.new(
                name=name or func.__name__,
                doc=doc or func.__doc__,
            )

            if asyncio.iscoroutinefunction(func):

                @wraps(func)
                async def wrapper_async(*args, **kwargs):
                    try:
                        result = await func(*args, **kwargs)
                    except Exception as error:
                        failure.inc()
                        raise error
                    else:
                        success.inc()
                        return result

                return wrapper_async

            else:

                @wraps(func)
                def wrapper(*args, **kwargs):
                    try:
                        result = func(*args, **kwargs)
                    except Exception as error:
                        failure.inc()
                        raise error
                    else:
                        success.inc()
                        return result

                return wrapper

        return decorator
