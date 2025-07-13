from datetime import datetime
from typing import Optional
from pydantic import BaseModel, config


# Province schema
class ProvinceBase(BaseModel):
    name: str
    category_id: int

class ProvinceCreate(ProvinceBase):
    pass

class ProvinceUpdate(ProvinceBase):
    name: Optional[str] = None
    category_id: Optional[int] = None

class Province(ProvinceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = config.ConfigDict(from_attributes=True)


# ProvinceCategory schema
class ProvinceCategoryBase(BaseModel):
    name: str

class ProvinceCategoryCreate(ProvinceCategoryBase):
    pass

class ProvinceCategoryUpdate(ProvinceCategoryBase):
    name: Optional[str] = None

class ProvinceCategory(ProvinceCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = config.ConfigDict(from_attributes=True)
