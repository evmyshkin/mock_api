from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response

from app.api.common.schemas.info_response_schema import InfoResponseSchema
from app.api.dependencies.setter_deps import get_setter_service
from app.api.setter.enums import SetterEntityTypeEnum
from app.api.setter.schemas.v1.setter_clear_response_schema import SetterClearResponseSchema
from app.api.setter.schemas.v1.setter_products_schema import ProductsGetResponseSchema
from app.api.setter.schemas.v1.setter_products_schema import ProductsSetOpenRequestSchema
from app.api.setter.schemas.v1.setter_products_schema import ProductsSetRequestSchema
from app.api.setter.services.setter_service import SetterService

router = APIRouter()
SetterServiceDep = Annotated[SetterService, Depends(get_setter_service)]


@router.post('/products/set', summary='Сохранить валидированные данные товаров.')
async def set_products(
    request: ProductsSetRequestSchema,
    service: SetterServiceDep,
) -> InfoResponseSchema:
    """Сохранить данные товаров со строгой валидацией схемы."""
    return await service.set_data(entity_type=SetterEntityTypeEnum.PRODUCTS, request=request)


@router.post('/products/set-open', summary='Сохранить данные товаров по свободной схеме.')
async def set_products_open(
    request: ProductsSetOpenRequestSchema,
    service: SetterServiceDep,
) -> InfoResponseSchema:
    """Сохранить данные товаров с валидацией по свободной схеме."""
    return await service.set_data_open(entity_type=SetterEntityTypeEnum.PRODUCTS, request=request)


@router.get('/products', summary='Получить накопленные записи данных товаров.')
async def get_products(
    response: Response,
    service: SetterServiceDep,
) -> ProductsGetResponseSchema:
    """Вернуть все накопленные записи данных товаров."""
    data = await service.get_data(entity_type=SetterEntityTypeEnum.PRODUCTS, res_obj=response)
    return ProductsGetResponseSchema(items=data)


@router.delete('/products', summary='Полностью очистить записи данных товаров.')
async def clear_products(
    service: SetterServiceDep,
) -> SetterClearResponseSchema:
    """Полностью удалить записи данных товаров."""
    return await service.clear_entity(entity_type=SetterEntityTypeEnum.PRODUCTS)


@router.delete('/clear', summary='Полностью очистить все записи данных витрины.')
async def clear_all(
    service: SetterServiceDep,
) -> SetterClearResponseSchema:
    """Полностью удалить все записи данных для всех сущностей витрины."""
    return await service.clear_all()
