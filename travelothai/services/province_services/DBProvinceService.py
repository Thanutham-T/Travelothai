from typing import List, Optional
from fastapi import HTTPException

from .ProvinceServiceInterface import ProvinceServiceInterface
from travelothai.schemas import province_schema
from travelothai.models import province_model

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class DBProvinceService(ProvinceServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    # ProvinceCategory Methods
    async def list_province_categories(self) -> List[province_schema.ProvinceCategory]:
        result = await self.session.exec(select(province_model.ProvinceCategory))
        if not result:
            raise HTTPException(status_code=404, detail="No province categories found")
        categories = result.scalars().all()
        return categories
    
    async def get_province_category(self, category_id: int) -> Optional[province_schema.ProvinceCategory]:
        result = await self.session.exec(
            select(province_model.ProvinceCategory).where(province_model.ProvinceCategory.id == category_id)
            )
        if not result:
            raise HTTPException(status_code=404, detail="Province category not found")
        category = result.scalar()
        return category
    
    async def create_province_category(self, category: province_schema.ProvinceCategoryCreate) -> province_schema.ProvinceCategory:
        # Validate that the category name not empty and unique
        if not category.name:
            raise HTTPException(status_code=400, detail="Category name must not be empty")
        result = await self.session.exec(
            select(province_model.ProvinceCategory).where(province_model.ProvinceCategory.name == category.name)
        )
        existing_category = result.first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category name must be unique")
        
        # Create the category
        db_category = province_model.ProvinceCategory(**category.model_dump())
        self.session.add(db_category)
        await self.session.commit()
        await self.session.refresh(db_category)
        return db_category
    

    async def update_province_category(self, category_id: int, category: province_schema.ProvinceCategoryUpdate) -> Optional[province_schema.ProvinceCategory]:
        # Validate that the category exists & name is not empty and unique
        db_category = await self.session.get(province_model.ProvinceCategory, category_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")
        if not category.name:
            raise HTTPException(status_code=400, detail="Category name must not be empty")
        result = await self.session.exec(
            select(province_model.ProvinceCategory).where(
                province_model.ProvinceCategory.name == category.name,
                province_model.ProvinceCategory.id != category_id
            )
        )
        existing_category = result.first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category name must be unique")
        
        # Update the category details
        update_data = category.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        self.session.add(db_category)
        await self.session.commit()
        await self.session.refresh(db_category)
        return db_category
    
    async def delete_province_category(self, category_id: int) -> None:
        # Validate that the category exists before deleting
        if not category_id:
            raise HTTPException(status_code=400, detail="Category ID must be provided for deletion.")
        if not await self.get_province_category(category_id):
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Delete the category
        db_category = await self.session.get(province_model.ProvinceCategory, category_id)
        if db_category:
            await self.session.delete(db_category)
            await self.session.commit()


    # Province Methods
    async def list_provinces(self) -> List[province_schema.Province]:
        result = await self.session.exec(select(province_model.Province))
        if not result:
            raise HTTPException(status_code=404, detail="No provinces found")
        provinces = result.scalars().all()
        return provinces

    async def get_province(self, province_id: int) -> Optional[province_schema.Province]:
        result = await self.session.exec(
            select(province_model.Province).where(province_model.Province.id == province_id)
            )
        if not result:
            raise HTTPException(status_code=404, detail="Province not found")
        province = result.scalar()
        return province

    async def create_province(self, province: province_schema.ProvinceCreate) -> province_schema.Province:
        # Validate that the province name is not empty and unique
        if not province.name:
            raise HTTPException(status_code=400, detail="Province name must not be empty")
        result = await self.session.exec(
            select(province_model.Province).where(province_model.Province.name == province.name)
        )
        existing_province = result.first()
        if existing_province:
            raise HTTPException(status_code=400, detail="Province name must be unique")
        
        # Create the province
        db_province = province_model.Province(**province.model_dump())
        self.session.add(db_province)
        await self.session.commit()
        await self.session.refresh(db_province)
        return db_province


    async def update_province(self, province_id: int, province: province_schema.ProvinceUpdate) -> Optional[province_schema.Province]:
        # Validate that the province exists & name is unique
        db_province = await self.session.get(province_model.Province, province_id)
        if not db_province:
            raise HTTPException(status_code=404, detail="Province not found")
        result = await self.session.exec(
            select(province_model.Province).where(
                province_model.Province.name == province.name,
                province_model.Province.id != province_id
            )
        )
        existing_province = result.first()
        if existing_province:
            raise HTTPException(status_code=400, detail="Province name must be unique")
        
        # Update the province details
        update_data = province.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_province, key, value)
        self.session.add(db_province)
        await self.session.commit()
        await self.session.refresh(db_province)
        return db_province


    async def delete_province(self, province_id: int) -> None:
        # Validate that the province exists before deleting
        if not province_id:
            raise HTTPException(status_code=400, detail="Province ID must be provided for deletion.")
        if not await self.get_province(province_id):
            raise HTTPException(status_code=404, detail="Province not found")
        
        # Delete the province
        db_province = await self.session.get(province_model.Province, province_id)
        await self.session.delete(db_province)
        await self.session.commit()
