from abc import ABC, abstractmethod
from typing import List, Optional

from travelothai.schemas import hotel_schema


class HotelServiceInterface(ABC):
    @abstractmethod
    async def list_hotels(self) -> List[hotel_schema.Hotel]:
        """List all hotels."""
        pass

    @abstractmethod
    async def get_hotel(self, hotel_id: int) -> Optional[hotel_schema.Hotel]:
        """Get a specific hotel by ID."""
        pass

    @abstractmethod
    async def create_hotel(self, hotel: hotel_schema.HotelCreate) -> hotel_schema.Hotel:
        """Create a new hotel."""
        pass

    @abstractmethod
    async def update_hotel(self, hotel_id: int, hotel: hotel_schema.HotelUpdate) -> Optional[hotel_schema.Hotel]:
        """Update an existing hotel."""
        pass

    @abstractmethod
    async def delete_hotel(self, hotel_id: int) -> None:
        """Delete a hotel."""
        pass
        