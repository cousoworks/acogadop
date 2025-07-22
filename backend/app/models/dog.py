from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class DogStatus(enum.Enum):
    AVAILABLE = "available"
    FOSTERED = "fostered"
    ADOPTED = "adopted"
    MEDICAL_CARE = "medical_care"

class DogSize(enum.Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra_large"

class DogGender(enum.Enum):
    MALE = "male"
    FEMALE = "female"

class Dog(Base):
    __tablename__ = "dogs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    breed = Column(String)
    age = Column(Integer)  # Age in months
    size = Column(Enum(DogSize))
    gender = Column(Enum(DogGender))
    weight = Column(Float)  # Weight in kg
    
    # Location and contact
    location = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Description and status
    description = Column(Text)
    medical_info = Column(Text)
    behavior_notes = Column(Text)
    status = Column(Enum(DogStatus), default=DogStatus.AVAILABLE)
    
    # Requirements
    good_with_kids = Column(Boolean, default=False)
    good_with_dogs = Column(Boolean, default=False)
    good_with_cats = Column(Boolean, default=False)
    needs_yard = Column(Boolean, default=False)
    
    # Media
    photos = Column(Text)  # JSON string of photo URLs
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="dogs")
    foster_applications = relationship("FosterApplication", back_populates="dog")