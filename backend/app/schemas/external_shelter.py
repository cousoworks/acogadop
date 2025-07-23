from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, HttpUrl
from app.models.external_shelter import ExternalShelterType, ExternalShelterStatus

class ExternalShelterBase(BaseModel):
    name: str
    website_url: str
    integration_type: ExternalShelterType
    location: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    description: Optional[str] = None

class ExternalShelterCreate(ExternalShelterBase):
    api_endpoint: Optional[str] = None
    rss_feed_url: Optional[str] = None
    scraping_config: Optional[Dict[str, Any]] = None
    api_config: Optional[Dict[str, Any]] = None
    sync_frequency_hours: int = 24

class ExternalShelterUpdate(BaseModel):
    name: Optional[str] = None
    website_url: Optional[str] = None
    api_endpoint: Optional[str] = None
    rss_feed_url: Optional[str] = None
    integration_type: Optional[ExternalShelterType] = None
    status: Optional[ExternalShelterStatus] = None
    scraping_config: Optional[Dict[str, Any]] = None
    api_config: Optional[Dict[str, Any]] = None
    location: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    description: Optional[str] = None
    sync_frequency_hours: Optional[int] = None

class ExternalShelterResponse(ExternalShelterBase):
    id: int
    status: ExternalShelterStatus
    api_endpoint: Optional[str]
    rss_feed_url: Optional[str]
    last_sync: Optional[datetime]
    sync_frequency_hours: int
    last_error: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ExternalDogBase(BaseModel):
    name: str
    breed: Optional[str] = None
    age: Optional[int] = None
    size: Optional[str] = None
    gender: Optional[str] = None
    weight: Optional[str] = None
    description: Optional[str] = None
    medical_info: Optional[str] = None
    behavior_notes: Optional[str] = None
    location: Optional[str] = None
    original_url: Optional[str] = None

class ExternalDogCreate(ExternalDogBase):
    external_shelter_id: int
    external_id: str
    photos: Optional[List[str]] = None

class ExternalDogResponse(ExternalDogBase):
    id: int
    external_shelter_id: int
    external_id: str
    photos: Optional[List[str]]
    is_available: bool
    last_seen: datetime
    created_at: datetime
    updated_at: Optional[datetime]
    external_shelter: Optional[ExternalShelterResponse] = None
    
    class Config:
        from_attributes = True

class SyncResult(BaseModel):
    shelter_id: int
    success: bool
    dogs_found: int
    dogs_created: int
    dogs_updated: int
    dogs_marked_unavailable: int
    error: Optional[str] = None
    sync_time: datetime
