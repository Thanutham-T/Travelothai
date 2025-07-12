from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import HTTPException

from .BookingServiceInterface import BookingServiceInterface
from travelothai.schemas import booking_schema
from travelothai.models import booking_model, hotel_model, ticket_model

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class DBBookingService(BookingServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_bookings(self) -> List[booking_schema.Booking]:
        result = await self.session.exec(select(booking_model.Booking))
        if not result:
            raise HTTPException(status_code=404, detail="No bookings found")
        bookings = result.scalars().all()
        return bookings

    async def get_booking(self, booking_id: int) -> Optional[booking_schema.Booking]:
        result = await self.session.exec(
            select(booking_model.Booking).where(booking_model.Booking.id == booking_id)
        )
        if not result:
            raise HTTPException(status_code=404, detail="Booking not found")
        booking = result.scalar()
        return booking

    async def create_booking(self, booking: booking_schema.BookingCreate) -> booking_schema.Booking:
        if not booking.hotel_id:
            raise HTTPException(status_code=400, detail="Hotel ID must be provided for booking creation.")

        db_hotel = await self.session.get(hotel_model.Hotel, booking.hotel_id)
        if not db_hotel:
            raise HTTPException(status_code=404, detail=f"Hotel with ID {booking.hotel_id} does not exist.")

        db_booking = booking_model.Booking(**booking.model_dump(exclude_unset=True))
        db_booking.price = db_hotel.price

        db_discount_amount = 0

        if booking.ticket_id:
            db_ticket = await self.session.get(ticket_model.Ticket, booking.ticket_id)
            if not db_ticket:
                raise HTTPException(status_code=404, detail=f"Ticket with ID {booking.ticket_id} does not exist.")
            if db_ticket.used >= db_ticket.amount:
                raise HTTPException(status_code=400, detail=f"Ticket with ID {booking.ticket_id} has already been fully used.")
            
            db_booking.ticket_id = booking.ticket_id

            db_ticket_result = await self.session.exec(
                select(ticket_model.Ticket).where(ticket_model.Ticket.id == booking.ticket_id)
            )
            db_ticket_obj = db_ticket_result.scalar_one_or_none()

            if db_ticket_obj:
                db_ticket_type_result = await self.session.exec(
                    select(ticket_model.TicketType).where(ticket_model.TicketType.id == db_ticket_obj.ticket_type_id)
                )
                db_ticket_type = db_ticket_type_result.scalar_one_or_none()
                if db_ticket_type:
                    db_discount_amount_result = await self.session.exec(
                        select(ticket_model.TicketUsageRule.tax_reduction).where(
                            ticket_model.TicketUsageRule.ticket_type_id == db_ticket_type.id
                        )
                    )
                    db_discount_amount = db_discount_amount_result.scalar_one_or_none() or 0

                    db_ticket.used += 1
                    self.session.add(db_ticket)
                    await self.session.commit()
                    await self.session.refresh(db_ticket)

        db_booking.discount_amount = db_discount_amount * db_booking.price
        db_booking.final_price = db_booking.price - db_booking.discount_amount

        db_booking.travel_date = booking.travel_date if booking.travel_date else datetime.now() + timedelta(days=7)
        db_booking.status = booking_schema.BookingStatus.BOOKING

        self.session.add(db_booking)
        await self.session.commit()
        await self.session.refresh(db_booking)
        return db_booking

    
    async def cancel_booking(self, booking_id: int) -> Optional[booking_schema.Booking]:
        booking = await self.get_booking(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Update the booking status to cancelled
        booking.status = booking_schema.BookingStatus.CANCELLED
        self.session.add(booking)
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def reschedule_booking(self, booking_id: int, new_travel_date: datetime, reason: str) -> Optional[booking_schema.BookingRescheduleLog]:
        booking = await self.get_booking(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Create a reschedule log entry
        reschedule_log = booking_model.BookingRescheduleLog(
            booking_id=booking.id,
            previous_travel_date=booking.travel_date,
            new_travel_date=new_travel_date,
            reason=reason
        )
        self.session.add(reschedule_log)
        
        # Update the booking's travel date
        booking.travel_date = new_travel_date
        self.session.add(booking)
        
        await self.session.commit()
        await self.session.refresh(booking)
        return reschedule_log
    
    async def list_reschedule_logs(self) -> List[booking_schema.BookingRescheduleLog]:
        result = await self.session.exec(select(booking_model.BookingRescheduleLog))
        if not result:
            raise HTTPException(status_code=404, detail="No reschedule logs found")
        reschedule_logs = result.scalars().all()
        return reschedule_logs
    
    async def get_reschedule_log(self, booking_id: int) -> List[booking_schema.BookingRescheduleLog]:
        result = await self.session.exec(
            select(booking_model.BookingRescheduleLog).where(booking_model.BookingRescheduleLog.booking_id == booking_id)
        )
        if not result:
            raise HTTPException(status_code=404, detail="No reschedule logs found for this booking")
        reschedule_logs = result.scalars().all()
        return reschedule_logs
