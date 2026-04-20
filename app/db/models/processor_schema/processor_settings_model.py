from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.models.base_models import BaseSettingsModel


class ProcessorSettingsModel(BaseSettingsModel):
    """Модель настроек для эндпоинтов обработки заказов."""

    __tablename__ = 'settings'
    __table_args__ = {'schema': 'processor_schema'}

    status_mode_id: Mapped[int] = mapped_column(ForeignKey('processor_schema.status_modes.id'))
    post_mode_id: Mapped[int] = mapped_column(ForeignKey('processor_schema.post_modes.id'))
