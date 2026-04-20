from pydantic import ConfigDict

from app.api.common.schemas.base_schema import BaseSchema


class OpenPayloadItemSchema(BaseSchema):
    """Базовая схема для элементов данных свободного формата с разрешенными дополнительными полями."""

    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        validate_assignment=True,
        from_attributes=True,
        extra='allow',
    )
