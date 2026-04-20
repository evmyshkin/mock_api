from typing import Annotated

from pydantic import Field

from app.api.settings.schemas.requests.base_settings_request_schema import BaseSettingsUpdateRequestSchema


class ProcessorSettingsUpdateRequestSchema(BaseSettingsUpdateRequestSchema):
    """Тело обновления настроек эндпоинтов обработки заказов."""

    status_mode_id: Annotated[
        int,
        Field(description='Идентификатор режима статусов для потока машины состояний.', ge=1),
    ]
    post_mode_id: Annotated[int, Field(description='Идентификатор режима мгновенного POST-ответа.', ge=1)]
