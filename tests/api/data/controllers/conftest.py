from datetime import datetime

import pytest

from app.api.setter.schemas.setter_data_response_schema import SetterDataResponseSchema


@pytest.fixture
def setter_data_response_item() -> SetterDataResponseSchema:
    timestamp = datetime.fromisoformat('2025-10-01T17:26:16+03:00')
    return SetterDataResponseSchema(
        id=1,
        entity_type='products',
        is_validated=True,
        payload={'eventid': '1'},
        created=timestamp,
        updated=timestamp,
    )


@pytest.fixture
def setter_data_response_list(
    setter_data_response_item: SetterDataResponseSchema,
) -> list[SetterDataResponseSchema]:
    return [setter_data_response_item]
