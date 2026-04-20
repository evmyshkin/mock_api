from typing import Annotated
from typing import Any

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema


class InfoResponseSchema(BaseSchema):
    info: Annotated[str, Field(description='Информация о запросе.')]
    context: Annotated[Any | None, Field(description=('Дополнительная информация о выполнении запроса.'))] = None
