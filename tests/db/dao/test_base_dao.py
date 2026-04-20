from datetime import UTC
from datetime import datetime

import pytest

from app.db.dao.base_dao import BaseDAO
from app.db.models.setter_schema.setter_settings_model import SetterSettingsModel


class DummyBaseDao(BaseDAO):
    model = SetterSettingsModel


@pytest.fixture
def dummy_base_dao() -> DummyBaseDao:
    return DummyBaseDao()


@pytest.mark.asyncio
class TestBaseDao:
    async def test_add_one_returns_new_object(self, fake_session, dummy_base_dao):
        result = await dummy_base_dao.add_one(endpoint_type='endpoint_1', response_delay=1, response_code=200)

        assert isinstance(result, SetterSettingsModel)
        assert result.endpoint_type == 'endpoint_1'
        fake_session.add.assert_called_once_with(result)
        fake_session.commit.assert_awaited_once_with()
        fake_session.close.assert_awaited_once_with()

    async def test_add_one_rolls_back_on_commit_error(self, fake_session, dummy_base_dao, mocker):
        fake_session.commit = mocker.AsyncMock(side_effect=RuntimeError('ошибка БД'))

        with pytest.raises(RuntimeError, match='ошибка БД'):
            await dummy_base_dao.add_one(endpoint_type='endpoint_1', response_delay=1, response_code=200)

        fake_session.rollback.assert_awaited_once_with()
        fake_session.close.assert_awaited_once_with()

    async def test_add_many_returns_new_objects(self, fake_session, dummy_base_dao):
        result = await dummy_base_dao.add_many(
            instances=[
                {'endpoint_type': 'endpoint_1', 'response_delay': 1, 'response_code': 200},
                {'endpoint_type': 'endpoint_2', 'response_delay': 2, 'response_code': 201},
            ]
        )

        assert len(result) == 2
        assert all(isinstance(item, SetterSettingsModel) for item in result)
        fake_session.add_all.assert_called_once_with(result)
        fake_session.commit.assert_awaited_once_with()

    async def test_add_many_rolls_back_on_commit_error(self, fake_session, dummy_base_dao, mocker):
        fake_session.commit = mocker.AsyncMock(side_effect=RuntimeError('ошибка БД'))

        with pytest.raises(RuntimeError, match='ошибка БД'):
            await dummy_base_dao.add_many(
                instances=[{'endpoint_type': 'endpoint_1', 'response_delay': 1, 'response_code': 200}]
            )

        fake_session.rollback.assert_awaited_once_with()

    async def test_find_one_or_none_returns_record(self, fake_session, dummy_base_dao, mocker):
        record = object()
        execute_result = mocker.MagicMock()
        execute_result.scalar_one_or_none.return_value = record
        fake_session.execute.return_value = execute_result

        result = await dummy_base_dao.find_one_or_none(endpoint_type='endpoint_1')

        assert result is record
        fake_session.execute.assert_awaited_once()

    async def test_find_one_or_none_by_id_returns_record(self, fake_session, dummy_base_dao, mocker):
        record = object()
        execute_result = mocker.MagicMock()
        execute_result.scalar_one_or_none.return_value = record
        fake_session.execute.return_value = execute_result

        result = await dummy_base_dao.find_one_or_none_by_id(data_id=11)

        assert result is record
        fake_session.execute.assert_awaited_once()

    async def test_find_all_ordered_returns_records(self, fake_session, dummy_base_dao, mocker):
        records = [object(), object()]
        execute_result = mocker.MagicMock()
        execute_result.scalars.return_value.all.return_value = records
        fake_session.execute.return_value = execute_result

        result = await dummy_base_dao.find_all_ordered(endpoint_type='endpoint_1')

        assert result == records
        fake_session.execute.assert_awaited_once()

    async def test_update_records_executes_and_commits(self, fake_session, dummy_base_dao):
        await dummy_base_dao.update_records(
            filter_by={'endpoint_type': 'endpoint_1'},
            values={'response_code': 429},
        )

        fake_session.execute.assert_awaited_once()
        fake_session.commit.assert_awaited_once_with()

    async def test_update_one_or_none_returns_updated_record(self, fake_session, dummy_base_dao, mocker):
        record = object()
        execute_result = mocker.MagicMock()
        execute_result.scalar_one_or_none.return_value = record
        fake_session.execute.return_value = execute_result

        result = await dummy_base_dao.update_one_or_none(
            filter_by={'endpoint_type': 'endpoint_1'},
            values={'response_code': 429},
        )

        assert result is record
        fake_session.execute.assert_awaited_once()
        fake_session.commit.assert_awaited_once_with()

    async def test_clear_old_data_returns_execute_result(self, fake_session, dummy_base_dao):
        execute_result = object()
        fake_session.execute.return_value = execute_result
        cutoff = datetime(2025, 1, 1, tzinfo=UTC)

        result = await dummy_base_dao.clear_old_data(cutoff=cutoff)

        assert result is execute_result
        fake_session.execute.assert_awaited_once()
        fake_session.commit.assert_awaited_once_with()
