from app.api.dependencies.dao_deps import ProcessorRequestDaoDep
from app.api.dependencies.dao_deps import ProcessorSettingsDaoDep
from app.api.dependencies.session_deps import SessionDep
from app.api.processor.services.processor_service import ProcessorService


def get_processor_service(
    session: SessionDep,
    processor_request_dao: ProcessorRequestDaoDep,
    processor_settings_dao: ProcessorSettingsDaoDep,
) -> ProcessorService:
    """Вернуть сервис для эндпоинтов submit/status обработки заказов."""
    return ProcessorService(
        processor_request_dao=processor_request_dao,
        processor_settings_dao=processor_settings_dao,
        session=session,
    )
