from app.api.dependencies.dao_deps import ProxyRequestDaoDep
from app.api.dependencies.dao_deps import ProxySettingsDaoDep
from app.api.dependencies.session_deps import SessionDep
from app.api.proxy.services.proxy_service import ProxyService


def get_proxy_service(
    session: SessionDep,
    proxy_request_dao: ProxyRequestDaoDep,
    proxy_settings_dao: ProxySettingsDaoDep,
) -> ProxyService:
    """Предоставить экземпляр сервиса загрузки товаров для API-обработчиков."""
    return ProxyService(
        proxy_request_dao=proxy_request_dao,
        proxy_settings_dao=proxy_settings_dao,
        session=session,
    )
