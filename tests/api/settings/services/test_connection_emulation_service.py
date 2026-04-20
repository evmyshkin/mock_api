from typing import cast

import pytest

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.settings.services.connection_emulation_service import ConnectionEmulationService


class _FakeSession:
    def __init__(self, in_transaction: bool) -> None:
        self._in_transaction = in_transaction
        self.rollback_called = False

    def in_transaction(self) -> bool:
        return self._in_transaction

    async def rollback(self) -> None:
        self.rollback_called = True


@pytest.mark.asyncio
async def test_apply_connection_settings_rolls_back_before_delay(mocker) -> None:
    sleep_mock = mocker.patch(
        'app.api.settings.services.connection_emulation_service.asyncio.sleep',
        new=mocker.AsyncMock(),
    )
    session = _FakeSession(in_transaction=True)
    response = Response()

    await ConnectionEmulationService.apply_connection_settings(
        response_delay=2,
        response_code=202,
        res_obj=response,
        db_session=cast(AsyncSession, cast(object, session)),
    )

    assert session.rollback_called is True
    sleep_mock.assert_awaited_once_with(2)
    assert response.status_code == 202


@pytest.mark.asyncio
async def test_apply_connection_settings_skips_rollback_without_transaction(mocker) -> None:
    sleep_mock = mocker.patch(
        'app.api.settings.services.connection_emulation_service.asyncio.sleep',
        new=mocker.AsyncMock(),
    )
    session = _FakeSession(in_transaction=False)
    response = Response()

    await ConnectionEmulationService.apply_connection_settings(
        response_delay=1,
        response_code=204,
        res_obj=response,
        db_session=cast(AsyncSession, cast(object, session)),
    )

    assert session.rollback_called is False
    sleep_mock.assert_awaited_once_with(1)
    assert response.status_code == 204
