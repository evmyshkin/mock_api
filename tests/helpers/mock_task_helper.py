class DummyTask:
    def __init__(self, *, cancelled: bool = False, done: bool = False, exc=None):
        self._cancelled = cancelled
        self._done = done
        self._exc = exc

    def cancelled(self) -> bool:
        return self._cancelled

    def done(self) -> bool:
        return self._done

    def exception(self):
        return self._exc


def mock_redis_task(*, cancelled: bool = False, done: bool = False, exc=None) -> DummyTask:
    return DummyTask(cancelled=cancelled, done=done, exc=exc)
