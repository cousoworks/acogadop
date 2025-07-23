from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class UserType(enum.Enum):
    FOSTER = "foster"
    SHELTER = "shelter"
    SHELTER_ADMIN = "shelter_admin"  # Perreras aprobadas
    VOLUNTEER = "volunteer"
    ADMIN = "admin"

class ShelterStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String)
    location = Column(String)
    user_type = Column(Enum(UserType), default=UserType.FOSTER)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Shelter-specific fields
    shelter_name = Column(String)  # Nombre oficial de la perrera
    shelter_license = Column(String)  # Número de licencia o registro
    shelter_address = Column(String)  # Dirección completa
    shelter_website = Column(String)  # Sitio web (opcional)
    shelter_description = Column(Text)  # Descripción de la perrera
    shelter_status = Column(Enum(ShelterStatus), default=ShelterStatus.PENDING)  # Estado de aprobación
    admin_notes = Column(Text)  # Notas del administrador sobre la aprobación/rechazo
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    dogs = relationship("Dog", back_populates="owner")
    foster_applications = relationship("FosterApplication", back_populates="user")