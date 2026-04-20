from typing import Any

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.settings.endpoint_types_enum import ProcessorEndpointTypesEnum
from app.db.dao.settings_dao import SettingsDao
from app.db.models.processor_schema.processor_post_mode_model import ProcessorPostModesModel
from app.db.models.processor_schema.processor_settings_model import ProcessorSettingsModel
from app.db.models.processor_schema.processor_status_mode_models import ProcessorStatusModesModel
from app.db.models.processor_schema.processor_status_mode_models import ProcessorStatusModeStepsModel
from app.db.schemas.select.processor_full_config_schema import FullProcessorConfigSchema
from app.db.session import connection


class ProcessorSettingsDao(SettingsDao):
    """DAO для настроек эндпоинтов и обновлений прогресса статусов."""

    model = ProcessorSettingsModel

    @connection
    async def get_endpoint_full_config(
        self,
        session: AsyncSession,
        endpoint_type: ProcessorEndpointTypesEnum,
    ) -> FullProcessorConfigSchema:
        """Получить настройки эндпоинта и связанные детали режимов отправки/статуса."""

        query = (
            select(
                func.jsonb_build_object(
                    'settings',
                    func.jsonb_build_object(*ProcessorSettingsModel.jsonb_build_object()),
                    'status_modes',
                    func.jsonb_build_object(*ProcessorStatusModesModel.jsonb_build_object()),
                    'status_mode_steps',
                    func.jsonb_build_object(*ProcessorStatusModeStepsModel.jsonb_build_object()),
                    'status_mode_len',
                    select(func.count(ProcessorStatusModeStepsModel.id))
                    .where(ProcessorStatusModeStepsModel.status_mode_id == ProcessorStatusModesModel.id)
                    .correlate(ProcessorStatusModesModel)
                    .scalar_subquery(),
                    'post_modes',
                    func.jsonb_build_object(*ProcessorPostModesModel.jsonb_build_object()),
                )
            )
            .join(
                ProcessorStatusModesModel,
                ProcessorSettingsModel.status_mode_id == ProcessorStatusModesModel.id,
            )
            .join(
                ProcessorStatusModeStepsModel,
                ProcessorStatusModesModel.id == ProcessorStatusModeStepsModel.status_mode_id,
            )
            .join(
                ProcessorPostModesModel,
                ProcessorSettingsModel.post_mode_id == ProcessorPostModesModel.id,
            )
            .where(
                ProcessorSettingsModel.endpoint_type == endpoint_type.value,
                ProcessorStatusModeStepsModel.step_order == 1,
            )
        )

        result = await session.execute(query)
        row = result.scalar_one_or_none()

        if row is None:
            raise ValueError(f'Настройки эндпоинта не найдены для {endpoint_type.value}')

        return FullProcessorConfigSchema.model_validate(row)

    @connection
    async def advance_status_steps(self, session: AsyncSession) -> list[Any]:
        """Перевести ожидающие запросы заказа на следующий шаг статуса."""

        stmt = text("""
            UPDATE processor_schema.requests req
            SET status_step_id = next_step.id,
                status_change_after = CASE
                    WHEN next_step.step_order = (
                        SELECT MAX(steps.step_order)
                        FROM processor_schema.status_mode_steps steps
                        WHERE steps.status_mode_id = next_step.status_mode_id
                    )
                    THEN NULL
                    ELSE req.status_change_after + (next_step.duration * INTERVAL '1 second')
                END,
                updated = NOW()
            FROM processor_schema.status_mode_steps current_step
            JOIN processor_schema.status_mode_steps next_step
              ON next_step.status_mode_id = current_step.status_mode_id
             AND next_step.step_order = current_step.step_order + 1
            WHERE current_step.id = req.status_step_id
              AND req.status_change_after IS NOT NULL
              AND req.status_change_after <= NOW()
            RETURNING req.request_id, req.order_id,
                (
                    SELECT s.status
                    FROM processor_schema.status_mode_steps s
                    WHERE s.id = req.status_step_id
                ) AS status
        """)

        result = await session.execute(stmt)
        await session.commit()
        return [row for row in result]
