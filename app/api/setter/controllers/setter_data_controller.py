from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.setter_data_deps import get_setter_data_service
from app.api.setter.schemas.setter_data_response_schema import SetterDataResponseSchema
from app.api.setter.services.setter_data_service import SetterDataService

router = APIRouter()
SetterDataServiceDep = Annotated[SetterDataService, Depends(get_setter_data_service)]


@router.get('/requests', summary='Получить сохраненные setter-запросы.')
async def get_setter_data(
    service: SetterDataServiceDep,
) -> list[SetterDataResponseSchema]:
    """Вернуть сохраненные setter requests для отладки."""
    return await service.get_setter_data()
