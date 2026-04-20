from datetime import datetime
from typing import Any

from app.api.common.schemas.base_schema import BaseSchema
from app.api.settings.endpoint_types_enum import ProcessorEndpointTypesEnum


class ProcessorRequestInsertSchema(BaseSchema):
    """Схема вставки для processor_schema.requests."""

    request_id: str
    endpoint_type: ProcessorEndpointTypesEnum
    order_id: str
    customer_id: str
    post_mode_id: int
    status_mode_id: int
    status_step_id: int
    unixtimestamp: int
    response_code: int
    response_delay: int
    status_change_after: datetime | None = None
    payload: Any
