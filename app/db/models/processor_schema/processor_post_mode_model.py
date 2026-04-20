from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.models.base_models import BaseDBModel


class ProcessorPostModesModel(BaseDBModel):
    """Модель для режимов мгновенного POST-ответа."""

    __tablename__ = 'post_modes'
    __table_args__ = {'schema': 'processor_schema'}

    name: Mapped[str] = mapped_column(unique=True)
    error_message: Mapped[dict | None] = mapped_column(JSONB)
