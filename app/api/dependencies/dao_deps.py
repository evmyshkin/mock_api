from typing import Annotated

from fastapi import Depends

from app.db.dao.processor_dao.processor_post_modes_dao import ProcessorPostModesDao
from app.db.dao.processor_dao.processor_request_dao import ProcessorRequestDao
from app.db.dao.processor_dao.processor_settings_dao import ProcessorSettingsDao
from app.db.dao.processor_dao.processor_status_mode_steps_dao import ProcessorStatusModeStepsDao
from app.db.dao.processor_dao.processor_status_modes_dao import ProcessorStatusModesDao
from app.db.dao.proxy_dao.proxy_request_dao import ProxyRequestDao
from app.db.dao.proxy_dao.proxy_settings_dao import ProxySettingsDao
from app.db.dao.setter_dao.setter_request_dao import SetterRequestDao
from app.db.dao.setter_dao.setter_settings_dao import SetterSettingsDao


def get_processor_request_dao() -> ProcessorRequestDao:
    """Создать DAO для записей запросов обработки заказов."""
    return ProcessorRequestDao()


def get_proxy_settings_dao() -> ProxySettingsDao:
    """Создать DAO для настроек эндпоинтов загрузки товаров."""
    return ProxySettingsDao()


def get_proxy_request_dao() -> ProxyRequestDao:
    """Создать DAO для сохраненных записей загрузки товаров."""
    return ProxyRequestDao()


def get_processor_settings_dao() -> ProcessorSettingsDao:
    """Создать DAO для настроек эндпоинтов обработки заказов."""
    return ProcessorSettingsDao()


def get_processor_post_modes_dao() -> ProcessorPostModesDao:
    """Создать DAO для POST-режимов обработки заказов."""
    return ProcessorPostModesDao()


def get_processor_status_mode_steps_dao() -> ProcessorStatusModeStepsDao:
    """Создать DAO для шагов режима статусов обработки заказов."""
    return ProcessorStatusModeStepsDao()


def get_processor_status_modes_dao() -> ProcessorStatusModesDao:
    """Создать DAO для режимов статусов обработки заказов."""
    return ProcessorStatusModesDao()


def get_setter_settings_dao() -> SetterSettingsDao:
    """Создать DAO для настроек эндпоинтов витрины."""
    return SetterSettingsDao()


def get_setter_request_dao() -> SetterRequestDao:
    """Создать DAO для записей данных витрины."""
    return SetterRequestDao()


ProxySettingsDaoDep = Annotated[ProxySettingsDao, Depends(get_proxy_settings_dao)]
ProxyRequestDaoDep = Annotated[ProxyRequestDao, Depends(get_proxy_request_dao)]
ProcessorRequestDaoDep = Annotated[ProcessorRequestDao, Depends(get_processor_request_dao)]
ProcessorSettingsDaoDep = Annotated[ProcessorSettingsDao, Depends(get_processor_settings_dao)]
ProcessorPostModesDaoDep = Annotated[ProcessorPostModesDao, Depends(get_processor_post_modes_dao)]
ProcessorStatusModeStepsDaoDep = Annotated[
    ProcessorStatusModeStepsDao,
    Depends(get_processor_status_mode_steps_dao),
]
ProcessorStatusModesDaoDep = Annotated[
    ProcessorStatusModesDao,
    Depends(get_processor_status_modes_dao),
]
SetterRequestDaoDep = Annotated[SetterRequestDao, Depends(get_setter_request_dao)]
SetterSettingsDaoDep = Annotated[SetterSettingsDao, Depends(get_setter_settings_dao)]
