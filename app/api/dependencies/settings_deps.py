from app.api.dependencies.dao_deps import ProcessorPostModesDaoDep
from app.api.dependencies.dao_deps import ProcessorSettingsDaoDep
from app.api.dependencies.dao_deps import ProcessorStatusModesDaoDep
from app.api.dependencies.dao_deps import ProcessorStatusModeStepsDaoDep
from app.api.dependencies.dao_deps import ProxySettingsDaoDep
from app.api.dependencies.dao_deps import SetterSettingsDaoDep
from app.api.dependencies.session_deps import SessionDep
from app.api.settings.services.processor_settings_service import ProcessorSettingsService
from app.api.settings.services.proxy_settings_service import ProxySettingsService
from app.api.settings.services.setter_settings_service import SetterSettingsService


def get_setter_settings_service(
    session: SessionDep,
    setter_settings_dao: SetterSettingsDaoDep,
) -> SetterSettingsService:
    """Вернуть сервис настроек витрины."""
    return SetterSettingsService(setter_settings_dao=setter_settings_dao, session=session)


def get_processor_settings_service(
    session: SessionDep,
    processor_settings_dao: ProcessorSettingsDaoDep,
    processor_status_mode_steps_dao: ProcessorStatusModeStepsDaoDep,
    processor_status_modes_dao: ProcessorStatusModesDaoDep,
    processor_post_modes_dao: ProcessorPostModesDaoDep,
) -> ProcessorSettingsService:
    """Вернуть сервис настроек обработки заказов."""
    return ProcessorSettingsService(
        processor_settings_dao=processor_settings_dao,
        processor_status_mode_steps_dao=processor_status_mode_steps_dao,
        processor_status_modes_dao=processor_status_modes_dao,
        processor_post_modes_dao=processor_post_modes_dao,
        session=session,
    )


def get_proxy_settings_service(
    session: SessionDep,
    proxy_settings_dao: ProxySettingsDaoDep,
) -> ProxySettingsService:
    """Вернуть сервис настроек загрузки товаров."""
    return ProxySettingsService(
        proxy_settings_dao=proxy_settings_dao,
        session=session,
    )
