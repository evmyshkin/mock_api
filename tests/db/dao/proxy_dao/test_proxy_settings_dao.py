import pytest

from app.api.settings.endpoint_types_enum import ProxyEndpointTypesEnum
from app.db.dao.proxy_dao.proxy_settings_dao import ProxySettingsDao


@pytest.fixture
def proxy_settings_dao() -> ProxySettingsDao:
    return ProxySettingsDao()


@pytest.mark.asyncio
class TestProxySettingsDao:
    async def test_get_endpoint_settings_returns_record(self, proxy_settings_dao, mocker):
        expected = object()
        find_one_mock = mocker.patch.object(proxy_settings_dao, 'find_one_or_none', return_value=expected)

        result = await proxy_settings_dao.get_endpoint_settings(endpoint_type=ProxyEndpointTypesEnum.CAPTURE)

        assert result is expected
        find_one_mock.assert_awaited_once_with(
            session=mocker.ANY,
            endpoint_type=ProxyEndpointTypesEnum.CAPTURE.value,
        )

    async def test_get_endpoint_settings_raises_when_missing(self, proxy_settings_dao, mocker):
        mocker.patch.object(proxy_settings_dao, 'find_one_or_none', return_value=None)

        with pytest.raises(ValueError, match=ProxyEndpointTypesEnum.CAPTURE.value):
            await proxy_settings_dao.get_endpoint_settings(endpoint_type=ProxyEndpointTypesEnum.CAPTURE)

    async def test_find_all_settings_proxies_to_find_all_ordered(self, proxy_settings_dao, mocker):
        expected = [object()]
        find_all_mock = mocker.patch.object(proxy_settings_dao, 'find_all_ordered', return_value=expected)

        result = await proxy_settings_dao.find_all_settings()

        assert result == expected
        find_all_mock.assert_awaited_once_with(session=mocker.ANY)

    async def test_update_endpoint_settings_proxies_to_update_one_or_none(self, proxy_settings_dao, mocker):
        expected = object()
        values = {'response_code': 503}
        update_mock = mocker.patch.object(proxy_settings_dao, 'update_one_or_none', return_value=expected)

        result = await proxy_settings_dao.update_endpoint_settings(setting_id=3, values=values)

        assert result is expected
        update_mock.assert_awaited_once_with(session=mocker.ANY, filter_by={'id': 3}, values=values)
