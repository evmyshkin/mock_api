from app.db.models.base_models import BaseSettingsModel


class SetterSettingsModel(BaseSettingsModel):
    """Модель настроек эмуляции GET для витрины."""

    __tablename__ = 'settings'
    __table_args__ = {'schema': 'setter_schema'}
