from fastapi import APIRouter, Depends, Response
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from travelothai.core.config import get_settings
from travelothai.services.province_services.ProvinceServiceInterface import ProvinceServiceInterface
from travelothai.services.province_services.MockProvinceService import MockProvinceService
from travelothai.services.province_services.DBProvinceService import DBProvinceService

from travelothai.schemas import province_schema
from travelothai.models import get_session

router = APIRouter(prefix="/provinces", tags=["provinces"])


def get_province_service(session: AsyncSession = Depends(get_session)) -> ProvinceServiceInterface:
    settings = get_settings()
    if settings.USE_MOCK:
        return MockProvinceService()
    return DBProvinceService(session=session)

# ProvinceCategory Endpoints
@router.get(
        "/categories",
        summary="List all province categories",
        description="Retrieve a list of all province categories available in the system.",
        response_model=list[province_schema.ProvinceCategory]
    )
async def read_province_categories(province_service: ProvinceServiceInterface = Depends(get_province_service)) -> List[province_schema.ProvinceCategory]:
    categories = await province_service.list_province_categories()
    return categories

@router.get(
        "/categories/{category_id}",
        summary="Get a specific province category",
        description="Retrieve details of a specific province category by its ID.",
        response_model=province_schema.ProvinceCategory
    )
async def read_province_category(category_id: int, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> Optional[province_schema.ProvinceCategory]:
    category = await province_service.get_province_category(category_id)
    return category

@router.post(
        "/categories",
        summary="Create a new province category",
        description="Create a new province category in the system.",
        response_model=province_schema.ProvinceCategory
    )
async def create_province_category(category: province_schema.ProvinceCategoryCreate, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> province_schema.ProvinceCategory:
    return await province_service.create_province_category(category)

@router.put(
        "/categories/{category_id}",
        summary="Update a province category",
        description="Update an existing province category in the system.",
        response_model=province_schema.ProvinceCategory
    )
async def update_province_category(category_id: int, category: province_schema.ProvinceCategoryUpdate, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> Optional[province_schema.ProvinceCategory]:
    updated_category = await province_service.update_province_category(category_id, category)
    return updated_category

@router.delete(
        "/categories/{category_id}",
        summary="Delete a province category",
        description="Delete a province category from the system.",
        response_model=None
    )
async def delete_province_category(category_id: int, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> None:
    await province_service.delete_province_category(category_id)
    return Response(status_code=204, content=None)


# Province Endpoints
@router.get(
        "/",
        summary="List all provinces",
        description="Retrieve a list of all provinces available in the system.",
        response_model=list[province_schema.Province]
    )
async def read_provinces(province_service: ProvinceServiceInterface = Depends(get_province_service)) -> List[province_schema.Province]:
    provinces = await province_service.list_provinces()
    return provinces

@router.get(
        "/{province_id}", 
        summary="Get a specific province",
        description="Retrieve details of a specific province by its ID.",
        response_model=province_schema.Province
    )
async def read_province(province_id: int, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> Optional[province_schema.Province]:
    province = await province_service.get_province(province_id)
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
    return updated_province

@router.delete(
        "/{province_id}",
        summary="Delete a province",
        description="Delete a province from the system.",
        response_model=None
    )
async def delete_province(province_id: int, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> None:
    await province_service.delete_province(province_id)
    return Response(status_code=204, content=None)
