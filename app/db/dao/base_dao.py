from collections.abc import Mapping
from collections.abc import Sequence
from datetime import datetime
from typing import Any

from sqlalchemy import Result
from sqlalchemy import and_
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.base_models import BaseDBModel
from app.db.session import connection


class BaseDAO:
    model = BaseDBModel  # Устанавливается в дочернем классе

    ############################
    # ВСТАВКА
    ############################

    @connection
    async def add_one(self, session: AsyncSession, **values: object) -> BaseDBModel:
        """Добавляет запись в БД.

        Args:
            session (AsyncSession): асинхронная сесся.
            **values (): атрибуты для заполнения столбцов записиси в БД.

        Returns:
            BaseDBModel: объект записи в БД.
        """

        new_instance = self.model(**values)

        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @connection
    async def add_many(self, session: AsyncSession, instances: list[dict[str, Any]]) -> list[BaseDBModel]:
        """Добавляет несколько записей в БД.

        Args:
            instances (list[dict[str, Any]]): объекты с атрибутами, которые
            нужно вставить в БД.
            session (AsyncSession): асинхронная сесся.

        Returns:
            list[BaseDBModel]: список объектов записей в БД.
        """

        new_instances = [self.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances

    ############################
    # ЧТЕНИЕ
    ############################

    @connection
    async def find_one_or_none(self, session: AsyncSession, **filter_by: object) -> BaseDBModel | None:
        """Ищет запись в БД по атрибутам.

        Args:
            **filter_by (): искомые атрибуты.
            session (AsyncSession): асинхронная сесся.

        Returns:
            BaseDBModel | None: объект записи в БД или None, если не нашли.
        """

        conditions = [getattr(self.model, field) == value for field, value in filter_by.items()]
        query = select(self.model).where(and_(*conditions))
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        return record

    @connection
    async def find_one_or_none_by_id(self, data_id: int, session: AsyncSession) -> BaseDBModel | None:
        """Ищет запись в БД по id.

        Args:
            data_id (int): идентификатор для поиска.
            session (AsyncSession): асинхронная сессия.

        Returns:
            BaseDBModel | None: объект записи в БД или None, если не нашли.

        """

        query = select(self.model).where(self.model.id == data_id)
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        return record

    @connection
    async def find_all_ordered(self, session: AsyncSession, **filter_by) -> Sequence[BaseDBModel]:
        """Найти все записи по критериям.

        Args:
            session (AsyncSession): асинхронная сессия.
            **filter_by (): критерии для фильтрации при поиске в БД.

        Returns:
            Sequence[BaseDBModel]:
        """

        conditions = [getattr(self.model, field) == value for field, value in filter_by.items()]
        query = select(self.model).where(and_(*conditions)).order_by(self.model.id)
        result = await session.execute(query)
        records = result.scalars().all()
        return records

    ############################
    # ОБНОВЛЕНИЕ
    ############################

    @connection
    async def update_records(
        self,
        session: AsyncSession,
        filter_by: Mapping[str, Any],
        values: Mapping[str, Any],
    ) -> None:
        """Обновить найденные записи на переданные значения.

        Args:
            session (AsyncSession): асинхронная сессия
            filter_by (dict): условия фильтрации
            values (dict): значения для обновления
        """
        conditions = [getattr(self.model, k) == v for k, v in filter_by.items()]
        stmt = update(self.model).where(and_(*conditions)).values(**values)
        await session.execute(stmt)
        await session.commit()

    @connection
    async def update_one_or_none(
        self, session: AsyncSession, filter_by: Mapping[str, Any], values: Mapping[str, Any]
    ) -> BaseDBModel | None:
        """Обновляет одну запись, если она найдена, иначе возвращает None.

        Args:
            session (AsyncSession): асинхронная сессия
            filter_by (dict): условия фильтрации.
            values (dict): значения для обновления.

        Returns:
            Optional[BaseDBModel]: обновлённая запись или None.
        """
        conditions = [getattr(self.model, k) == v for k, v in filter_by.items()]
        stmt = (
            update(self.model)
            .where(and_(*conditions))
            .values(**values)
            .execution_options(synchronize_session='fetch')  # чтобы вернуть объект после обновления
            .returning(self.model)
        )

        result = await session.execute(stmt)
        updated_record = result.scalar_one_or_none()  # вернёт None, если не нашёл

        await session.commit()
        return updated_record

    ############################
    # УДАЛЕНИЕ
    ############################

    @connection
    async def clear_old_data(
        self,
        session: AsyncSession,
        cutoff: datetime,
    ) -> Result[Any]:
        """Удаляет записи старше чем cutoff.

         Проверка по полю cls.model.created

        Args:
            session (AsyncSession): асинхронная сессия
            cutoff (datetime): время, раньге которого надо удалить записи.

        Returns:
            Result[Any]: объект с информацией о статусе удаления.
        """

        query = delete(self.model).where(self.model.created < cutoff)

        result = await session.execute(query)
        await session.commit()

        return result
