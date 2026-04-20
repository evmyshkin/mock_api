import uuid

import pytest


@pytest.fixture
def fixed_upload_payload() -> dict[str, str]:
    return {'url': 'https://s3.example.com/file.xlsx'}


@pytest.fixture
def random_request_id() -> str:
    return uuid.uuid4().hex


@pytest.fixture
def fixed_auth_header() -> str:
    return 'Bearer 123'
