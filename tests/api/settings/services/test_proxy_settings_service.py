from types import SimpleNamespace

import pytest

from fastapi import HTTPException

from app.api.settings.endpoint_types_enum import ProxyEndpointTypesEnum
from app.api.settings.schemas.requests.base_settings_request_schema import BaseSettingsUpdateRequestSchema
from app.api.settings.services.proxy_settings_service import ProxySettingsService


@pytest.mark.asyncio
class TestProxySettingsService:
    async def test_get_settings_returns_validated_response_list(self, mocker):
        session = mocker.Mock()
        proxy_settings_dao = mocker.Mock()
        proxy_settings_dao.find_all_settings = mocker.AsyncMock(
            return_value=[
                SimpleNamespace(
                    id=1,
                    endpoint_type=ProxyEndpointTypesEnum.CAPTURE.value,
                    response_delay=2,
                    response_code=201,
                )
            ]
        )
        service = ProxySettingsService(proxy_settings_dao=proxy_settings_dao, session=session)

        result = await service.get_settings()

        assert len(result) == 1
        assert result[0].model_dump(mode='json') == {
            'id': 1,
            'endpoint_type': ProxyEndpointTypesEnum.CAPTURE.value,
            'response_delay': 2,
            'response_code': 201,
        }
        proxy_settings_dao.find_all_settings.assert_awaited_once_with(session=session)

    async def test_update_proxy_setting_returns_updated_setting(self, mocker):
        session = mocker.Mock()
        proxy_settings_dao = mocker.Mock()
        proxy_settings_dao.update_endpoint_settings = mocker.AsyncMock(
            return_value=SimpleNamespace(
                id=1,
                endpoint_type=ProxyEndpointTypesEnum.CAPTURE.value,
                response_delay=1,
                response_code=204,
            )
        )
        service = ProxySettingsService(proxy_settings_dao=proxy_settings_dao, session=session)
        values = BaseSettingsUpdateRequestSchema(id=1, response_delay=1, response_code=204)

        result = await service.update_proxy_setting(values=values)

        assert result.model_dump(mode='json') == {
            'id': 1,
            'endpoint_type': ProxyEndpointTypesEnum.CAPTURE.value,
            'response_delay': 1,
            'response_code': 204,
        }
        proxy_settings_dao.update_endpoint_settings.assert_awaited_once_with(
            session=session,
            setting_id=1,
            values=values.model_dump(),
        )

    async def test_update_proxy_setting_raises_404_when_setting_not_found(self, mocker):
        session = mocker.Mock()
        proxy_settings_dao = mocker.Mock()
        proxy_settings_dao.update_endpoint_settings = mocker.AsyncMock(return_value=None)
        service = ProxySettingsService(proxy_settings_dao=proxy_settings_dao, session=session)
        values = BaseSettingsUpdateRequestSchema(id=99, response_delay=0, response_code=200)

        with pytest.raises(HTTPException, match='Настройка загрузки товаров не найдена по id') as exc:
            await service.update_proxy_setting(values=values)

        assert exc.value.status_code == 404
