import pytest

from app.api.settings.endpoint_types_enum import SetterEndpointTypesEnum
from app.db.dao.setter_dao.setter_settings_dao import SetterSettingsDao


@pytest.fixture
def setter_settings_dao() -> SetterSettingsDao:
    return SetterSettingsDao()


@pytest.mark.asyncio
class TestSetterSettingsDao:
    async def test_get_endpoint_settings_returns_record(self, setter_settings_dao, mocker):
        expected = object()
        find_one_mock = mocker.patch.object(setter_settings_dao, 'find_one_or_none', return_value=expected)
        result = await setter_settings_dao.get_endpoint_settings(endpoint_type=SetterEndpointTypesEnum.GET_PRODUCTS)

        assert result is expected
        find_one_mock.assert_awaited_once_with(
            session=mocker.ANY,
            endpoint_type=SetterEndpointTypesEnum.GET_PRODUCTS.value,
        )

    async def test_get_endpoint_settings_raises_when_missing(self, setter_settings_dao, mocker):
        mocker.patch.object(setter_settings_dao, 'find_one_or_none', return_value=None)
        with pytest.raises(ValueError, match=SetterEndpointTypesEnum.GET_PRODUCTS.value):
            await setter_settings_dao.get_endpoint_settings(endpoint_type=SetterEndpointTypesEnum.GET_PRODUCTS)

    async def test_find_all_settings_proxies_to_find_all_ordered(self, setter_settings_dao, mocker):
        expected = [object()]
        find_all_mock = mocker.patch.object(setter_settings_dao, 'find_all_ordered', return_value=expected)
        result = await setter_settings_dao.find_all_settings()

        assert result == expected
        find_all_mock.assert_awaited_once_with(session=mocker.ANY)

    async def test_update_endpoint_settings_proxies_to_update_one_or_none(self, setter_settings_dao, mocker):
        expected = object()
        values = {'response_code': 400}

        update_mock = mocker.patch.object(setter_settings_dao, 'update_one_or_none', return_value=expected)
        result = await setter_settings_dao.update_endpoint_settings(setting_id=9, values=values)

        assert result is expected
        update_mock.assert_awaited_once_with(session=mocker.ANY, filter_by={'id': 9}, values=values)
