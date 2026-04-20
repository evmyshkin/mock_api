from app.db.models.base_models import BaseSettingsModel


class ProxySettingsModel(BaseSettingsModel):
    """Модель таблицы настроек эмуляции ответа эндпоинта загрузки товаров."""

    __tablename__ = 'settings'
    __table_args__ = {'schema': 'proxy_schema'}
