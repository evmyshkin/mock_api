from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.models.base_models import BaseDBModel


class SetterRequestModel(BaseDBModel):
    """Модель таблицы для сохраненных записей данных тестовой витрины."""

    __tablename__ = 'requests'
    __table_args__ = {'schema': 'setter_schema'}

    entity_type: Mapped[str]
    payload: Mapped[dict | list] = mapped_column(JSONB, nullable=False)
    is_validated: Mapped[bool] = mapped_column(default=False, server_default=text('False'))
