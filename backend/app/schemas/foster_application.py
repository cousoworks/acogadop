from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.foster_application import ApplicationStatus

class FosterApplicationBase(BaseModel):
    message: Optional[str] = None
    experience: Optional[str] = None
    living_situation: Optional[str] = None
    availability: Optional[str] = None

class FosterApplicationCreate(FosterApplicationBase):
    dog_id: int

class FosterApplicationUpdate(BaseModel):
    status: ApplicationStatus
    admin_notes: Optional[str] = None

class FosterApplicationResponse(FosterApplicationBase):
    id: int
    user_id: int
    dog_id: int
    status: ApplicationStatus
    admin_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class FosterApplication(FosterApplicationResponse):
    pass