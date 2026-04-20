from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.models.base_models import BaseDBModel


class ProxyRequestModel(BaseDBModel):
    """Модель таблицы для сохраненных запросов загрузки товаров."""

    __tablename__ = 'requests'
    __table_args__ = {'schema': 'proxy_schema'}

    request_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    query_params: Mapped[dict] = mapped_column(JSONB, nullable=False)
    headers: Mapped[dict] = mapped_column(JSONB, nullable=False)
    body: Mapped[dict] = mapped_column(JSONB, nullable=False)
