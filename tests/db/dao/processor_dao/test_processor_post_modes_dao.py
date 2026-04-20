import pytest

from app.db.dao.processor_dao.processor_post_modes_dao import ProcessorPostModesDao


@pytest.fixture
def processor_post_modes_dao() -> ProcessorPostModesDao:
    return ProcessorPostModesDao()


@pytest.mark.asyncio
class TestProcessorPostModesDao:
    async def test_find_all_post_modes_proxies_to_find_all_ordered(self, processor_post_modes_dao, mocker):
        expected = [object()]
        find_all_mock = mocker.patch.object(
            processor_post_modes_dao,
            'find_all_ordered',
            return_value=expected,
        )

        result = await processor_post_modes_dao.find_all_post_modes()

        assert result == expected
        find_all_mock.assert_awaited_once_with(session=mocker.ANY)
