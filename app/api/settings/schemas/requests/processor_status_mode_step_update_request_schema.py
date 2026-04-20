from typing import Annotated

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema
from app.api.settings.schemas.common.common_schemas import ProcessorValidationErrorSchema


class ProcessorStatusModeStepUpdateRequestSchema(BaseSchema):
    """Тело обновления одного шага статуса в потоке обработки заказов."""

    id: Annotated[int, Field(description='Идентификатор шага статуса.', examples=['1'])]
    duration: Annotated[int, Field(description='Длительность статуса в секундах.', ge=1)]
    error_message: Annotated[
        list[ProcessorValidationErrorSchema] | None,
        Field(default=None, description='Опциональное структурированное тело ошибки для этого статуса.'),
    ]
