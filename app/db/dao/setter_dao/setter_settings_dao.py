from app.db.dao.settings_dao import SettingsDao
from app.db.models.setter_schema.setter_settings_model import SetterSettingsModel


class SetterSettingsDao(SettingsDao):
    """DAO для настроек соединения эндпоинтов витрины."""

    model = SetterSettingsModel
