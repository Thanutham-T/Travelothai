from .ProvinceServiceInterface import ProvinceServiceInterface
from travelothai.schemas import province_schema


class DBProvinceService(ProvinceServiceInterface):
    async def list_provinces(self) -> list[province_schema.Province]:
        # This method should interact with the database to retrieve all provinces
        raise NotImplementedError("This method should be implemented to fetch provinces from the database")
    
    async def get_province(self, province_id: int) -> province_schema.Province:
        # This method should interact with the database to retrieve a specific province by ID
        raise NotImplementedError("This method should be implemented to fetch a province from the database")
    
    async def create_province(self, province: province_schema.ProvinceCreate) -> province_schema.Province:
        # This method should interact with the database to create a new province
        raise NotImplementedError("This method should be implemented to create a province in the database")

    async def update_province(self, province_id: int, province: province_schema.ProvinceUpdate) -> province_schema.Province:
        # This method should interact with the database to update an existing province
        raise NotImplementedError("This method should be implemented to update a province in the database")

    async def delete_province(self, province_id: int) -> None:
        # This method should interact with the database to delete a province
        raise NotImplementedError("This method should be implemented to delete a province from the database")
