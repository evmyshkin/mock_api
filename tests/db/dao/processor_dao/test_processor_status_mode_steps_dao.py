import pytest

from app.db.dao.processor_dao.processor_status_mode_steps_dao import ProcessorStatusModeStepsDao


@pytest.fixture
def processor_status_mode_steps_dao() -> ProcessorStatusModeStepsDao:
    return ProcessorStatusModeStepsDao()


@pytest.mark.asyncio
class TestProcessorStatusModeStepsDao:
    async def test_find_all_status_mode_steps_returns_rows(
        self,
        fake_session,
        processor_status_mode_steps_dao,
        mocker,
    ):
        expected = [{'id': 1}]
        execute_result = mocker.MagicMock()
        execute_result.scalars.return_value.all.return_value = expected
        fake_session.execute.return_value = execute_result

        result = await processor_status_mode_steps_dao.find_all_status_mode_steps()

        assert result == expected
        fake_session.execute.assert_awaited_once()

    async def test_update_status_mode_step_proxies_to_update_one_or_none(self, processor_status_mode_steps_dao, mocker):
        expected = object()
        update_mock = mocker.patch.object(
            processor_status_mode_steps_dao,
            'update_one_or_none',
            return_value=expected,
        )

        result = await processor_status_mode_steps_dao.update_status_mode_step(step_id=10, values={'duration': 30})

        assert result is expected
        update_mock.assert_awaited_once_with(session=mocker.ANY, filter_by={'id': 10}, values={'duration': 30})
