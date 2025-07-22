from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ApplicationStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"

class FosterApplication(Base):
    __tablename__ = "foster_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=False)
    
    # Application details
    message = Column(Text)
    experience = Column(Text)
    living_situation = Column(Text)
    availability = Column(String)
    
    # Status
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    admin_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="foster_applications")
    dog = relationship("Dog", back_populates="foster_applications")