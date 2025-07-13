from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from travelothai.core.config import get_settings
from travelothai.services.booking_services.BookingServiceInterface import BookingServiceInterface
from travelothai.services.booking_services.MockBookingService import MockBookingService
from travelothai.services.booking_services.DBBookingService import DBBookingService

from travelothai.schemas import booking_schema
from travelothai.models import get_session

router = APIRouter(prefix="/bookings", tags=["bookings"])


def get_booking_service(session: AsyncSession = Depends(get_session)) -> BookingServiceInterface:
    settings = get_settings()
    if settings.USE_MOCK:
        return MockBookingService()
    return DBBookingService(session=session)

# Booking endpoints
@router.get(
        "/",
        summary="List all bookings",
        description="Retrieve a list of all bookings available in the system.",
        response_model=list[booking_schema.Booking]
    )
async def read_bookings(booking_service: BookingServiceInterface = Depends(get_booking_service)) -> List[booking_schema.Booking]:
    bookings = await booking_service.list_bookings()
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found")
    return bookings

@router.get(
        "/{booking_id}",
        summary="Get a specific booking",
        description="Retrieve details of a specific booking by its ID.",
        response_model=booking_schema.Booking
    )
async def read_booking(booking_id: int, booking_service: BookingServiceInterface = Depends(get_booking_service)) -> Optional[booking_schema.Booking]:
    booking = await booking_service.get_booking(booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.post(
        "/",
        summary="Create a new booking",
        description="Create a new booking in the system.",
        response_model=booking_schema.Booking
    )
async def create_booking(booking: booking_schema.BookingCreate, booking_service: BookingServiceInterface = Depends(get_booking_service)) -> booking_schema.Booking:
    return await booking_service.create_booking(booking)

@router.put(
        "/{booking_id}/cancel",
        summary="Cancel a booking",
        description="Cancel an existing booking in the system.",
        response_model=booking_schema.Booking
    )
async def cancel_booking(booking_id: int, booking_service: BookingServiceInterface = Depends(get_booking_service)) -> booking_schema.Booking:
    canceled_booking = await booking_service.cancel_booking(booking_id)
    if canceled_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return canceled_booking


# Reschedule booking endpoint
@router.get(
        "reschedule_logs",
        summary="List all reschedule logs",
        description="Retrieve all reschedule logs.",
        response_model=List[booking_schema.BookingRescheduleLog]
    )
async def list_reschedule_logs(booking_service: BookingServiceInterface = Depends(get_booking_service)) -> List[booking_schema.BookingRescheduleLog]:
    return await booking_service.list_reschedule_logs()

@router.get(
        "/{booking_id}/reschedule_log",
        summary="Get a specific reschedule log for a booking",
        description="Retrieve a specific reschedule log by booking ID.",
        response_model=List[booking_schema.BookingRescheduleLog]
    )
async def get_reschedule_log(booking_id: int, booking_service: BookingServiceInterface = Depends(get_booking_service)) -> List[booking_schema.BookingRescheduleLog]:
    log = await booking_service.get_reschedule_log(booking_id)
    if not log:
        raise HTTPException(status_code=404, detail="No reschedule log found for this booking")
    return log

@router.post(
        "/{booking_id}/reschedule",
        summary="Reschedule a booking",
        description="Reschedule an existing booking in the system.",
        response_model=bool
    )
async def reschedule_booking(booking_id: int, new_travel_date: datetime, reason: str, booking_service: BookingServiceInterface = Depends(get_booking_service)) -> bool:
    return await booking_service.reschedule_booking(booking_id, new_travel_date, reason)
