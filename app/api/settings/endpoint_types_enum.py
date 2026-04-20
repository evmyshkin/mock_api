from enum import Enum


class SetterEndpointTypesEnum(Enum):
    """Типы endpoint settings для setter API."""

    GET_PRODUCTS = 'get_products'


class ProcessorEndpointTypesEnum(Enum):
    """Типы endpoint settings для processor API."""

    SUBMIT = 'submit'
    STATUS = 'status'


class ProxyEndpointTypesEnum(Enum):
    """Типы endpoint settings для proxy API."""

    CAPTURE = 'capture'
