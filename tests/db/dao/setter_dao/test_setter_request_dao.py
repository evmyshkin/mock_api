from types import SimpleNamespace

import pytest

from app.api.setter.enums import SetterEntityTypeEnum
from app.db.dao.setter_dao.setter_request_dao import SetterRequestDao


class _PayloadValue:
    def __init__(self, payload):
        self._payload = payload

    def model_dump(self, exclude_unset, mode):
        assert exclude_unset is True
        assert mode == 'json'
        return self._payload


@pytest.fixture
def setter_request_dao() -> SetterRequestDao:
    return SetterRequestDao()


@pytest.mark.asyncio
class TestSetterRequestDao:
    async def test_add_entity_records(self, fake_session, setter_request_dao):
        values = SimpleNamespace(root=[_PayloadValue({'id': '1'})])

        result = await setter_request_dao.add_entity_records(
            entity_type=SetterEntityTypeEnum.PRODUCTS,
            values=values,
            is_validated=True,
        )

        assert len(result) == 1
        assert result[0].entity_type == SetterEntityTypeEnum.PRODUCTS.value
        assert result[0].payload == {'id': '1'}
        assert result[0].is_validated is True
        fake_session.add_all.assert_called_once_with(result)
        fake_session.commit.assert_awaited_once_with()

    async def test_add_entity_records_accepts_raw_dict_for_open_schema(self, fake_session, setter_request_dao):
        values = SimpleNamespace(root=[{'arbitrary': 'value'}])

        result = await setter_request_dao.add_entity_records(
            entity_type=SetterEntityTypeEnum.PRODUCTS,
            values=values,
            is_validated=False,
        )

        assert len(result) == 1
        assert result[0].payload == {'arbitrary': 'value'}
        assert result[0].is_validated is False

    async def test_find_entity_payloads(self, setter_request_dao, mocker):
        records = [SimpleNamespace(payload={'id': '1'}), SimpleNamespace(payload={'id': '2'})]
        find_all_mock = mocker.patch.object(setter_request_dao, 'find_all_ordered', return_value=records)

        result = await setter_request_dao.find_entity_payloads(entity_type=SetterEntityTypeEnum.PRODUCTS)

        assert result == [{'id': '1'}, {'id': '2'}]
        find_all_mock.assert_awaited_once_with(session=mocker.ANY, entity_type=SetterEntityTypeEnum.PRODUCTS.value)

    async def test_find_all_requests_returns_rows(self, fake_session, setter_request_dao, mocker):
        expected = [mocker.Mock(id=2), mocker.Mock(id=1)]
        execute_result = mocker.Mock()
        execute_result.scalars.return_value.all.return_value = expected
        fake_session.execute.return_value = execute_result

        result = await setter_request_dao.find_all_requests()

        assert result == expected
        fake_session.execute.assert_awaited_once()

    async def test_clear_entity_records(self, fake_session, setter_request_dao):
        fake_session.execute.return_value = SimpleNamespace(rowcount=4)

        result = await setter_request_dao.clear_entity_records(entity_type=SetterEntityTypeEnum.PRODUCTS)

        assert result.rowcount == 4
        fake_session.execute.assert_awaited_once()
        statement = str(fake_session.execute.await_args.args[0])
        assert 'DELETE FROM setter_schema.requests' in statement
        assert 'WHERE setter_schema.requests.entity_type' in statement

    async def test_clear_all_records(self, fake_session, setter_request_dao):
        fake_session.execute.return_value = SimpleNamespace(rowcount=9)

        result = await setter_request_dao.clear_all_records()

        assert result.rowcount == 9
        fake_session.execute.assert_awaited_once()
        statement = str(fake_session.execute.await_args.args[0])
        assert 'DELETE FROM setter_schema.requests' in statement
