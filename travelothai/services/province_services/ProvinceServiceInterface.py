from abc import ABC, abstractmethod
from typing import List, Optional

from travelothai.schemas import province_schema


class ProvinceServiceInterface(ABC):
    # ProvinceCategory methods
    @abstractmethod
    async def list_province_categories(self) -> List[province_schema.ProvinceCategory]:
        """List all province categories."""
        pass

    @abstractmethod
    async def get_province_category(self, category_id: int) -> Optional[province_schema.ProvinceCategory]:
        """Get a specific province category by ID."""
        pass

    @abstractmethod
    async def create_province_category(self, category: province_schema.ProvinceCategoryCreate) -> province_schema.ProvinceCategory:
        """Create a new province category."""
        pass

    @abstractmethod
    async def update_province_category(self, category_id: int, category: province_schema.ProvinceCategoryUpdate) -> Optional[province_schema.ProvinceCategory]:
        """Update an existing province category."""
        pass

    @abstractmethod
    async def delete_province_category(self, category_id: int) -> None:
        """Delete a province category."""
        pass

    # Province methods
    @abstractmethod
    async def list_provinces(self) -> List[province_schema.Province]:
        """List all provinces."""
        pass

    @abstractmethod
    async def get_province(self, province_id: int) -> Optional[province_schema.Province]:
        """Get a specific province by ID."""
        pass

    @abstractmethod
    async def create_province(self, province: province_schema.ProvinceCreate) -> province_schema.Province:
        """Create a new province."""
        pass

    @abstractmethod
    async def update_province(self, province_id: int, province: province_schema.ProvinceUpdate) -> Optional[province_schema.Province]:
        """Update an existing province."""
        pass

    @abstractmethod
    async def delete_province(self, province_id: int) -> None:
        """Delete a province."""
        pass
        