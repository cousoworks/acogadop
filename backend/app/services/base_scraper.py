from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.external_shelter import ExternalShelter, ExternalDog
from app.schemas.external_shelter import SyncResult
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for all shelter scrapers"""
    
    def __init__(self, shelter: ExternalShelter, db: Session):
        self.shelter = shelter
        self.db = db
        self.dogs_found = 0
        self.dogs_created = 0
        self.dogs_updated = 0
        self.dogs_marked_unavailable = 0
        
    @abstractmethod
    async def fetch_dogs(self) -> List[Dict[str, Any]]:
        """Fetch dogs from the external source"""
        pass
    
    async def sync(self) -> SyncResult:
        """Main sync method"""
        try:
            logger.info(f"Starting sync for shelter {self.shelter.name}")
            
            # Fetch dogs from external source
            external_dogs_data = await self.fetch_dogs()
            self.dogs_found = len(external_dogs_data)
            
            # Track current external IDs to mark missing dogs as unavailable
            current_external_ids = set()
            
            # Process each dog
            for dog_data in external_dogs_data:
                external_id = dog_data.get('external_id')
                if not external_id:
                    continue
                    
                current_external_ids.add(external_id)
                
                # Check if dog already exists
                existing_dog = self.db.query(ExternalDog).filter(
                    ExternalDog.external_shelter_id == self.shelter.id,
                    ExternalDog.external_id == external_id
                ).first()
                
                if existing_dog:
                    # Update existing dog
                    self._update_dog(existing_dog, dog_data)
                    self.dogs_updated += 1
                else:
                    # Create new dog
                    self._create_dog(dog_data)
                    self.dogs_created += 1
            
            # Mark dogs as unavailable if they're no longer in the source
            self._mark_unavailable_dogs(current_external_ids)
            
            # Update shelter sync status
            self.shelter.last_sync = datetime.utcnow()
            self.shelter.last_error = None
            
            self.db.commit()
            
            logger.info(f"Sync completed for shelter {self.shelter.name}: "
                       f"{self.dogs_found} found, {self.dogs_created} created, "
                       f"{self.dogs_updated} updated, {self.dogs_marked_unavailable} marked unavailable")
            
            return SyncResult(
                shelter_id=self.shelter.id,
                success=True,
                dogs_found=self.dogs_found,
                dogs_created=self.dogs_created,
                dogs_updated=self.dogs_updated,
                dogs_marked_unavailable=self.dogs_marked_unavailable,
                sync_time=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Sync failed for shelter {self.shelter.name}: {str(e)}")
            
            # Update shelter error status
            self.shelter.last_error = str(e)
            self.shelter.status = "error"
            self.db.commit()
            
            return SyncResult(
                shelter_id=self.shelter.id,
                success=False,
                dogs_found=0,
                dogs_created=0,
                dogs_updated=0,
                dogs_marked_unavailable=0,
                error=str(e),
                sync_time=datetime.utcnow()
            )
    
    def _create_dog(self, dog_data: Dict[str, Any]):
        """Create a new external dog"""
        dog = ExternalDog(
            external_shelter_id=self.shelter.id,
            external_id=dog_data['external_id'],
            name=dog_data.get('name', 'Unknown'),
            breed=dog_data.get('breed'),
            age=self._parse_age(dog_data.get('age')),
            size=dog_data.get('size'),
            gender=dog_data.get('gender'),
            weight=dog_data.get('weight'),
            description=dog_data.get('description'),
            medical_info=dog_data.get('medical_info'),
            behavior_notes=dog_data.get('behavior_notes'),
            location=dog_data.get('location'),
            original_url=dog_data.get('original_url'),
            photos=dog_data.get('photos', []),
            is_available=True,
            last_seen=datetime.utcnow()
        )
        
        self.db.add(dog)
    
    def _update_dog(self, existing_dog: ExternalDog, dog_data: Dict[str, Any]):
        """Update an existing external dog"""
        existing_dog.name = dog_data.get('name', existing_dog.name)
        existing_dog.breed = dog_data.get('breed', existing_dog.breed)
        existing_dog.age = self._parse_age(dog_data.get('age')) or existing_dog.age
        existing_dog.size = dog_data.get('size', existing_dog.size)
        existing_dog.gender = dog_data.get('gender', existing_dog.gender)
        existing_dog.weight = dog_data.get('weight', existing_dog.weight)
        existing_dog.description = dog_data.get('description', existing_dog.description)
        existing_dog.medical_info = dog_data.get('medical_info', existing_dog.medical_info)
        existing_dog.behavior_notes = dog_data.get('behavior_notes', existing_dog.behavior_notes)
        existing_dog.location = dog_data.get('location', existing_dog.location)
        existing_dog.original_url = dog_data.get('original_url', existing_dog.original_url)
        existing_dog.photos = dog_data.get('photos', existing_dog.photos)
        existing_dog.is_available = True
        existing_dog.last_seen = datetime.utcnow()
    
    def _mark_unavailable_dogs(self, current_external_ids: set):
        """Mark dogs as unavailable if they're no longer in the source"""
        unavailable_dogs = self.db.query(ExternalDog).filter(
            ExternalDog.external_shelter_id == self.shelter.id,
            ExternalDog.is_available == True,
            ~ExternalDog.external_id.in_(current_external_ids)
        ).all()
        
        for dog in unavailable_dogs:
            dog.is_available = False
            self.dogs_marked_unavailable += 1
    
    def _parse_age(self, age_str: Optional[str]) -> Optional[int]:
        """Parse age string to months"""
        if not age_str:
            return None
            
        age_str = age_str.lower().strip()
        
        try:
            # Try to extract number
            import re
            numbers = re.findall(r'\d+', age_str)
            if not numbers:
                return None
                
            age_value = int(numbers[0])
            
            # Convert to months based on unit
            if 'año' in age_str or 'year' in age_str:
                return age_value * 12
            elif 'mes' in age_str or 'month' in age_str:
                return age_value
            elif 'semana' in age_str or 'week' in age_str:
                return max(1, age_value // 4)  # Convert weeks to months
            else:
                # Assume months if no unit specified
                return age_value
                
        except (ValueError, IndexError):
            return None
