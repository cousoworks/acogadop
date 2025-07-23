from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import UserType, ShelterStatus

class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    user_type: UserType = UserType.FOSTER

class ShelterRegistration(UserBase):
    password: str
    shelter_name: str
    shelter_license: Optional[str] = None
    shelter_address: Optional[str] = None
    shelter_website: Optional[str] = None
    shelter_description: Optional[str] = None
    user_type: UserType = UserType.SHELTER

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    user_type: Optional[UserType] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    password: Optional[str] = None
    
    # Shelter fields
    shelter_name: Optional[str] = None
    shelter_license: Optional[str] = None
    shelter_address: Optional[str] = None
    shelter_website: Optional[str] = None
    shelter_description: Optional[str] = None
    shelter_status: Optional[ShelterStatus] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    shelter_name: Optional[str] = None
    shelter_status: Optional[ShelterStatus] = None
    
    class Config:
        from_attributes = True

class ShelterApplicationResponse(BaseModel):
    id: int
    email: str
    name: str
    phone: Optional[str]
    location: Optional[str]
    shelter_name: Optional[str]
    shelter_license: Optional[str]
    shelter_address: Optional[str]
    shelter_website: Optional[str]
    shelter_description: Optional[str]
    shelter_status: ShelterStatus
    admin_notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ShelterApproval(BaseModel):
    user_id: int
    approved: bool
    admin_notes: Optional[str] = None

class User(UserResponse):
    pass