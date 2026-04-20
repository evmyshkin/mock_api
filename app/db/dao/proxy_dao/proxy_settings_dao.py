from app.db.dao.settings_dao import SettingsDao
from app.db.models.proxy_schema.proxy_settings_model import ProxySettingsModel


class ProxySettingsDao(SettingsDao):
    """DAO для настроек эндпоинтов загрузки товаров."""

    model = ProxySettingsModel
