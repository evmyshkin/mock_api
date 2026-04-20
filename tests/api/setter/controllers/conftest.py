import pytest

from app.api.setter.schemas.v1.setter_products_schema import ProductItemSchema
from app.api.setter.schemas.v1.setter_products_schema import ProductsSetOpenRequestSchema
from app.api.setter.schemas.v1.setter_products_schema import ProductsSetRequestSchema


@pytest.fixture
def product_strict_request() -> ProductsSetRequestSchema:
    return ProductsSetRequestSchema(
        root=[
            ProductItemSchema(
                product_id='prod-1',
                sku='TSHIRT-001',
                name='Classic T-Shirt',
                category='tops',
                price=29.9,
                currency='USD',
                quantity=25,
            )
        ]
    )


@pytest.fixture
def product_open_request() -> ProductsSetOpenRequestSchema:
    return ProductsSetOpenRequestSchema(
        root=[
            {
                'arbitrary_key': 42,
                'nested': {'size': 'M'},
                'color': 'black',
                'quantity': 25,
            }
        ]
    )
