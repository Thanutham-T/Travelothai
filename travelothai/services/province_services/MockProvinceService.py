import datetime

from .ProvinceServiceInterface import ProvinceServiceInterface
from travelothai.schemas import province_schema


mock_provinces: list[province_schema.Province] = [
    province_schema.Province(id=1, name="กรุงเทพมหานคร", category_id=1, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
    province_schema.Province(id=2, name="น่าน", category_id=2, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
]
mock_id = 3

class MockProvinceService(ProvinceServiceInterface):
    def list_provinces(self) -> list[province_schema.Province]:
        return mock_provinces
    
    def get_province(self, province_id: int) -> province_schema.Province:
        for province in mock_provinces:
            if province.id == province_id:
                return province
        raise ValueError("Province not found")
    
    def create_province(self, province: province_schema.ProvinceCreate) -> province_schema.Province:
        global mock_id
        new_province = province_schema.Province(
            id=mock_id,
            name=province.name,
            category_id=province.category_id,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        mock_provinces.append(new_province)
        mock_id += 1
        return new_province
    
    def update_province(self, province_id: int, province: province_schema.ProvinceUpdate) -> province_schema.Province:
        for idx, existing_province in enumerate(mock_provinces):
            if existing_province.id == province_id:
                updated_province = existing_province.model_copy(update=province.model_dump(exclude_unset=True))
                updated_province.updated_at = datetime.datetime.now()
                mock_provinces[idx] = updated_province
                return updated_province
        raise ValueError("Province not found")
    
    def delete_province(self, province_id: int) -> None:
        global mock_provinces
        mock_provinces = [province for province in mock_provinces if province.id != province_id]
        if len(mock_provinces) == 0:
            raise ValueError("Province not found")
        return None
