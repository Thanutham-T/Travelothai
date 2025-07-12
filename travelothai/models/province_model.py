from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from travelothai.schemas.hotel_schema import Hotel

# ProvinceCategory model
class ProvinceCategoryBase(SQLModel):
    name: str = Field(index=True, unique=True)

class ProvinceCategory(ProvinceCategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationship
    provinces: List["Province"] = Relationship(back_populates="category")


# Province model
class ProvinceBase(SQLModel):
    name: str = Field(index=True, unique=True)
    category_id: int = Field(foreign_key="provincecategory.id")

class Province(ProvinceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationship
    hotels: List["Hotel"] = Relationship(back_populates="province")
    category: Optional[ProvinceCategory] = Relationship(back_populates="provinces")
