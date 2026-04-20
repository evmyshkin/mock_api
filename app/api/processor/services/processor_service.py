import time
import uuid

from datetime import UTC
from datetime import datetime

from fastapi import HTTPException
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.processor.schemas.requests.processor_submit_request_schema import ProcessorSubmitRequestSchema
from app.api.processor.schemas.responses.processor_request_response_schema import ProcessorRequestResponseSchema
from app.api.processor.schemas.responses.processor_status_response_schema import ProcessorStatusResponseSchema
from app.api.processor.schemas.responses.processor_submit_response_schema import ProcessorSubmitResponseSchema
from app.api.processor.utils.processor_exceptions import ProcessorSubmitError
from app.api.settings.endpoint_types_enum import ProcessorEndpointTypesEnum
from app.api.settings.services.connection_emulation_service import ConnectionEmulationService
from app.db.dao.processor_dao.processor_request_dao import ProcessorRequestDao
from app.db.dao.processor_dao.processor_settings_dao import ProcessorSettingsDao
from app.db.schemas.insert.processor_request_insert_schema import ProcessorRequestInsertSchema
from app.db.schemas.select.processor_request_and_status_steps_schema import ProcessorRequestAndStatusStepsSchema


class ProcessorService:
    """Сервис, реализующий поведение submit/status для mock-обработки заказов."""

    submit_endpoint_type = ProcessorEndpointTypesEnum.SUBMIT
    status_endpoint_type = ProcessorEndpointTypesEnum.STATUS

    def __init__(
        self,
        processor_request_dao: ProcessorRequestDao,
        processor_settings_dao: ProcessorSettingsDao,
        session: AsyncSession,
    ) -> None:
        self._processor_request_dao = processor_request_dao
        self._processor_settings_dao = processor_settings_dao
        self._session = session

    async def submit_order(
        self,
        request: ProcessorSubmitRequestSchema,
        res_obj: Response,
    ) -> ProcessorSubmitResponseSchema:
        """Обработать отправку заказа и зарегистрировать запрос в машине состояний."""

        request_id = str(uuid.uuid4())
        unixtimestamp = int(time.time())

        config = await self._processor_settings_dao.get_endpoint_full_config(
            session=self._session,
            endpoint_type=self.submit_endpoint_type,
        )

        post_mode_error_message = config.post_modes.error_message
        response_delay = config.settings.response_delay
        response_code = config.settings.response_code

        status = config.status_mode_steps.status
        status_mode_id = config.status_modes.id
        status_step_id = config.status_mode_steps.id
        status_step_order = config.status_mode_steps.step_order
        status_mode_len = config.status_mode_len
        status_error_message = config.status_mode_steps.error_message

        status_change_after = (
            datetime.fromtimestamp(
                unixtimestamp + config.status_mode_steps.duration,
                tz=UTC,
            )
            if status_step_order < status_mode_len
            else None
        )

        await ConnectionEmulationService.apply_connection_settings(
            response_delay=response_delay,
            response_code=response_code,
            res_obj=res_obj,
            db_session=self._session,
        )

        if post_mode_error_message is not None:
            raise ProcessorSubmitError(status_code=422, msg=post_mode_error_message)

        response = ProcessorSubmitResponseSchema(
            request_id=request_id,
            order_id=request.order_id,
            status=status,
            unixtimestamp=unixtimestamp,
            error_message=status_error_message,
        )

        values = ProcessorRequestInsertSchema(
            request_id=request_id,
            endpoint_type=self.submit_endpoint_type,
            order_id=request.order_id,
            customer_id=request.customer_id,
            post_mode_id=config.post_modes.id,
            status_mode_id=status_mode_id,
            status_step_id=status_step_id,
            unixtimestamp=unixtimestamp,
            response_code=response_code,
            response_delay=response_delay,
            status_change_after=status_change_after,
            payload=request.model_dump(mode='json', by_alias=True),
        )

        await self._processor_request_dao.add_request(session=self._session, values=values)

        return response

    async def get_order_status(self, request_id: str, res_obj: Response) -> ProcessorStatusResponseSchema:
        """Получить текущий статус обработки для отправленного запроса заказа."""

        settings = await self._processor_settings_dao.get_endpoint_settings(
            session=self._session,
            endpoint_type=self.status_endpoint_type,
        )

        await ConnectionEmulationService.apply_connection_settings(
            response_delay=settings.response_delay,
            response_code=settings.response_code,
            res_obj=res_obj,
            db_session=self._session,
        )

        order_request = await self._processor_request_dao.find_request_and_status(
            session=self._session,
            request_id=request_id,
        )

        if order_request is None:
            raise HTTPException(status_code=404, detail='Запрос обработки заказа не найден по request_id')

        response_data = ProcessorRequestAndStatusStepsSchema.model_validate(order_request)

        return ProcessorStatusResponseSchema(
            request_id=response_data.request.request_id,
            order_id=response_data.request.order_id,
            status=response_data.status_mode_steps.status,
            unixtimestamp=response_data.request.unixtimestamp,
            error_message=response_data.status_mode_steps.error_message,
        )

    async def get_requests(self) -> list[ProcessorRequestResponseSchema]:
        """Вернуть сохраненные requests обработки в порядке от новых к старым."""

        records = await self._processor_request_dao.find_requests(session=self._session)
        return [ProcessorRequestResponseSchema.model_validate(record) for record in records]
