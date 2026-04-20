import pytest


@pytest.mark.asyncio
class TestHealthCheck:
    async def test_healthcheck(self, async_client):
        r = await async_client.get('/healthcheck')
        assert r.status_code == 200
        data = r.json()
        assert data.get('info') == 'сервис работает'

    async def test_metrics(self, async_client):
        r = await async_client.get('/metrics')
        assert r.status_code == 200
        assert r.headers.get('content-type', '').startswith('text/plain')
