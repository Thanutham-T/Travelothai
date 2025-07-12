from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .province_model import Province
    from .booking_model import Booking

# Hotel model
class HotelBase(SQLModel):
    name: str = Field(index=True)
    province_id: int = Field(foreign_key="province.id")
    price: float = Field(gt=0)

class Hotel(HotelBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationship
    province: Optional["Province"] = Relationship(back_populates="hotels")
    bookings: List["Booking"] = Relationship(back_populates="hotel")
