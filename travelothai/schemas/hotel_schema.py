from datetime import datetime
from typing import Optional
from pydantic import BaseModel, config


# Hotel schema
class HotelBase(BaseModel):
    name: str
    province_id: int
    price: float

class HotelCreate(HotelBase):
    pass

class HotelUpdate(HotelBase):
    name: Optional[str] = None
    province_id: Optional[int] = None
    price: Optional[float] = None

class Hotel(HotelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = config.ConfigDict(from_attributes=True)
