from pydantic import ConfigDict
from pydantic import RootModel


class BaseRootSchema(RootModel):
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        validate_assignment=True,
        from_attributes=True,
    )
