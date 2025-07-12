import datetime
from typing import List, Optional

from .ProvinceServiceInterface import ProvinceServiceInterface
from travelothai.schemas import province_schema


mock_provinces_category: List[province_schema.ProvinceCategory] = [
    province_schema.ProvinceCategory(id=1, name="เมืองหลัก", created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
    province_schema.ProvinceCategory(id=2, name="เมืองรอง", created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
]
mock_provinces_category_id = 3

mock_provinces: List[province_schema.Province] = [
    province_schema.Province(id=1, name="กรุงเทพมหานคร", category_id=1, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
    province_schema.Province(id=2, name="น่าน", category_id=2, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()),
]
mock_id = 3

class MockProvinceService(ProvinceServiceInterface):
    # Mock ProvinceCategory methods
    async def list_province_categories(self) -> List[province_schema.ProvinceCategory]:
        return mock_provinces_category
    
    async def get_province_category(self, category_id: int) -> Optional[province_schema.ProvinceCategory]:
        for category in mock_provinces_category:
            if category.id == category_id:
                return category
        return None
    
    async def create_province_category(self, category: province_schema.ProvinceCategoryCreate) -> province_schema.ProvinceCategory:
        global mock_provinces_category_id
        new_category = province_schema.ProvinceCategory(
            id=mock_provinces_category_id,
            name=category.name,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        mock_provinces_category.append(new_category)
        mock_provinces_category_id += 1
        return new_category
    
    async def update_province_category(self, category_id: int, category: province_schema.ProvinceCategoryUpdate) -> Optional[province_schema.ProvinceCategory]:
        for idx, existing_category in enumerate(mock_provinces_category):
            if existing_category.id == category_id:
                updated_category = existing_category.model_copy(update=category.model_dump(exclude_unset=True))
                updated_category.updated_at = datetime.datetime.now()
                mock_provinces_category[idx] = updated_category
                return updated_category
        return None
    
    async def delete_province_category(self, category_id: int) -> None:
        global mock_provinces_category
        mock_provinces_category = [category for category in mock_provinces_category if category.id != category_id]
        return None
    
    
    # Mock ProvinceService methods
    async def list_provinces(self) -> List[province_schema.Province]:
        return mock_provinces

    async def get_province(self, province_id: int) -> Optional[province_schema.Province]:
        for province in mock_provinces:
            if province.id == province_id:
                return province
        return None

    async def create_province(self, province: province_schema.ProvinceCreate) -> province_schema.Province:
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

    async def update_province(self, province_id: int, province: province_schema.ProvinceUpdate) -> Optional[province_schema.Province]:
        for idx, existing_province in enumerate(mock_provinces):
            if existing_province.id == province_id:
                updated_province = existing_province.model_copy(update=province.model_dump(exclude_unset=True))
                updated_province.updated_at = datetime.datetime.now()
                mock_provinces[idx] = updated_province
                return updated_province
        return None

    async def delete_province(self, province_id: int) -> None:
        global mock_provinces
        mock_provinces = [province for province in mock_provinces if province.id != province_id]
        return None
