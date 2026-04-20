import pytest

from app.api.settings.endpoint_types_enum import ProcessorEndpointTypesEnum
from app.api.settings.endpoint_types_enum import ProxyEndpointTypesEnum
from app.api.settings.endpoint_types_enum import SetterEndpointTypesEnum
from app.api.settings.schemas.common.common_schemas import ProcessorPostErrorDetailSchema
from app.api.settings.schemas.common.common_schemas import ProcessorPostErrorLocationSchema
from app.api.settings.schemas.common.common_schemas import ProcessorPostValidationErrorSchema
from app.api.settings.schemas.common.common_schemas import ProcessorValidationErrorSchema
from app.api.settings.schemas.requests.base_settings_request_schema import BaseSettingsUpdateRequestSchema
from app.api.settings.schemas.requests.processor_settings_update_request_schema import (
    ProcessorSettingsUpdateRequestSchema,
)
from app.api.settings.schemas.requests.processor_status_mode_step_update_request_schema import (
    ProcessorStatusModeStepUpdateRequestSchema,
)
from app.api.settings.schemas.responses.processor_post_modes_response_schema import ProcessorPostModesResponseSchema
from app.api.settings.schemas.responses.processor_settings_response_schema import ProcessorSettingsResponseSchema
from app.api.settings.schemas.responses.processor_status_mode_steps_response_schemas import (
    ProcessorStatusModeStepsNamedResponseSchema,
)
from app.api.settings.schemas.responses.processor_status_mode_steps_response_schemas import (
    ProcessorStatusModeStepsResponseSchema,
)
from app.api.settings.schemas.responses.processor_status_modes_response_schema import ProcessorStatusModesResponseSchema
from app.api.settings.schemas.responses.proxy_settings_response_schema import ProxySettingsResponseSchema
from app.api.settings.schemas.responses.setter_settings_response_schema import SetterSettingsResponseSchema


@pytest.fixture
def processor_settings_update_request() -> ProcessorSettingsUpdateRequestSchema:
    return ProcessorSettingsUpdateRequestSchema(
        id=1,
        response_delay=3,
        response_code=201,
        status_mode_id=2,
        post_mode_id=1,
    )


@pytest.fixture
def processor_status_mode_step_update_request() -> ProcessorStatusModeStepUpdateRequestSchema:
    return ProcessorStatusModeStepUpdateRequestSchema(
        id=10,
        duration=30,
        error_message=[
            ProcessorValidationErrorSchema(
                paths=['field'],
                processor_code='OP_16',
                error_code='INVALID_VALUE',
                annotation='Ошибка валидации',
            )
        ],
    )


@pytest.fixture
def processor_settings_response() -> ProcessorSettingsResponseSchema:
    return ProcessorSettingsResponseSchema(
        id=1,
        endpoint_type=ProcessorEndpointTypesEnum.SUBMIT,
        response_delay=3,
        response_code=201,
        status_mode_id=2,
        post_mode_id=1,
    )


@pytest.fixture
def processor_settings_response_list(
    processor_settings_response: ProcessorSettingsResponseSchema,
) -> list[ProcessorSettingsResponseSchema]:
    return [processor_settings_response]


@pytest.fixture
def processor_post_modes_response_list() -> list[ProcessorPostModesResponseSchema]:
    return [
        ProcessorPostModesResponseSchema(id=1, name='POST_DEFAULT', error_message=None),
        ProcessorPostModesResponseSchema(
            id=2,
            name='POST_ERROR',
            error_message=ProcessorPostValidationErrorSchema(
                validation_error=ProcessorPostErrorDetailSchema(
                    detail=[
                        ProcessorPostErrorLocationSchema(
                            loc=['body', 'order_id'],
                            msg='Эмулированная ошибка валидации отправки',
                            type='value_error.processor.mock_error_response',
                        )
                    ]
                )
            ),
        ),
    ]


@pytest.fixture
def processor_status_modes_response_list() -> list[ProcessorStatusModesResponseSchema]:
    return [
        ProcessorStatusModesResponseSchema(id=1, name='FULFILLMENT_SUCCESS'),
        ProcessorStatusModesResponseSchema(id=2, name='FULFILLMENT_FAILED'),
    ]


@pytest.fixture
def processor_status_mode_steps_response() -> ProcessorStatusModeStepsResponseSchema:
    return ProcessorStatusModeStepsResponseSchema(
        id=10,
        status_mode_id=1,
        step_order=1,
        status='Заказ получен',
        duration=30,
        error_message=None,
    )


@pytest.fixture
def processor_status_mode_steps_named_response_list() -> list[ProcessorStatusModeStepsNamedResponseSchema]:
    return [
        ProcessorStatusModeStepsNamedResponseSchema(
            id=10,
            status_mode_id=1,
            status_mode_name='FULFILLMENT_SUCCESS',
            step_order=1,
            status='Заказ получен',
            duration=30,
            error_message=None,
        )
    ]


@pytest.fixture
def setter_settings_update_request() -> BaseSettingsUpdateRequestSchema:
    return BaseSettingsUpdateRequestSchema(
        id=1,
        response_delay=2,
        response_code=202,
    )


@pytest.fixture
def setter_settings_response() -> SetterSettingsResponseSchema:
    return SetterSettingsResponseSchema(
        id=1,
        endpoint_type=SetterEndpointTypesEnum.GET_PRODUCTS,
        response_delay=2,
        response_code=202,
    )


@pytest.fixture
def setter_settings_response_list(
    setter_settings_response: SetterSettingsResponseSchema,
) -> list[SetterSettingsResponseSchema]:
    return [setter_settings_response]


@pytest.fixture
def proxy_settings_update_request() -> BaseSettingsUpdateRequestSchema:
    return BaseSettingsUpdateRequestSchema(
        id=1,
        response_delay=1,
        response_code=204,
    )


@pytest.fixture
def proxy_settings_response() -> ProxySettingsResponseSchema:
    return ProxySettingsResponseSchema(
        id=1,
        endpoint_type=ProxyEndpointTypesEnum.CAPTURE,
        response_delay=1,
        response_code=204,
    )


@pytest.fixture
def proxy_settings_response_list(
    proxy_settings_response: ProxySettingsResponseSchema,
) -> list[ProxySettingsResponseSchema]:
    return [proxy_settings_response]
