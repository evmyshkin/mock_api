from collections.abc import AsyncGenerator
from collections.abc import Callable
from functools import wraps
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import config

db_url = config.get_db_url()

# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(url=db_url)
# Создаем фабрику сессий для взаимодействия с базой данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    """Вернуть асинхронную сессию SQLAlchemy.

    Это dependency-friendly обертка для постепенного внедрения DI.
    """
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


def connection(
    method: Callable,
) -> Callable:
    """Декоратор, вызывает асинхронную сессию для метода работы с БД.

    Args:
        method (Callable): вызываемый метод работы с БД

    Returns:
        Callable
    """

    @wraps(method)
    async def _wrapper(*args, **kwargs) -> Any:
        # Позволяем переиспользовать уже открытую сессию в рамках одной операции.
        # Это сохраняет обратную совместимость: старые вызовы без `session` продолжат
        # автоматически создавать отдельную сессию.
        provided_session = kwargs.get('session')
        if provided_session is not None:
            return await method(*args, **kwargs)

        async with async_session_maker() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception:
                await session.rollback()  # Откатываем сессию при ошибке
                raise
            finally:
                await session.close()

    return _wrapper
