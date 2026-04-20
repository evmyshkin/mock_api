from typing import Annotated

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema


class BaseSettingsUpdateRequestSchema(BaseSchema):
    id: Annotated[int, Field(description='Идентификатор записи настройки.', ge=1, examples=['1'])]
    response_delay: Annotated[
        int,
        Field(description='Задержка ответа в секундах.', default=0, ge=0, examples=['0']),
    ]
    response_code: Annotated[
        int,
        Field(description='HTTP-код ответа.', default=200, ge=100, le=599, examples=['200']),
    ]
