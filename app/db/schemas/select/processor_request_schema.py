from datetime import datetime

from app.api.common.schemas.base_schema import BaseSchema


class ProcessorRequestSchema(BaseSchema):
    request_id: str
    endpoint_type: str
    order_id: str
    customer_id: str
    response_delay: int
    response_code: int
    post_mode_id: int
    status_mode_id: int
    status_step_id: int
    status_change_after: datetime | None
    unixtimestamp: int
    payload: dict | list
