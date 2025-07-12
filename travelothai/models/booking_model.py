from enum import Enum
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .hotel_model import Hotel
    from .ticket_model import Ticket

class BookingStatus(str, Enum):
    BOOKING = "booking"
    RESCHEDULED = "rescheduled"
    CANCELLED = "cancelled"


# Booking schema
class BookingBase(SQLModel):
    hotel_id: int = Field(foreign_key="hotel.id")
    # user_id: int = Field(foreign_key="user.id")
    user_id: int = Field(default=None)
    ticket_id: int = Field(foreign_key="ticket.id")
    travel_date: datetime = Field(default_factory=datetime.now)
    price: float = Field(gt=0)
    discount_amount: float = Field(default=0)
    final_price: float = Field(default=0)
    status: BookingStatus = Field(default=BookingStatus.BOOKING)

class Booking(BookingBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    hotel: Optional["Hotel"] = Relationship(back_populates="bookings")
    ticket: Optional["Ticket"] = Relationship(back_populates="bookings")
    reschedule_logs: list["BookingRescheduleLog"] = Relationship(back_populates="booking")


# BookingRescheduleLog schema
class BookingRescheduleLogBase(SQLModel):
    booking_id: int = Field(foreign_key="booking.id")
    previous_travel_date: datetime = Field(default_factory=datetime.now)
    new_travel_date: datetime = Field(default_factory=datetime.now)
    reason: Optional[str] = Field(default=None)

class BookingRescheduleLog(BookingRescheduleLogBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    booking: Optional["Booking"] = Relationship(back_populates="reschedule_logs")
