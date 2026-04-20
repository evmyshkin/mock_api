from typing import Annotated

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema


class ProcessorStatusModesResponseSchema(BaseSchema):
    """Описание режима статусов."""

    id: Annotated[int, Field(description='Идентификатор режима статусов.')]
    name: Annotated[str, Field(description='Название режима статусов.')]
