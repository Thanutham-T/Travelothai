from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from travelothai.core.config import get_settings
from travelothai.services.hotel_services.HotelServiceInterface import HotelServiceInterface
from travelothai.services.hotel_services.MockHotelService import MockHotelService
from travelothai.services.hotel_services.DBHotelService import DBHotelService

from travelothai.schemas import hotel_schema
from travelothai.models import get_session

router = APIRouter(prefix="/hotels", tags=["hotels"])


def get_hotel_service(session: AsyncSession = Depends(get_session)) -> HotelServiceInterface:
    settings = get_settings()
    if settings.USE_MOCK:
        return MockHotelService()
    return DBHotelService(session=session)

@router.get(
        "/",
        summary="List all hotels",
        description="Retrieve a list of all hotels available in the system.",
        response_model=list[hotel_schema.Hotel]
    )
async def read_hotels(hotel_service: HotelServiceInterface = Depends(get_hotel_service)) -> List[hotel_schema.Hotel]:
    hotels = await hotel_service.list_hotels()
    if not hotels:
        raise HTTPException(status_code=404, detail="No hotels found")
    return hotels

@router.get(
        "/{hotel_id}",
        summary="Get a specific hotel",
        description="Retrieve details of a specific hotel by its ID.",
        response_model=hotel_schema.Hotel
    )
async def read_hotel(hotel_id: int, hotel_service: HotelServiceInterface = Depends(get_hotel_service)) -> Optional[hotel_schema.Hotel]:
    hotel = await hotel_service.get_hotel(hotel_id)
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel

@router.post(
        "/",
        summary="Create a new hotel",
        description="Create a new hotel in the system.",
        response_model=hotel_schema.Hotel
    )
async def create_hotel(hotel: hotel_schema.HotelCreate, hotel_service: HotelServiceInterface = Depends(get_hotel_service)) -> hotel_schema.Hotel:
    return await hotel_service.create_hotel(hotel)

@router.put(
        "/{hotel_id}",
        summary="Update a hotel",
        description="Update an existing hotel in the system.",
        response_model=hotel_schema.Hotel
    )
async def update_hotel(hotel_id: int, hotel: hotel_schema.HotelUpdate, hotel_service: HotelServiceInterface = Depends(get_hotel_service)) -> Optional[hotel_schema.Hotel]:
    updated_hotel = await hotel_service.update_hotel(hotel_id, hotel)
    if updated_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return updated_hotel

@router.delete(
        "/{hotel_id}",
        summary="Delete a hotel",
        description="Delete a hotel from the system.",
        response_model=None
    )
async def delete_hotel(hotel_id: int, hotel_service: HotelServiceInterface = Depends(get_hotel_service)) -> None:
    hotel = await hotel_service.get_hotel(hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    await hotel_service.delete_hotel(hotel_id)
    return Response(status_code=204, content=None)
