from app.api.common.schemas.base_schema import BaseSchema


class ProcessorStatusModeStepsSchema(BaseSchema):
    id: int
    status_mode_id: int
    step_order: int
    status: str
    duration: int
    error_message: list[dict] | None
