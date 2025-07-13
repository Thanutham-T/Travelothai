from abc import ABC, abstractmethod
import datetime
from typing import List, Optional

from travelothai.schemas import booking_schema


class BookingServiceInterface(ABC):
    # Booking service interface
    @abstractmethod
    async def list_bookings(self) -> List[booking_schema.Booking]:
        """List all bookings."""
        pass

    @abstractmethod
    async def get_booking(self, booking_id: int) -> Optional[booking_schema.Booking]:
        """Get a specific booking by ID."""
        pass

    @abstractmethod
    async def create_booking(self, booking: booking_schema.BookingCreate) -> booking_schema.Booking:
        """Create a new booking."""
        pass

    @abstractmethod
    async def cancel_booking(self, booking_id: int) -> Optional[booking_schema.Booking]:
        """Cancel an existing booking."""
        pass

    # BookingReschedule
    @abstractmethod
    async def reschedule_booking(self, booking_id: int, new_travel_date: datetime.datetime, reason: str) -> Optional[booking_schema.BookingRescheduleLog]:
        """Reschedule an existing booking."""
        pass

    @abstractmethod
    async def list_reschedule_logs(self) -> List[booking_schema.BookingRescheduleLog]:
        """List reschedule logs for a specific booking."""
        pass

    @abstractmethod
    async def get_reschedule_log(self, booking_id: int) -> List[booking_schema.BookingRescheduleLog]:
        """Get a specific reschedule log by booking ID."""
        pass