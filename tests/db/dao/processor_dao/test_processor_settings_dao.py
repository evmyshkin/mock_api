import pytest

from app.api.settings.endpoint_types_enum import ProcessorEndpointTypesEnum
from app.db.dao.processor_dao.processor_settings_dao import ProcessorSettingsDao
from app.db.schemas.select.processor_full_config_schema import FullProcessorConfigSchema


def _full_config_payload():
    return {
        'settings': {
            'endpoint_type': ProcessorEndpointTypesEnum.SUBMIT.value,
            'response_delay': 2,
            'response_code': 200,
            'status_mode_id': 10,
            'post_mode_id': 20,
        },
        'status_modes': {'id': 10, 'name': 'FULFILLMENT_SUCCESS'},
        'status_mode_steps': {
            'id': 100,
            'status_mode_id': 10,
            'step_order': 1,
            'status': 'Заказ получен',
            'duration': 5,
            'error_message': None,
        },
        'post_modes': {'id': 20, 'name': 'POST_DEFAULT', 'error_message': None},
        'status_mode_len': 3,
    }


@pytest.fixture
def processor_settings_dao() -> ProcessorSettingsDao:
    return ProcessorSettingsDao()


@pytest.mark.asyncio
class TestProcessorSettingsDao:
    async def test_get_endpoint_settings_returns_record(self, processor_settings_dao, mocker):
        expected = object()
        find_one_mock = mocker.patch.object(processor_settings_dao, 'find_one_or_none', return_value=expected)

        result = await processor_settings_dao.get_endpoint_settings(
            endpoint_type=ProcessorEndpointTypesEnum.SUBMIT,
        )

        assert result is expected
        find_one_mock.assert_awaited_once_with(
            session=mocker.ANY,
            endpoint_type=ProcessorEndpointTypesEnum.SUBMIT.value,
        )

    async def test_get_endpoint_settings_raises_when_missing(self, processor_settings_dao, mocker):
        mocker.patch.object(processor_settings_dao, 'find_one_or_none', return_value=None)

        with pytest.raises(ValueError, match=ProcessorEndpointTypesEnum.SUBMIT.value):
            await processor_settings_dao.get_endpoint_settings(
                endpoint_type=ProcessorEndpointTypesEnum.SUBMIT,
            )

    async def test_get_endpoint_full_config_returns_validated_schema(
        self,
        fake_session,
        processor_settings_dao,
        mocker,
    ):
        payload = _full_config_payload()
        execute_result = mocker.MagicMock()
        execute_result.scalar_one_or_none.return_value = payload
        fake_session.execute.return_value = execute_result

        result = await processor_settings_dao.get_endpoint_full_config(
            endpoint_type=ProcessorEndpointTypesEnum.SUBMIT,
        )

        assert isinstance(result, FullProcessorConfigSchema)
        assert result.settings.endpoint_type == ProcessorEndpointTypesEnum.SUBMIT.value
        fake_session.execute.assert_awaited_once()

    async def test_get_endpoint_full_config_raises_when_not_found(self, fake_session, processor_settings_dao, mocker):
        execute_result = mocker.MagicMock()
        execute_result.scalar_one_or_none.return_value = None
        fake_session.execute.return_value = execute_result

        with pytest.raises(ValueError, match=ProcessorEndpointTypesEnum.SUBMIT.value):
            await processor_settings_dao.get_endpoint_full_config(
                endpoint_type=ProcessorEndpointTypesEnum.SUBMIT,
            )

    async def test_advance_status_steps_returns_rows(self, fake_session, processor_settings_dao):
        db_rows = [('req-1', 'order-1', 'Упаковка')]
        fake_session.execute.return_value = db_rows

        result = await processor_settings_dao.advance_status_steps()

        assert result == db_rows
        fake_session.execute.assert_awaited_once()
        fake_session.commit.assert_awaited_once_with()

    async def test_find_all_settings_proxies_to_find_all_ordered(self, processor_settings_dao, mocker):
        expected = [object()]
        find_all_mock = mocker.patch.object(processor_settings_dao, 'find_all_ordered', return_value=expected)

        result = await processor_settings_dao.find_all_settings()

        assert result == expected
        find_all_mock.assert_awaited_once_with(session=mocker.ANY)

    async def test_update_endpoint_settings_proxies_to_update_one_or_none(self, processor_settings_dao, mocker):
        expected = object()
        values = {'response_code': 429}
        update_mock = mocker.patch.object(processor_settings_dao, 'update_one_or_none', return_value=expected)

        result = await processor_settings_dao.update_endpoint_settings(setting_id=7, values=values)

        assert result is expected
        update_mock.assert_awaited_once_with(session=mocker.ANY, filter_by={'id': 7}, values=values)
