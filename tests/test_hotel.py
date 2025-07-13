import pytest
from fastapi import status

from travelothai.main import app
from travelothai.models import get_session, province_model

from base import session, engine, client

# ------------------------ Fixtures ------------------------
@pytest.fixture
async def hotel_data(session):
    category = province_model.ProvinceCategory(id=1, name="Test Category")
    province = province_model.Province(id=1, name="Test Province", category_id=1)
    session.add(category)
    session.add(province)
    await session.commit()

    return {"name": "Test Hotel", "province_id": 1, "price": 1000}


# ------------------------ Tests ------------------------
@pytest.mark.asyncio
async def test_create_hotel(client, hotel_data):
    response = await client.post("/v1/hotels/", json=hotel_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == hotel_data["name"]
    assert data["province_id"] == hotel_data["province_id"]
    assert data["price"] == hotel_data["price"]

@pytest.mark.asyncio
async def test_update_hotel(client, hotel_data):
    create_response = await client.post("/v1/hotels/", json=hotel_data)
    hotel_id = create_response.json()["id"]
    updated_data = {"name": "Updated Hotel", "province_id": 1, "price": 1500}
    response = await client.put(f"/v1/hotels/{hotel_id}", json=updated_data)  # ← แก้ตรงนี้
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Hotel"
    assert response.json()["price"] == 1500

@pytest.mark.asyncio
async def test_get_hotel(client, hotel_data):
    create_response = await client.post("/v1/hotels/", json=hotel_data)
    hotel_id = create_response.json()["id"]
    response = await client.get(f"/v1/hotels/{hotel_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == hotel_id
    assert data["name"] == hotel_data["name"]
    assert data["province_id"] == hotel_data["province_id"]
    assert data["price"] == hotel_data["price"]

@pytest.mark.asyncio
async def test_get_nonexistent_hotel(client):
    response = await client.get("/v1/hotels/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Hotel not found"}

@pytest.mark.asyncio
async def test_delete_hotel(client, hotel_data):
    create_response = await client.post("/v1/hotels/", json=hotel_data)
    hotel_id = create_response.json()["id"]
    response = await client.delete(f"/v1/hotels/{hotel_id}")
    assert response.status_code == 204

    # Verify deletion
    get_response = await client.get(f"/v1/hotels/{hotel_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Hotel not found"}    
