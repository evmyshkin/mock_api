from typing import Annotated

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema


class BaseSettingsResponseSchema(BaseSchema):
    id: Annotated[int, Field(description='Идентификатор записи настройки.', examples=['1'])]
    response_delay: Annotated[int, Field(description='Настроенная задержка ответа в секундах.', examples=['0'])]
    response_code: Annotated[
        int,
        Field(description='Настроенный HTTP-код ответа.', examples=['200']),
    ]
