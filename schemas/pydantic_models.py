from typing import Union

from pydantic import BaseModel, Field
from enum import Enum

class Feature(str, Enum):
    YES = 'Yes'
    NO = 'No'

class Building(str, Enum):
    VILLA = 'VILLA'
    EXCEPTIONAL_PROPERTY = 'EXCEPTIONAL_PROPERTY'
    HOUSE = 'HOUSE'
    MIXED_USE_BUILDING = 'MIXED_USE_BUILDING'
    BUNGALOW = 'BUNGALOW'
    COUNTRY_COTTAGE = 'COUNTRY_COTTAGE'
    TOWN_HOUSE = 'TOWN_HOUSE'
    LOFT = 'LOFT'
    MANSION = 'MANSION'
    APARTMENT = 'APARTMENT'
    MANOR_HOUSE = 'MANOR_HOUSE'
    CHALET = 'CHALET'
    CASTLE = 'CASTLE'
    FARMHOUSE = 'FARMHOUSE'
    OTHER_PROPERTY = 'OTHER_PROPERTY'
    FLAT_STUDIO = 'FLAT_STUDIO'
    DUPLEX = 'DUPLEX'
    GROUND_FLOOR = 'GROUND_FLOOR'
    PENTHOUSE = 'PENTHOUSE'
    KOT = 'KOT'
    SERVICE_FLAT = 'SERVICE_FLAT'
    TRIPLEX = 'TRIPLEX'

class Property(BaseModel):
    netHabitableSurface: Union[float, int] = Field(..., gt=0, description="The size in sqm must be greater than zero")
    bedroomCount: Union[float, int] = Field(..., ge=0, description="The number of bedrooms must be greater or equal to zero")
    condition: Feature = Field(..., description="['Yes'] means in 'good' condition - such as 'as_new', 'good' or 'renovated', ['No'] means some renovation/restoration is needed")
    subtype: Building = Field(..., description="Type of property in all caps and no white space")
    full_kitchen: Feature = Field(..., description="['Yes'] means that there is a FULLY equipped kitchen")
    postalCode: int = Field(..., gt=999, lt=10000, description="The zip_code must be greater than 999 and less than 10,000")
    hasTerrace: Feature = Field(..., description="['Yes'] means that there is at least 1 terrace")
    hasGarden: Feature = Field(..., description="['Yes'] means that there is a garden")
    hasSwimmingPool: Feature = Field(..., description="['Yes'] means that there is a swimming pool")