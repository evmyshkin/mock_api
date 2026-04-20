from fastapi import APIRouter

from app.api.common.schemas.info_response_schema import InfoResponseSchema

router = APIRouter()


@router.get(
    '/healthcheck',
    response_model_exclude_none=True,
    summary='Ручка хелсчека.',
    description='Ручка хелсчека.',
)
async def healthcheck() -> InfoResponseSchema:
    """Хелсчек.

    Returns:
        InfoResponseSchema:
    """
    return InfoResponseSchema(info='сервис работает')
