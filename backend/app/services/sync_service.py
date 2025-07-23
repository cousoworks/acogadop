from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.models.external_shelter import ExternalShelter, ExternalShelterType, ExternalShelterStatus
from app.services.web_scraper import WebScraper
from app.services.feed_scrapers import RSSFeedScraper, APIScraper
from app.schemas.external_shelter import SyncResult
from datetime import datetime, timedelta
import logging
import asyncio

logger = logging.getLogger(__name__)

class SyncService:
    """Service to manage synchronization of external shelters"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def sync_shelter(self, shelter_id: int) -> SyncResult:
        """Sync a specific shelter"""
        
        shelter = self.db.query(ExternalShelter).filter(
            ExternalShelter.id == shelter_id
        ).first()
        
        if not shelter:
            raise ValueError(f"Shelter with ID {shelter_id} not found")
        
        if shelter.status != ExternalShelterStatus.ACTIVE:
            raise ValueError(f"Shelter {shelter.name} is not active")
        
        # Get appropriate scraper
        scraper = self._get_scraper(shelter)
        
        # Perform sync
        result = await scraper.sync()
        
        return result
    
    async def sync_all_due_shelters(self) -> List[SyncResult]:
        """Sync all shelters that are due for synchronization"""
        
        now = datetime.utcnow()
        results = []
        
        # Get shelters that need syncing
        due_shelters = self.db.query(ExternalShelter).filter(
            ExternalShelter.status == ExternalShelterStatus.ACTIVE,
            (ExternalShelter.last_sync.is_(None)) | 
            (ExternalShelter.last_sync < now - timedelta(hours=ExternalShelter.sync_frequency_hours))
        ).all()
        
        logger.info(f"Found {len(due_shelters)} shelters due for sync")
        
        # Sync each shelter
        for shelter in due_shelters:
            try:
                result = await self.sync_shelter(shelter.id)
                results.append(result)
                
                # Add delay between syncs to be respectful
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Failed to sync shelter {shelter.name}: {str(e)}")
                
                # Create error result
                error_result = SyncResult(
                    shelter_id=shelter.id,
                    success=False,
                    dogs_found=0,
                    dogs_created=0,
                    dogs_updated=0,
                    dogs_marked_unavailable=0,
                    error=str(e),
                    sync_time=now
                )
                results.append(error_result)
        
        return results
    
    def _get_scraper(self, shelter: ExternalShelter):
        """Get appropriate scraper for shelter type"""
        
        if shelter.integration_type == ExternalShelterType.SCRAPER:
            return WebScraper(shelter, self.db)
        elif shelter.integration_type == ExternalShelterType.RSS:
            return RSSFeedScraper(shelter, self.db)
        elif shelter.integration_type == ExternalShelterType.API:
            return APIScraper(shelter, self.db)
        else:
            raise ValueError(f"Unknown integration type: {shelter.integration_type}")
    
    async def test_shelter_connection(self, shelter_id: int) -> Dict[str, Any]:
        """Test connection to a shelter without performing full sync"""
        
        shelter = self.db.query(ExternalShelter).filter(
            ExternalShelter.id == shelter_id
        ).first()
        
        if not shelter:
            raise ValueError(f"Shelter with ID {shelter_id} not found")
        
        try:
            scraper = self._get_scraper(shelter)
            
            # Try to fetch just a few dogs to test connection
            dogs_data = await scraper.fetch_dogs()
            
            return {
                "success": True,
                "message": f"Successfully connected to {shelter.name}",
                "dogs_found": len(dogs_data),
                "test_time": datetime.utcnow()
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to connect to {shelter.name}: {str(e)}",
                "dogs_found": 0,
                "test_time": datetime.utcnow(),
                "error": str(e)
            }
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get overall sync status for all shelters"""
        
        all_shelters = self.db.query(ExternalShelter).all()
        
        status = {
            "total_shelters": len(all_shelters),
            "active_shelters": 0,
            "inactive_shelters": 0,
            "error_shelters": 0,
            "last_successful_syncs": {},
            "shelters_due_for_sync": 0
        }
        
        now = datetime.utcnow()
        
        for shelter in all_shelters:
            if shelter.status == ExternalShelterStatus.ACTIVE:
                status["active_shelters"] += 1
                
                # Check if due for sync
                if (not shelter.last_sync or 
                    shelter.last_sync < now - timedelta(hours=shelter.sync_frequency_hours)):
                    status["shelters_due_for_sync"] += 1
                
                # Record last successful sync
                if shelter.last_sync and not shelter.last_error:
                    status["last_successful_syncs"][shelter.name] = shelter.last_sync
                    
            elif shelter.status == ExternalShelterStatus.INACTIVE:
                status["inactive_shelters"] += 1
            elif shelter.status == ExternalShelterStatus.ERROR:
                status["error_shelters"] += 1
        
        return status


# Background task functions for FastAPI
async def sync_all_shelters_task(db: Session):
    """Background task to sync all due shelters"""
    sync_service = SyncService(db)
    results = await sync_service.sync_all_due_shelters()
    
    logger.info(f"Completed sync for {len(results)} shelters")
    return results

async def sync_single_shelter_task(shelter_id: int, db: Session):
    """Background task to sync a single shelter"""
    sync_service = SyncService(db)
    result = await sync_service.sync_shelter(shelter_id)
    
    logger.info(f"Completed sync for shelter {shelter_id}")
    return result
