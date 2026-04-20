from typing import Annotated

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema


class ProcessorValidationErrorSchema(BaseSchema):
    """Структурированное тело ошибки валидации статуса."""

    paths: Annotated[list[str], Field(examples=[['some_field']], alias='Paths')]
    processor_code: Annotated[str, Field(examples=['OP_16'], alias='ProcessorCode')]
    error_code: Annotated[str, Field(examples=['INVALID_VALUE'], alias='ErrorCode')]
    annotation: Annotated[str, Field(examples=['Эмулированный текст ошибки валидации'], alias='Annotation')]


class ProcessorPostErrorLocationSchema(BaseSchema):
    """Описание одной ошибки в теле мгновенной ошибки отправки."""

    loc: Annotated[list[str], Field(description='Путь до поля с ошибкой.', examples=[['body', 'order_id']])]
    msg: Annotated[
        str,
        Field(description='Текст ошибки валидации.', examples=['Эмулированная ошибка валидации отправки']),
    ]
    type: Annotated[
        str,
        Field(description='Код ошибки.', examples=['value_error.processor.mock_error_response']),
    ]


class ProcessorPostErrorDetailSchema(BaseSchema):
    """Коллекция ошибок валидации мгновенной отправки."""

    detail: Annotated[
        list[ProcessorPostErrorLocationSchema],
        Field(description='Список ошибок с путями и сообщениями.'),
    ]


class ProcessorPostValidationErrorSchema(BaseSchema):
    """Схема тела для мгновенного ответа 422."""

    validation_error: Annotated[
        ProcessorPostErrorDetailSchema,
        Field(description='Детали валидации.', alias='validationError'),
    ]
