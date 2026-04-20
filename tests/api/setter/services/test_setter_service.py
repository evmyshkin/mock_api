import pytest

from fastapi import Response

from app.api.setter.enums import SetterEntityTypeEnum
from app.api.setter.services.setter_service import SetterService
from app.api.settings.endpoint_types_enum import SetterEndpointTypesEnum


@pytest.mark.asyncio
class TestSetterService:
    async def test_get_data_applies_connection_settings(self, mocker):
        setter_request_dao = mocker.Mock()
        setter_request_dao.find_entity_payloads = mocker.AsyncMock(return_value=[{'id': '1'}])

        settings = mocker.Mock(response_delay=2, response_code=202)
        setter_settings_dao = mocker.Mock()
        setter_settings_dao.get_endpoint_settings = mocker.AsyncMock(return_value=settings)

        apply_connection_settings_mock = mocker.patch(
            'app.api.setter.services.setter_service.ConnectionEmulationService.apply_connection_settings',
            new=mocker.AsyncMock(),
        )

        session = mocker.Mock()
        response = Response()
        service = SetterService(
            setter_request_dao=setter_request_dao,
            setter_settings_dao=setter_settings_dao,
            session=session,
        )

        result = await service.get_data(entity_type=SetterEntityTypeEnum.PRODUCTS, res_obj=response)

        assert result == [{'id': '1'}]
        setter_settings_dao.get_endpoint_settings.assert_awaited_once_with(
            session=session,
            endpoint_type=SetterEndpointTypesEnum.GET_PRODUCTS,
        )
        apply_connection_settings_mock.assert_awaited_once_with(
            response_delay=2,
            response_code=202,
            res_obj=response,
            db_session=session,
        )
        setter_request_dao.find_entity_payloads.assert_awaited_once_with(
            session=session,
            entity_type=SetterEntityTypeEnum.PRODUCTS,
        )
