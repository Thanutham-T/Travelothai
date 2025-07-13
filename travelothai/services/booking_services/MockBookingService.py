import datetime
from typing import List, Optional

from .BookingServiceInterface import BookingServiceInterface
from travelothai.schemas import booking_schema


mock_bookings: List[booking_schema.Booking] = [
    booking_schema.Booking(id=1, hotel_id=1, user_id=1, ticket_id=1, travel_date=datetime.datetime.now(), price=1000, discount_amount=0, final_price=1000, status=booking_schema.BookingStatus.BOOKING, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
    booking_schema.Booking(id=2, hotel_id=2, user_id=2, ticket_id=2, travel_date=datetime.datetime.now(), price=1500, discount_amount=0, final_price=1500, status=booking_schema.BookingStatus.BOOKING, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
]
mock_reschedule_logs: List[booking_schema.BookingRescheduleLog] = [
    booking_schema.BookingRescheduleLog(
        id=1,
        booking_id=1,
        previous_travel_date=datetime.datetime.now(),
        new_travel_date=datetime.datetime.now() + datetime.timedelta(days=1),
        reason="Change of plans",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    ),
    booking_schema.BookingRescheduleLog(
        id=2,
        booking_id=1,
        previous_travel_date=datetime.datetime.now(),
        new_travel_date=datetime.datetime.now() + datetime.timedelta(days=2),
        reason="Flight delay",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    ),
]

mock_id = 3
mock_reschedule_logs_id = 3


class MockBookingService(BookingServiceInterface):
    async def list_bookings(self) -> List[booking_schema.Booking]:
        return mock_bookings

    async def get_booking(self, booking_id: int) -> Optional[booking_schema.Booking]:
        for booking in mock_bookings:
            if booking.id == booking_id:
                return booking
        return None

    async def create_booking(self, booking: booking_schema.BookingCreate) -> booking_schema.Booking:
        global mock_id
        new_booking = booking_schema.Booking(
            id=mock_id,
            hotel_id=booking.hotel_id,
            user_id=booking.user_id,
            ticket_id=booking.ticket_id,
            travel_date=booking.travel_date,
            price=booking.price,
            discount_amount=booking.discount_amount,
            final_price=booking.final_price,
            status=booking.status,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        mock_bookings.append(new_booking)
        mock_id += 1
        return new_booking

    async def cancel_booking(self, booking_id: int) -> Optional[booking_schema.Booking]:
        for booking in mock_bookings:
            if booking.id == booking_id:
                booking.status = booking_schema.BookingStatus.CANCELLED
                booking.updated_at = datetime.datetime.now()
                return booking
        return None
    
    
    # Reschedule booking
    async def list_reschedule_logs(self) -> List[booking_schema.BookingRescheduleLog]:
        return mock_reschedule_logs

    async def get_reschedule_log(self, booking_id: int) -> List[booking_schema.BookingRescheduleLog]:
        return [log for log in mock_reschedule_logs if log.booking_id == booking_id]
    
    async def reschedule_booking(self, booking_id: int, new_travel_date: datetime.datetime, reason: str) -> bool:
        global mock_reschedule_logs_id
        for existing_booking in mock_bookings:
            if existing_booking.id == booking_id:
                reschedule_log = booking_schema.BookingRescheduleLog(
                    id=mock_reschedule_logs_id,
                    booking_id=booking_id,
                    previous_travel_date=existing_booking.travel_date,
                    new_travel_date=new_travel_date,
                    reason=reason,
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now()
                )
                existing_booking.travel_date = new_travel_date
                existing_booking.updated_at = datetime.datetime.now()
                mock_reschedule_logs.append(reschedule_log)
                mock_reschedule_logs_id += 1
                return True
        return False


