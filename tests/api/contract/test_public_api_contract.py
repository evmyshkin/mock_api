from json import loads
from pathlib import Path

import pytest

from app.main import fastapi_app

EXPECTED_PUBLIC_PATHS: dict[str, set[str]] = {
    '/setter/api/v1/products/set': {'post'},
    '/setter/api/v1/products/set-open': {'post'},
    '/setter/api/v1/products': {'get', 'delete'},
    '/setter/api/v1/clear': {'delete'},
    '/setter/api/v1/requests': {'get'},
    '/processor/api/v1/order': {'post'},
    '/processor/api/v1/requests': {'get'},
    '/processor/api/v1/status': {'get'},
    '/proxy/api/v1/pay': {'post'},
    '/proxy/api/v1/requests': {'get', 'delete'},
    '/proxy/api/v1/requests/{request_id}': {'get'},
    '/setter/settings': {'get', 'put'},
    '/processor/settings': {'get', 'put'},
    '/processor/settings/post-modes': {'get'},
    '/processor/settings/status-modes': {'get'},
    '/processor/settings/status-mode-steps': {'get', 'put'},
    '/proxy/settings': {'get', 'put'},
    '/healthcheck': {'get'},
}


@pytest.mark.contract
def test_openapi_paths_match_expected_public_contract() -> None:
    openapi = fastapi_app.openapi()
    paths: dict[str, dict] = openapi['paths']

    actual = {path: set(operations.keys()) for path, operations in paths.items()}

    assert actual == EXPECTED_PUBLIC_PATHS


@pytest.mark.contract
def test_openapi_does_not_publish_legacy_routes_or_metrics() -> None:
    paths = fastapi_app.openapi()['paths']

    assert '/api/v1/orders' not in paths
    assert '/api/v1/customers' not in paths
    assert '/data/ord' not in paths
    assert '/setter/data/requests' not in paths
    assert '/metrics' not in paths


@pytest.mark.contract
def test_versioned_openapi_snapshot_is_up_to_date() -> None:
    snapshot_path = Path('docs/openapi/openapi.v1.json')
    expected = loads(snapshot_path.read_text(encoding='utf-8'))
    actual = fastapi_app.openapi()

    assert actual == expected
