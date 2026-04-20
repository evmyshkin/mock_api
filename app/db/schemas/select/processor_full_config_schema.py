from app.api.common.schemas.base_schema import BaseSchema
from app.db.schemas.select.processor_post_modes_schema import ProcessorPostModesSchema
from app.db.schemas.select.processor_settings_schema import ProcessorSettingsSchema
from app.db.schemas.select.processor_status_mode_steps_schema import ProcessorStatusModeStepsSchema
from app.db.schemas.select.processor_status_modes_schema import ProcessorStatusModesSchema


class FullProcessorConfigSchema(BaseSchema):
    settings: ProcessorSettingsSchema
    status_modes: ProcessorStatusModesSchema
    status_mode_steps: ProcessorStatusModeStepsSchema
    post_modes: ProcessorPostModesSchema
    status_mode_len: int
