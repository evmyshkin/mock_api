from typing import Annotated

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema


class SetterClearResponseSchema(BaseSchema):
    """Унифицированная схема ответа для эндпоинтов очистки."""

    info: Annotated[str, Field(description='Описание результата.')]
    deleted_count: Annotated[int, Field(description='Количество удаленных записей.', ge=0)]
