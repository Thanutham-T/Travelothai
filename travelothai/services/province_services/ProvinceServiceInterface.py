from abc import ABC, abstractmethod

from travelothai.schemas import province_schema


class ProvinceServiceInterface(ABC):
    @abstractmethod
    def list_provinces(self) -> list[province_schema.Province]:
        """List all provinces."""
        pass

    @abstractmethod
    def get_province(self, province_id: int) -> province_schema.Province:
        """Get a specific province by ID."""
        pass

    @abstractmethod
    def create_province(self, province: province_schema.ProvinceCreate) -> province_schema.Province:
        """Create a new province."""
        pass

    @abstractmethod
    def update_province(self, province_id: int, province: province_schema.ProvinceUpdate) -> province_schema.Province:
        """Update an existing province."""
        pass

    @abstractmethod
    def delete_province(self, province_id: int) -> None:
        """Delete a province."""
        pass
        