from typing import List, Optional
from fastapi import HTTPException

from .HotelServiceInterface import HotelServiceInterface
from travelothai.schemas import hotel_schema
from travelothai.models import hotel_model, province_model

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class DBHotelService(HotelServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_hotels(self) -> List[hotel_schema.Hotel]:
        result = await self.session.exec(select(hotel_model.Hotel))
        if not result:
            raise HTTPException(status_code=404, detail="No hotels found")
        hotels = result.scalars().all()
        return hotels

    async def get_hotel(self, hotel_id: int) -> Optional[hotel_schema.Hotel]:
        result = await self.session.exec(
            select(hotel_model.Hotel).where(hotel_model.Hotel.id == hotel_id)
            )
        if not result:
            raise HTTPException(status_code=404, detail="Hotel not found")
        hotel = result.scalar()
        return hotel

    async def create_hotel(self, hotel: hotel_schema.HotelCreate) -> hotel_schema.Hotel:
        # Validate that the province exists before creating the hotel
        if not hotel.province_id:
            raise HTTPException(status_code=400, detail="Province ID must be provided for hotel creation.")
        db_province = await self.session.get(province_model.Province, hotel.province_id)
        if not db_province:
            raise HTTPException(status_code=404, detail=f"Province with ID {hotel.province_id} does not exist.")

        # Create the hotel    
        db_hotel = hotel_model.Hotel(**hotel.model_dump())
        self.session.add(db_hotel)
        await self.session.commit()
        await self.session.refresh(db_hotel)
        return db_hotel


    async def update_hotel(self, hotel_id: int, hotel: hotel_schema.HotelUpdate) -> Optional[hotel_schema.Hotel]:
        # Validate that the hotel exists before updating
        db_hotel = await self.session.get(hotel_model.Hotel, hotel_id)
        if not db_hotel:
            return HTTPException(status_code=404, detail="Hotel not found")
        if not hotel.province_id:
            raise HTTPException(status_code=400, detail="Province ID must be provided for hotel creation.")
        db_province = await self.session.get(province_model.Province, hotel.province_id)
        if not db_province:
            raise HTTPException(status_code=404, detail=f"Province with ID {hotel.province_id} does not exist.")
        
        # Update the hotel details
        update_data = hotel.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_hotel, key, value)
        self.session.add(db_hotel)
        await self.session.commit()
        await self.session.refresh(db_hotel)
        return db_hotel
    

    async def delete_hotel(self, hotel_id: int) -> None:
        # Validate that the hotel exists before deleting
        if not hotel_id:
            raise HTTPException(status_code=400, detail="Hotel ID must be provided for deletion.")
        if not await self.get_hotel(hotel_id):
            raise HTTPException(status_code=404, detail="Hotel not found")
        
        # Delete the hotel
        db_hotel = await self.session.get(hotel_model.Hotel, hotel_id)
        if db_hotel:
            await self.session.delete(db_hotel)
            await self.session.commit()
