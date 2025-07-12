from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from travelothai.models.province_model import Province


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
    province: Optional[Province] = Relationship(back_populates="hotels")
