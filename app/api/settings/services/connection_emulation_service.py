import asyncio

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession


class ConnectionEmulationService:
    @staticmethod
    async def apply_connection_settings(
        response_delay: int,
        response_code: int,
        res_obj: Response,
        db_session: AsyncSession | None = None,
    ) -> None:
        """Применить настройки для ручки.

        Args:
            response_delay (int): задержка ответа в секундах
            response_code (int): код ответа
            res_obj (Response): объект для которого применить настройку
            db_session (AsyncSession | None): открытая сессия, которую можно
                освободить от read-only транзакции перед artificial delay.
        """
        # Для request-scoped сессии не держим открытую транзакцию во время sleep.
        # Это особенно важно для ручек с response_delay, чтобы не занимать
        # соединение пула дольше необходимого.
        if db_session is not None and db_session.in_transaction():
            await db_session.rollback()

        # Вызвать задержку ответа ручки
        await asyncio.sleep(response_delay)

        # Подменить код ответа ручки
        res_obj.status_code = response_code
