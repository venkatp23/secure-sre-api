import pytest
from httpx import ASGITransport, AsyncClient
from main import app

@pytest.mark.asyncio
async def test_health_check():
    # SRE: Ensuring the health endpoint is reliable
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    
    assert response.status_code == 200
    # Note: If your /health only returns {"status": "healthy"}, 
    # make sure this line matches your actual code in main.py
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_secure_data_unauthorized():
    # Security: Ensuring the gate blocks unauthorized access
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/secure-data")
    
    # This is the "Gatekeeper" test. It MUST fail with 401 if no token is provided.
    assert response.status_code == 401