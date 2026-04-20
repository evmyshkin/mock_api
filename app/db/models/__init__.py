# Добавлять сюда новые таблицы для миграций

# схема processor
# схема proxy
from app.db.models.processor_schema.processor_post_mode_model import ProcessorPostModesModel as ProcessorPostModesModel
from app.db.models.processor_schema.processor_request_model import ProcessorRequestModel as ProcessorRequestModel
from app.db.models.processor_schema.processor_settings_model import ProcessorSettingsModel as ProcessorSettingsModel
from app.db.models.processor_schema.processor_status_mode_models import (
    ProcessorStatusModesModel as ProcessorStatusModesModel,
)
from app.db.models.processor_schema.processor_status_mode_models import (
    ProcessorStatusModeStepsModel as ProcessorStatusModeStepsModel,
)
from app.db.models.proxy_schema.proxy_request_model import ProxyRequestModel as ProxyRequestModel
from app.db.models.proxy_schema.proxy_settings_model import ProxySettingsModel as ProxySettingsModel

# схема setter
from app.db.models.setter_schema.setter_request_model import SetterRequestModel as SetterRequestModel
from app.db.models.setter_schema.setter_settings_model import SetterSettingsModel as SetterSettingsModel
