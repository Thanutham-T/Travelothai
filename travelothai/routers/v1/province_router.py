from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List, Optional

from travelothai.core.config import get_settings
from travelothai.services.province_services.ProvinceServiceInterface import ProvinceServiceInterface
from travelothai.services.province_services.MockProvinceService import MockProvinceService
from travelothai.services.province_services.DBProvinceService import DBProvinceService

from travelothai.schemas import province_schema

router = APIRouter(prefix="/provinces", tags=["provinces"])


def get_province_service() -> ProvinceServiceInterface:
    settings = get_settings()
    if settings.USE_MOCK:
        return MockProvinceService()
    return DBProvinceService()

@router.get(
        "/",
        summary="List all provinces",
        description="Retrieve a list of all provinces available in the system.",
        response_model=list[province_schema.Province]
    )
async def read_provinces(province_service: ProvinceServiceInterface = Depends(get_province_service)) -> List[province_schema.Province]:
    provinces = await province_service.list_provinces()
    if not provinces:
        raise HTTPException(status_code=404, detail="No provinces found")
    return provinces

@router.get(
        "/{province_id}", 
        summary="Get a specific province",
        description="Retrieve details of a specific province by its ID.",
        response_model=province_schema.Province
    )
async def read_province(province_id: int, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> Optional[province_schema.Province]:
    province = await province_service.get_province(province_id)
    if province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    return province

@router.post(
        "/",
        summary="Create a new province",
        description="Create a new province in the system.",
        response_model=province_schema.Province
    )
async def create_province(province: province_schema.ProvinceCreate, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> province_schema.Province:
    return await province_service.create_province(province)

@router.put(
        "/{province_id}",
        summary="Update a province",
        description="Update an existing province in the system.",
        response_model=province_schema.Province
    )
async def update_province(province_id: int, province: province_schema.ProvinceUpdate, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> Optional[province_schema.Province]:
    updated_province = await province_service.update_province(province_id, province)
    if updated_province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    return updated_province

@router.delete(
        "/{province_id}",
        summary="Delete a province",
        description="Delete a province from the system.",
        response_model=None
    )
async def delete_province(province_id: int, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> None:
    province = await province_service.get_province(province_id)
    if not province:
        raise HTTPException(status_code=404, detail="Province not found")
    await province_service.delete_province(province_id)
    return Response(status_code=204, content=None)
