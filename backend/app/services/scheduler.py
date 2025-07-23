from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.sync_service import sync_all_shelters_task
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    """Service to manage scheduled tasks"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        
    def start(self):
        """Start the scheduler"""
        try:
            # Schedule daily sync at 2 AM
            self.scheduler.add_job(
                self._daily_sync_job,
                CronTrigger(hour=2, minute=0),
                id="daily_shelter_sync",
                name="Daily External Shelter Sync",
                replace_existing=True
            )
            
            # Schedule sync every 6 hours for high-priority shelters
            self.scheduler.add_job(
                self._frequent_sync_job,
                CronTrigger(hour="*/6"),
                id="frequent_shelter_sync",
                name="Frequent External Shelter Sync",
                replace_existing=True
            )
            
            self.scheduler.start()
            logger.info("Scheduler started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start scheduler: {str(e)}")
    
    def stop(self):
        """Stop the scheduler"""
        try:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped successfully")
        except Exception as e:
            logger.error(f"Failed to stop scheduler: {str(e)}")
    
    async def _daily_sync_job(self):
        """Daily sync job for all shelters"""
        logger.info("Starting daily shelter sync job")
        
        try:
            # Get database session
            db = next(get_db())
            
            # Run sync
            results = await sync_all_shelters_task(db)
            
            # Log results
            success_count = sum(1 for r in results if r.success)
            error_count = len(results) - success_count
            
            logger.info(f"Daily sync completed: {success_count} successful, {error_count} errors")
            
        except Exception as e:
            logger.error(f"Daily sync job failed: {str(e)}")
        finally:
            db.close()
    
    async def _frequent_sync_job(self):
        """Frequent sync job for high-priority shelters"""
        logger.info("Starting frequent shelter sync job")
        
        try:
            # This could be customized to only sync certain high-priority shelters
            db = next(get_db())
            
            # For now, just run the regular sync
            results = await sync_all_shelters_task(db)
            
            success_count = sum(1 for r in results if r.success)
            logger.info(f"Frequent sync completed: {success_count} shelters synced")
            
        except Exception as e:
            logger.error(f"Frequent sync job failed: {str(e)}")
        finally:
            db.close()
    
    def add_custom_job(self, func, trigger, job_id: str, name: str):
        """Add a custom job to the scheduler"""
        try:
            self.scheduler.add_job(
                func,
                trigger,
                id=job_id,
                name=name,
                replace_existing=True
            )
            logger.info(f"Added custom job: {name}")
        except Exception as e:
            logger.error(f"Failed to add custom job {name}: {str(e)}")
    
    def remove_job(self, job_id: str):
        """Remove a job from the scheduler"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Removed job: {job_id}")
        except Exception as e:
            logger.error(f"Failed to remove job {job_id}: {str(e)}")
    
    def get_jobs(self):
        """Get all scheduled jobs"""
        return self.scheduler.get_jobs()

# Global scheduler instance
scheduler_service = SchedulerService()
