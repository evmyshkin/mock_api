from typing import Annotated

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema
from app.api.settings.schemas.common.common_schemas import ProcessorValidationErrorSchema


class ProcessorStatusModeStepsResponseSchema(BaseSchema):
    """Описание шага статуса."""

    id: Annotated[int, Field(description='Идентификатор шага статуса.')]
    status_mode_id: Annotated[int, Field(description='Идентификатор родительского режима статусов.')]
    step_order: Annotated[int, Field(description='Порядок шага статуса в режиме.')]
    status: Annotated[str, Field(description='Значение статуса, возвращаемое эндпоинтом статуса.')]
    duration: Annotated[int, Field(description='Длительность статуса в секундах.', ge=1)]
    error_message: Annotated[
        list[ProcessorValidationErrorSchema] | None,
        Field(description='Опциональное структурированное тело ошибки для этого статуса.'),
    ]


class ProcessorStatusModeStepsNamedResponseSchema(ProcessorStatusModeStepsResponseSchema):
    """Описание шага статуса с именем режима статусов."""

    status_mode_name: Annotated[str, Field(description='Человекочитаемое название режима статусов.')]
