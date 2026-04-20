from __future__ import annotations

import asyncio
import logging
import os
import uuid

import httpx

BASE_URL = os.getenv('MOCK_API_BASE_URL', 'http://localhost:8000')
logger = logging.getLogger(__name__)


async def main() -> None:
    """Run a minimal end-to-end interaction against local mock_api."""
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15) as client:
        health = await client.get('/healthcheck')
        health.raise_for_status()
        logger.info('[healthcheck] %s', health.json())

        storefront_set = await client.post(
            '/api/v1/products/set',
            json=[
                {
                    'product_id': 'product-1',
                    'sku': 'sku-001',
                    'name': 'Demo Product',
                    'category': 'electronics',
                    'price': 10.5,
                    'currency': 'USD',
                    'quantity': 5,
                }
            ],
        )
        storefront_set.raise_for_status()
        logger.info('[storefront:set] %s', storefront_set.json())

        storefront_get = await client.get('/api/v1/products')
        storefront_get.raise_for_status()
        logger.info('[storefront:get] %s', storefront_get.json())

        submit = await client.post(
            '/api/v1/order-processing/submit',
            json={
                'order_id': 'order-1001',
                'customer_id': 'customer-42',
                'items': [
                    {
                        'sku': 'sku-001',
                        'quantity': 1,
                        'unit_price': 10.5,
                    }
                ],
                'total_amount': 10.5,
                'currency': 'USD',
            },
        )
        submit.raise_for_status()
        submit_data = submit.json()
        request_id = submit_data['request_id']
        logger.info('[order-processing:submit] %s', submit_data)

        await asyncio.sleep(6)

        status = await client.get('/api/v1/order-processing/status', params={'request_id': request_id})
        status.raise_for_status()
        logger.info('[order-processing:status] %s', status.json())

        upload_request_id = str(uuid.uuid4())
        upload = await client.post(
            '/api/v1/product-upload',
            headers={'request_id': upload_request_id},
            json={
                'file_url': 'https://example.test/products.xlsx',
                'uploaded_by': 'integration-test',
            },
        )
        upload.raise_for_status()
        logger.info('[product-upload:capture] %s', upload.json())

        upload_record = await client.get(f'/api/v1/product-upload/records/{upload_request_id}')
        upload_record.raise_for_status()
        logger.info('[product-upload:get-by-id] %s', upload_record.json())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
