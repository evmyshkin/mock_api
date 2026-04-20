from typing import Annotated
from typing import Any

from pydantic import Field

from app.api.common.schemas.base_root_schema import BaseRootSchema
from app.api.common.schemas.base_schema import BaseSchema


class ProductItemSchema(BaseSchema):
    """Схема элемента данных товара для строгой валидации."""

    product_id: Annotated[str, Field(description='Идентификатор товара.', min_length=1)]
    sku: Annotated[str, Field(description='SKU товара.', min_length=1)]
    name: Annotated[str, Field(description='Наименование товара.', min_length=1)]
    category: Annotated[str, Field(description='Категория товара.', min_length=1)]
    price: Annotated[float, Field(description='Цена товара.', ge=0)]
    currency: Annotated[
        str,
        Field(description='Код валюты по ISO.', min_length=3, max_length=3, pattern='^[A-Z]{3}$'),
    ]
    quantity: Annotated[int, Field(description='Доступное количество товара.', ge=0)]


class ProductsSetRequestSchema(BaseRootSchema):
    """Строгое тело запроса для эндпоинта записи товаров."""

    root: Annotated[list[ProductItemSchema], Field(min_length=1)]


class ProductsSetOpenRequestSchema(BaseRootSchema):
    """Тело запроса свободного формата для эндпоинта записи товаров (произвольные объекты)."""

    root: Annotated[list[dict[str, Any]], Field(min_length=1)]


class ProductsGetResponseSchema(BaseSchema):
    """Схема ответа эндпоинта чтения товаров."""

    items: Annotated[list[dict[str, Any]], Field(description='Накопленные данные товаров.')]
