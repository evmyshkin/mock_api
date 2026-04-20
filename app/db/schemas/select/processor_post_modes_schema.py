from app.api.common.schemas.base_schema import BaseSchema


class ProcessorPostModesSchema(BaseSchema):
    id: int
    name: str
    error_message: dict | None
