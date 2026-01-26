from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# Shared properties
class PsGcBase(SQLModel):
    code: str = Field(index=True, unique=True)
    name: str = Field(index=True)
    
class Region(PsGcBase, table=True):
    __tablename__ = "regions"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    provinces: List["Province"] = Relationship(back_populates="region")
    districts: List["District"] = Relationship(back_populates="region")
    cities: List["City"] = Relationship(back_populates="region") 

class Province(PsGcBase, table=True):
    __tablename__ = "provinces"
    id: Optional[int] = Field(default=None, primary_key=True)
    region_code: str = Field(foreign_key="regions.code", index=True)
    
    region: Optional[Region] = Relationship(back_populates="provinces")
    cities: List["City"] = Relationship(back_populates="province")
    
class District(PsGcBase, table=True):
    __tablename__ = "districts"
    id: Optional[int] = Field(default=None, primary_key=True)
    region_code: str = Field(foreign_key="regions.code", index=True)
    
    region: Optional[Region] = Relationship(back_populates="districts")
    cities: List["City"] = Relationship(back_populates="district")

class City(PsGcBase, table=True):
    __tablename__ = "cities"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    province_code: Optional[str] = Field(default=None, foreign_key="provinces.code", index=True)
    district_code: Optional[str] = Field(default=None, foreign_key="districts.code", index=True)
    region_code: str = Field(foreign_key="regions.code", index=True)
    
    city_class: Optional[str] = None 
    
    province: Optional[Province] = Relationship(back_populates="cities")
    district: Optional[District] = Relationship(back_populates="cities")
    region: Optional[Region] = Relationship(back_populates="cities")
    
    barangays: List["Barangay"] = Relationship(back_populates="city")

class Barangay(PsGcBase, table=True):
    __tablename__ = "barangays"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    city_code: str = Field(foreign_key="cities.code", index=True)
    province_code: Optional[str] = Field(default=None, index=True)
    region_code: Optional[str] = Field(default=None, index=True)
    
    city: Optional[City] = Relationship(back_populates="barangays")
