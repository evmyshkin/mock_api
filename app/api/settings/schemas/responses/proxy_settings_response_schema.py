from typing import Annotated

from pydantic import Field

from app.api.settings.endpoint_types_enum import ProxyEndpointTypesEnum
from app.api.settings.schemas.responses.base_settings_response_schema import BaseSettingsResponseSchema


class ProxySettingsResponseSchema(BaseSettingsResponseSchema):
    """Схема ответа настроек загрузки товаров."""

    endpoint_type: Annotated[
        ProxyEndpointTypesEnum,
        Field(description='Тип эндпоинта для настроек эмуляции ответа загрузки товаров.'),
    ]
