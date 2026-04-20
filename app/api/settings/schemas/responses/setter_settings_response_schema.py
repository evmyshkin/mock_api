from typing import Annotated

from pydantic import Field

from app.api.settings.endpoint_types_enum import SetterEndpointTypesEnum
from app.api.settings.schemas.responses.base_settings_response_schema import BaseSettingsResponseSchema


class SetterSettingsResponseSchema(BaseSettingsResponseSchema):
    """Схема ответа настроек эндпоинтов витрины."""

    endpoint_type: Annotated[
        SetterEndpointTypesEnum,
        Field(description='Тип эндпоинта, к которому применяются настройки.'),
    ]
