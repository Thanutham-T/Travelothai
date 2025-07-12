from fastapi import APIRouter, Depends

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

@router.get("/")
def read_provinces(province_service: ProvinceServiceInterface = Depends(get_province_service)) -> list[province_schema.Province]:
    provinces = province_service.list_provinces()
    return provinces

@router.get("/{province_id}", response_model=province_schema.Province)
def read_province(province_id: int, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> province_schema.Province:
    province = province_service.get_province(province_id)
    return province

@router.post("/", response_model=province_schema.Province)
def create_province(province: province_schema.ProvinceCreate, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> province_schema.Province:
    new_province = province_service.create_province(province)
    return new_province

@router.put("/{province_id}", response_model=province_schema.Province)
def update_province(province_id: int, province: province_schema.ProvinceUpdate, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> province_schema.Province:
    updated_province = province_service.update_province(province_id, province)
    return updated_province

@router.delete("/{province_id}", response_model=None)
def delete_province(province_id: int, province_service: ProvinceServiceInterface = Depends(get_province_service)) -> None:
    province_service.delete_province(province_id)
    return None
