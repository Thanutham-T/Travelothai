from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# ProvinceCategory model
class ProvinceCategoryBase(SQLModel):
    name: str

class ProvinceCategory(ProvinceCategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

# Province model
class ProvinceBase(SQLModel):
    name: str = Field(index=True)
    category_id: int = Field(foreign_key="provincecategory.id")

class Province(ProvinceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    category: Optional[ProvinceCategory] = Relationship(back_populates="provinces")
