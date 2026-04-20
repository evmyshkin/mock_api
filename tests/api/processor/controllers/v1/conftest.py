import pytest

from app.api.processor.schemas.requests.processor_submit_request_schema import OrderLineItemSchema
from app.api.processor.schemas.requests.processor_submit_request_schema import ProcessorSubmitRequestSchema
from app.api.processor.schemas.responses.processor_request_response_schema import ProcessorRequestResponseSchema
from app.api.processor.schemas.responses.processor_status_response_schema import ProcessorStatusResponseSchema
from app.api.processor.schemas.responses.processor_submit_response_schema import ProcessorSubmitResponseSchema


@pytest.fixture
def order_submit_request() -> ProcessorSubmitRequestSchema:
    return ProcessorSubmitRequestSchema(
        order_id='order-1',
        customer_id='customer-1',
        items=[OrderLineItemSchema(sku='SKU-1', quantity=2, unit_price=15.5)],
        total_amount=31.0,
        currency='USD',
    )


@pytest.fixture
def order_submit_response() -> ProcessorSubmitResponseSchema:
    return ProcessorSubmitResponseSchema(
        request_id='req-1',
        order_id='order-1',
        status='Заказ получен',
        unixtimestamp=1710000000,
        error_message=None,
    )


@pytest.fixture
def order_status_response() -> ProcessorStatusResponseSchema:
    return ProcessorStatusResponseSchema(
        request_id='req-1',
        order_id='order-1',
        status='Упаковка',
        unixtimestamp=1710000000,
        error_message=None,
    )


@pytest.fixture
def order_request_response() -> ProcessorRequestResponseSchema:
    return ProcessorRequestResponseSchema(
        id=1,
        request_id='req-1',
        endpoint_type='submit',
        order_id='order-1',
        customer_id='customer-1',
        response_delay=2,
        response_code=202,
        post_mode_id=1,
        status_mode_id=1,
        status_step_id=11,
        status_change_after=None,
        unixtimestamp=1710000000,
        payload={
            'order_id': 'order-1',
            'customer_id': 'customer-1',
            'items': [{'sku': 'SKU-1', 'quantity': 2, 'unit_price': 15.5}],
            'total_amount': 31.0,
            'currency': 'USD',
        },
        created='2026-04-19T10:00:00Z',
        updated='2026-04-19T10:00:00Z',
    )
