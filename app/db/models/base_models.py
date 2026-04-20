from datetime import datetime
from typing import Any

from sqlalchemy import TIMESTAMP
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.elements import KeyedColumnElement


# Базовый класс для моделей ОРД и СИ
class BaseDBModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    @classmethod
    def jsonb_build_object(
        cls,
        exclude: list[str] | None = None,
        alias: object | None = None,
    ) -> list[Any]:
        """Собрать JSONB-объект для модели.

        Args:
            exclude: Исключаемые поля.
            alias: Передаем объект алиаса

        Returns:
            list[ключ колонки, колонка]
        """

        payload: list[KeyedColumnElement | str] = []

        if not exclude:
            exclude = []

        # Коллекция столбцов поддерживает итерацию
        for column in cls.__table__.columns:  # type: ignore
            if column.key in exclude:
                continue

            payload.append(column.key)

            if alias:
                payload.append(getattr(alias, column.key))

            else:
                payload.append(column)

        return payload


class BaseSettingsModel(BaseDBModel):
    __abstract__ = True

    endpoint_type: Mapped[str] = mapped_column(unique=True)
    response_delay: Mapped[int]
    response_code: Mapped[int]


class BaseDataModel(BaseDBModel):
    __abstract__ = True

    endpoint_type: Mapped[str]
    payload: Mapped[dict | list] = mapped_column(JSONB, nullable=False)
