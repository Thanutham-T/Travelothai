from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, config


class BookingStatus(str, Enum):
    BOOKING = "booking"
    RESCHEDULED = "rescheduled"
    CANCELLED = "cancelled"


# Booking schema
class BookingBase(BaseModel):
    hotel_id: int
    user_id: int
    ticket_id: int
    travel_date: datetime
    price: float
    discount_amount: float
    final_price: float
    status: BookingStatus

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BookingBase):
    hotel_id: Optional[int] = None
    user_id: Optional[int] = None
    travel_date: Optional[datetime] = None
    price: Optional[float] = None
    discount_amount: Optional[float] = None
    final_price: Optional[float] = None
    status: Optional[BookingStatus] = None

class Booking(BookingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = config.ConfigDict(from_attributes=True)


# BookingRescheduleLog schema
class BookingRescheduleLogBase(BaseModel):
    booking_id: int
    previous_travel_date: datetime
    new_travel_date: datetime
    reason: Optional[str] = None

class BookingRescheduleLogCreate(BookingRescheduleLogBase):
    pass

class BookingRescheduleLogUpdate(BookingRescheduleLogBase):
    booking_id: Optional[int] = None
    previous_travel_date: Optional[datetime] = None
    new_travel_date: Optional[datetime] = None
    reason: Optional[str] = None

class BookingRescheduleLog(BookingRescheduleLogBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = config.ConfigDict(from_attributes=True)
