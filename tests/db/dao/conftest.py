import pytest


class _SessionContextManager:
    def __init__(self, session):
        self._session = session

    async def __aenter__(self):
        return self._session

    async def __aexit__(self, exc_type, exc, tb):
        return False


@pytest.fixture
def fake_session(mocker):
    session = mocker.MagicMock()
    session.execute = mocker.AsyncMock()
    session.commit = mocker.AsyncMock()
    session.rollback = mocker.AsyncMock()
    session.close = mocker.AsyncMock()
    session.add = mocker.MagicMock()
    session.add_all = mocker.MagicMock()
    return session


@pytest.fixture(autouse=True)
def _patch_async_session_maker(monkeypatch, fake_session):
    def _maker():
        return _SessionContextManager(fake_session)

    monkeypatch.setattr('app.db.session.async_session_maker', _maker)
