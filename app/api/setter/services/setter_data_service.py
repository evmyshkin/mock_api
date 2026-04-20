from sqlalchemy.ext.asyncio import AsyncSession

from app.api.setter.schemas.setter_data_response_schema import SetterDataResponseSchema
from app.db.dao.setter_dao.setter_request_dao import SetterRequestDao


class SetterDataService:
    """Сервис чтения отладочных снимков записей витрины."""

    def __init__(self, setter_request_dao: SetterRequestDao, session: AsyncSession) -> None:
        self._setter_request_dao = setter_request_dao
        self._session = session

    async def get_setter_data(self) -> list[SetterDataResponseSchema]:
        """Вернуть все сохраненные записи витрины."""
        data = await self._setter_request_dao.find_all_requests(session=self._session)
        return [SetterDataResponseSchema.model_validate(item) for item in data]
