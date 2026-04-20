from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.models.base_models import BaseDataModel


class ProcessorRequestModel(BaseDataModel):
    """Модель отправленных запросов обработки заказов."""

    __tablename__ = 'requests'
    __table_args__ = {'schema': 'processor_schema'}

    request_id: Mapped[str] = mapped_column(unique=True)
    order_id: Mapped[str]
    customer_id: Mapped[str]
    post_mode_id: Mapped[int] = mapped_column(ForeignKey('processor_schema.post_modes.id'))
    response_delay: Mapped[int]
    response_code: Mapped[int]
    status_mode_id: Mapped[int] = mapped_column(ForeignKey('processor_schema.status_modes.id'))
    status_step_id: Mapped[int] = mapped_column(ForeignKey('processor_schema.status_mode_steps.id'))
    status_change_after: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    unixtimestamp: Mapped[int]
