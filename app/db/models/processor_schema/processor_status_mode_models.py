from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.models.base_models import BaseDBModel


class ProcessorStatusModesModel(BaseDBModel):
    """Модель для именованных сценариев перехода статусов."""

    __tablename__ = 'status_modes'
    __table_args__ = {'schema': 'processor_schema'}

    name: Mapped[str] = mapped_column(unique=True)


class ProcessorStatusModeStepsModel(BaseDBModel):
    """Модель шагов статуса внутри каждого сценария переходов."""

    __tablename__ = 'status_mode_steps'
    __table_args__ = (
        UniqueConstraint('status_mode_id', 'step_order', name='uq_processor_step_order'),
        UniqueConstraint('status_mode_id', 'status', name='uq_processor_step_status'),
        {'schema': 'processor_schema'},
    )

    status_mode_id: Mapped[int] = mapped_column(ForeignKey('processor_schema.status_modes.id'))
    step_order: Mapped[int]
    status: Mapped[str]
    duration: Mapped[int]
    error_message: Mapped[list[dict] | None] = mapped_column(JSONB)
