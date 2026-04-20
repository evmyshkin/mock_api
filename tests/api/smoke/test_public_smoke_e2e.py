import uuid

import pytest


@pytest.mark.asyncio
@pytest.mark.smoke
class TestPublicSmokeE2E:
    async def test_setter_processor_proxy_cycle(self, async_client):
        clear_setter_res = await async_client.delete('/setter/api/v1/clear')
        assert clear_setter_res.status_code == 200

        clear_upload_res = await async_client.delete('/proxy/api/v1/requests')
        assert clear_upload_res.status_code == 200

        health_res = await async_client.get('/healthcheck')
        assert health_res.status_code == 200
        assert health_res.json().get('info')

        setter_payload = [
            {
                'product_id': f'product-{uuid.uuid4().hex[:8]}',
                'sku': f'sku-{uuid.uuid4().hex[:8]}',
                'name': 'Smoke Product',
                'category': 'smoke-tests',
                'price': 19.99,
                'currency': 'USD',
                'quantity': 10,
            }
        ]

        setter_set_res = await async_client.post('/setter/api/v1/products/set', json=setter_payload)
        assert setter_set_res.status_code == 200

        setter_get_res = await async_client.get('/setter/api/v1/products')
        assert setter_get_res.status_code == 200
        setter_items = setter_get_res.json()['items']
        assert len(setter_items) >= 1

        order_submit_res = await async_client.post(
            '/processor/api/v1/order',
            json={
                'order_id': f'order-{uuid.uuid4().hex[:8]}',
                'customer_id': f'customer-{uuid.uuid4().hex[:8]}',
                'items': [{'sku': setter_payload[0]['sku'], 'quantity': 1, 'unit_price': 19.99}],
                'total_amount': 19.99,
                'currency': 'USD',
            },
        )
        assert order_submit_res.status_code == 200

        order_request_id = order_submit_res.json()['request_id']
        order_status_res = await async_client.get(
            '/processor/api/v1/status',
            params={'request_id': order_request_id},
        )
        assert order_status_res.status_code == 200
        assert order_status_res.json()['request_id'] == order_request_id

        upload_request_id = f'req-{uuid.uuid4().hex[:10]}'
        upload_payload = {
            'file_url': 'https://example.test/products.xlsx',
            'uploaded_by': 'smoke-suite',
        }
        upload_res = await async_client.post(
            '/proxy/api/v1/pay',
            headers={'request_id': upload_request_id},
            json=upload_payload,
        )
        assert upload_res.status_code == 200
        assert upload_res.json()['request_id'] == upload_request_id

        upload_record_res = await async_client.get(f'/proxy/api/v1/requests/{upload_request_id}')
        assert upload_record_res.status_code == 200
        assert upload_record_res.json()['body'] == upload_payload
