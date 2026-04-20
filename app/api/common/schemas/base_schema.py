from pydantic import BaseModel
from pydantic import ConfigDict


class BaseSchema(BaseModel):
    # Конфиги для всех схем
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        validate_assignment=True,
        from_attributes=True,
    )

    @classmethod
    def get_field_names(cls) -> set[str]:
        """Получить список названий полей у валидационной схемы.

        Returns:
            set[str]: Возвращает alias'ы полей, если они заданы, иначе имена полей Python
        """
        field_names = set()
        for name, field in cls.model_fields.items():
            # Используем alias, если он задан, иначе имя поля Python
            field_name = field.alias if field.alias else name
            field_names.add(field_name)
        return field_names
