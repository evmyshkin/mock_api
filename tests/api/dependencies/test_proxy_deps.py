from app.api.dependencies.dao_deps import get_proxy_request_dao
from app.api.dependencies.dao_deps import get_proxy_settings_dao
from app.api.dependencies.proxy_deps import get_proxy_service
from app.api.dependencies.settings_deps import get_proxy_settings_service
from app.api.proxy.services.proxy_service import ProxyService
from app.api.settings.services.proxy_settings_service import ProxySettingsService
from app.db.dao.proxy_dao.proxy_request_dao import ProxyRequestDao
from app.db.dao.proxy_dao.proxy_settings_dao import ProxySettingsDao


class TestProxyDeps:
    def test_get_proxy_request_dao_returns_expected_instance(self):
        dao = get_proxy_request_dao()

        assert isinstance(dao, ProxyRequestDao)

    def test_get_proxy_settings_dao_returns_expected_instance(self):
        dao = get_proxy_settings_dao()

        assert isinstance(dao, ProxySettingsDao)

    def test_get_proxy_service_wires_session_and_daos(self):
        session = object()
        proxy_request_dao = ProxyRequestDao()
        proxy_settings_dao = ProxySettingsDao()

        service = get_proxy_service(
            session=session,
            proxy_request_dao=proxy_request_dao,
            proxy_settings_dao=proxy_settings_dao,
        )

        assert isinstance(service, ProxyService)
        assert service._session is session
        assert service._proxy_request_dao is proxy_request_dao
        assert service._proxy_settings_dao is proxy_settings_dao

    def test_get_proxy_settings_service_wires_session_and_dao(self):
        session = object()
        proxy_settings_dao = ProxySettingsDao()

        service = get_proxy_settings_service(
            session=session,
            proxy_settings_dao=proxy_settings_dao,
        )

        assert isinstance(service, ProxySettingsService)
        assert service._session is session
        assert service._proxy_settings_dao is proxy_settings_dao
