import datetime
from typing import List, Optional

from .HotelServiceInterface import HotelServiceInterface
from travelothai.schemas import hotel_schema


mock_hotels: List[hotel_schema.Hotel] = [
    hotel_schema.Hotel(id=1, name="โรงแรมกรุงเทพ", province_id=1, price=1000, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
    hotel_schema.Hotel(id=2, name="โรงแรมเชียงใหม่", province_id=2, price=1500, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
]
mock_id = 3

class MockHotelService(HotelServiceInterface):
    async def list_hotels(self) -> List[hotel_schema.Hotel]:
        return mock_hotels

    async def get_hotel(self, hotel_id: int) -> Optional[hotel_schema.Hotel]:
        for hotel in mock_hotels:
            if hotel.id == hotel_id:
                return hotel
        return None

    async def create_hotel(self, hotel: hotel_schema.HotelCreate) -> hotel_schema.Hotel:
        global mock_id
        new_hotel = hotel_schema.Hotel(
            id=mock_id,
            name=hotel.name,
            province_id=hotel.province_id,
            price=hotel.price,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        mock_hotels.append(new_hotel)
        mock_id += 1
        return new_hotel

    async def update_hotel(self, hotel_id: int, hotel: hotel_schema.HotelUpdate) -> Optional[hotel_schema.Hotel]:
        for idx, existing_hotel in enumerate(mock_hotels):
            if existing_hotel.id == hotel_id:
                updated_hotel = existing_hotel.model_copy(update=hotel.model_dump(exclude_unset=True))
                updated_hotel.updated_at = datetime.datetime.now()
                mock_hotels[idx] = updated_hotel
                return updated_hotel
        return None

    async def delete_hotel(self, hotel_id: int) -> None:
        global mock_hotels
        mock_hotels = [hotel for hotel in mock_hotels if hotel.id != hotel_id]
        return None
