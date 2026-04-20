from app.api.common.schemas.base_schema import BaseSchema
from app.db.schemas.select.processor_request_schema import ProcessorRequestSchema
from app.db.schemas.select.processor_status_mode_steps_schema import ProcessorStatusModeStepsSchema


class ProcessorRequestAndStatusStepsSchema(BaseSchema):
    """Схема запроса заказа с присоединенным текущим шагом статуса."""

    request: ProcessorRequestSchema
    status_mode_steps: ProcessorStatusModeStepsSchema
