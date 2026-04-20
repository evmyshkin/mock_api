import pytest

from app.db.dao.processor_dao.processor_status_modes_dao import ProcessorStatusModesDao


@pytest.fixture
def processor_status_modes_dao() -> ProcessorStatusModesDao:
    return ProcessorStatusModesDao()


@pytest.mark.asyncio
class TestProcessorStatusModesDao:
    async def test_find_all_status_modes_proxies_to_find_all_ordered(self, processor_status_modes_dao, mocker):
        expected = [object()]
        find_all_mock = mocker.patch.object(
            processor_status_modes_dao,
            'find_all_ordered',
            return_value=expected,
        )

        result = await processor_status_modes_dao.find_all_status_modes()

        assert result == expected
        find_all_mock.assert_awaited_once_with(session=mocker.ANY)
