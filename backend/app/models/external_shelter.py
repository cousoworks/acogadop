from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ExternalShelterType(enum.Enum):
    SCRAPER = "scraper"  # Web scraping
    API = "api"  # API integration
    RSS = "rss"  # RSS feed

class ExternalShelterStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class ExternalShelter(Base):
    """Modelo para perreras externas que tienen web propia"""
    __tablename__ = "external_shelters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Nombre de la perrera
    website_url = Column(String, nullable=False)  # URL principal
    api_endpoint = Column(String)  # Endpoint de API si existe
    rss_feed_url = Column(String)  # URL del RSS si existe
    
    # Configuración de integración
    integration_type = Column(Enum(ExternalShelterType), nullable=False)
    status = Column(Enum(ExternalShelterStatus), default=ExternalShelterStatus.ACTIVE)
    
    # Configuración de scraping/parsing
    scraping_config = Column(JSON)  # Configuración JSON para selectores CSS, etc.
    api_config = Column(JSON)  # Configuración para APIs (headers, auth, etc.)
    
    # Metadatos
    location = Column(String)  # Ubicación de la perrera
    contact_email = Column(String)
    contact_phone = Column(String)
    description = Column(Text)
    
    # Control de sincronización
    last_sync = Column(DateTime(timezone=True))
    sync_frequency_hours = Column(Integer, default=24)  # Frecuencia de sincronización en horas
    last_error = Column(Text)  # Último error de sincronización
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    external_dogs = relationship("ExternalDog", back_populates="external_shelter")

class ExternalDog(Base):
    """Modelo para perros obtenidos de fuentes externas"""
    __tablename__ = "external_dogs"
    
    id = Column(Integer, primary_key=True, index=True)
    external_shelter_id = Column(Integer, ForeignKey("external_shelters.id"), nullable=False)
    external_id = Column(String, nullable=False)  # ID único en la fuente externa
    
    # Datos del perro (similar al modelo Dog)
    name = Column(String, nullable=False)
    breed = Column(String)
    age = Column(Integer)  # Age in months
    size = Column(String)  # Mantenemos como string para mayor flexibilidad
    gender = Column(String)
    weight = Column(String)  # Como string para manejar diferentes formatos
    
    # Información adicional
    description = Column(Text)
    medical_info = Column(Text)
    behavior_notes = Column(Text)
    location = Column(String)
    
    # URLs y enlaces
    original_url = Column(String)  # URL original en la fuente
    photos = Column(JSON)  # Array de URLs de fotos
    
    # Control de estado
    is_available = Column(Boolean, default=True)
    last_seen = Column(DateTime(timezone=True), server_default=func.now())  # Última vez que se vio en la fuente
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    external_shelter = relationship("ExternalShelter", back_populates="external_dogs")
    
    __table_args__ = (
        UniqueConstraint('external_shelter_id', 'external_id', name='unique_external_dog'),
    )
