from app.api.dependencies.dao_deps import SetterRequestDaoDep
from app.api.dependencies.dao_deps import SetterSettingsDaoDep
from app.api.dependencies.session_deps import SessionDep
from app.api.setter.services.setter_service import SetterService


def get_setter_service(
    session: SessionDep,
    setter_request_dao: SetterRequestDaoDep,
    setter_settings_dao: SetterSettingsDaoDep,
) -> SetterService:
    """Предоставить экземпляр сервиса витрины для API-обработчиков."""
    return SetterService(
        setter_request_dao=setter_request_dao,
        setter_settings_dao=setter_settings_dao,
        session=session,
    )
