from typing import Annotated

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema
from app.api.settings.schemas.common.common_schemas import ProcessorPostValidationErrorSchema


class ProcessorPostModesResponseSchema(BaseSchema):
    """Описание POST-режима для эндпоинта отправки."""

    id: Annotated[int, Field(description='Идентификатор POST-режима.')]
    name: Annotated[str, Field(description='Название POST-режима.')]
    error_message: Annotated[
        ProcessorPostValidationErrorSchema | None,
        Field(description='Опциональное тело мгновенного ответа 422.'),
    ]
