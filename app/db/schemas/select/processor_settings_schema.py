from app.api.common.schemas.base_schema import BaseSchema


class ProcessorSettingsSchema(BaseSchema):
    endpoint_type: str
    response_delay: int
    response_code: int
    status_mode_id: int
    post_mode_id: int
