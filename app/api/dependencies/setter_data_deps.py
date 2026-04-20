from app.api.dependencies.dao_deps import SetterRequestDaoDep
from app.api.dependencies.session_deps import SessionDep
from app.api.setter.services.setter_data_service import SetterDataService


def get_setter_data_service(
    session: SessionDep,
    setter_request_dao: SetterRequestDaoDep,
) -> SetterDataService:
    """Вернуть сервис отладочных данных витрины."""
    return SetterDataService(setter_request_dao=setter_request_dao, session=session)
