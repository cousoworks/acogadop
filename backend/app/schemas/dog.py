from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.models.dog import DogStatus, DogSize, DogGender

class DogBase(BaseModel):
    name: str
    breed: Optional[str] = None
    age: Optional[int] = None  # Age in months
    size: Optional[DogSize] = None
    gender: Optional[DogGender] = None
    weight: Optional[float] = None
    location: Optional[str] = None
    description: Optional[str] = None
    medical_info: Optional[str] = None
    behavior_notes: Optional[str] = None
    good_with_kids: bool = False
    good_with_dogs: bool = False
    good_with_cats: bool = False
    needs_yard: bool = False

class DogCreate(DogBase):
    pass

class DogUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    size: Optional[DogSize] = None
    gender: Optional[DogGender] = None
    weight: Optional[float] = None
    location: Optional[str] = None
    description: Optional[str] = None
    medical_info: Optional[str] = None
    behavior_notes: Optional[str] = None
    status: Optional[DogStatus] = None
    good_with_kids: Optional[bool] = None
    good_with_dogs: Optional[bool] = None
    good_with_cats: Optional[bool] = None
    needs_yard: Optional[bool] = None

class DogResponse(DogBase):
    id: int
    status: DogStatus
    owner_id: Optional[int] = None
    photos: Optional[List[str]] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Dog(DogResponse):
    pass