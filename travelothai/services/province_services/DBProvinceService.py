from typing import List, Optional

from .ProvinceServiceInterface import ProvinceServiceInterface
from travelothai.schemas import province_schema
from travelothai.models import get_session, province_model
from sqlalchemy.future import select
from contextlib import asynccontextmanager

class DBProvinceService(ProvinceServiceInterface):
    @asynccontextmanager
    async def _get_session(self):
        async for session in get_session():
            yield session

    async def list_provinces(self) -> List[province_schema.Province]:
        async with self._get_session() as session:
            result = await session.exec(select(province_model.Province))
            provinces = result.scalars().all()
            return provinces

    async def get_province(self, province_id: int) -> Optional[province_schema.Province]:
        async with self._get_session() as session:
            result = await session.exec(
                select(province_model.Province).where(province_model.Province.id == province_id)
            )
            province = result.scalar()
            return province

    async def create_province(self, province: province_schema.ProvinceCreate) -> province_schema.Province:
        async with self._get_session() as session:
            db_province = province_model.Province(**province.model_dump())
            session.add(db_province)
            await session.commit()
            await session.refresh(db_province)
            return db_province

    async def update_province(self, province_id: int, province: province_schema.ProvinceUpdate) -> Optional[province_schema.Province]:
        async with self._get_session() as session:
            db_province = await session.get(province_model.Province, province_id)
            if not db_province:
                return None
            update_data = province.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_province, key, value)
            session.add(db_province)
            await session.commit()
            await session.refresh(db_province)
            return db_province

    async def delete_province(self, province_id: int) -> None:
        async with self._get_session() as session:
            db_province = await session.get(province_model.Province, province_id)
            if db_province:
                await session.delete(db_province)
                await session.commit()
