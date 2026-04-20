from typing import Annotated

from pydantic import Field

from app.api.settings.endpoint_types_enum import ProcessorEndpointTypesEnum
from app.api.settings.schemas.responses.base_settings_response_schema import BaseSettingsResponseSchema


class ProcessorSettingsResponseSchema(BaseSettingsResponseSchema):
    """Схема ответа настроек эндпоинтов обработки заказов."""

    endpoint_type: Annotated[
        ProcessorEndpointTypesEnum,
        Field(description='Тип эндпоинта, к которому применяется настройка.'),
    ]
    status_mode_id: Annotated[int, Field(description='Идентификатор режима статусов для переходов.')]
    post_mode_id: Annotated[int, Field(description='Идентификатор режима мгновенного ответа отправки.')]
