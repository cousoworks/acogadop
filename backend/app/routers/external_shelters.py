from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User, UserType
from app.models.external_shelter import ExternalShelter, ExternalDog, ExternalShelterStatus
from app.schemas.external_shelter import (
    ExternalShelterCreate, ExternalShelterUpdate, ExternalShelterResponse,
    ExternalDogResponse, SyncResult
)

router = APIRouter()

def require_admin(current_user: User = Depends(get_current_user)):
    """Dependency to require admin access"""
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can manage external shelters"
        )
    return current_user

@router.post("/external-shelters", response_model=ExternalShelterResponse)
async def create_external_shelter(
    shelter_data: ExternalShelterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Crear una nueva perrera externa - solo administradores"""
    
    # Check if shelter with same website already exists
    existing_shelter = db.query(ExternalShelter).filter(
        ExternalShelter.website_url == shelter_data.website_url
    ).first()
    
    if existing_shelter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A shelter with this website URL already exists"
        )
    
    db_shelter = ExternalShelter(**shelter_data.dict())
    db.add(db_shelter)
    db.commit()
    db.refresh(db_shelter)
    
    return ExternalShelterResponse.from_orm(db_shelter)

@router.get("/external-shelters", response_model=List[ExternalShelterResponse])
async def get_external_shelters(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
    status_filter: Optional[ExternalShelterStatus] = None
):
    """Obtener todas las perreras externas - solo administradores"""
    
    query = db.query(ExternalShelter)
    
    if status_filter:
        query = query.filter(ExternalShelter.status == status_filter)
    
    shelters = query.all()
    return [ExternalShelterResponse.from_orm(shelter) for shelter in shelters]

@router.get("/external-shelters/{shelter_id}", response_model=ExternalShelterResponse)
async def get_external_shelter(
    shelter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Obtener una perrera externa específica - solo administradores"""
    
    shelter = db.query(ExternalShelter).filter(ExternalShelter.id == shelter_id).first()
    if not shelter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External shelter not found"
        )
    
    return ExternalShelterResponse.from_orm(shelter)

@router.put("/external-shelters/{shelter_id}", response_model=ExternalShelterResponse)
async def update_external_shelter(
    shelter_id: int,
    shelter_data: ExternalShelterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Actualizar una perrera externa - solo administradores"""
    
    shelter = db.query(ExternalShelter).filter(ExternalShelter.id == shelter_id).first()
    if not shelter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External shelter not found"
        )
    
    update_data = shelter_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(shelter, field, value)
    
    db.commit()
    db.refresh(shelter)
    
    return ExternalShelterResponse.from_orm(shelter)

@router.delete("/external-shelters/{shelter_id}")
async def delete_external_shelter(
    shelter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Eliminar una perrera externa - solo administradores"""
    
    shelter = db.query(ExternalShelter).filter(ExternalShelter.id == shelter_id).first()
    if not shelter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External shelter not found"
        )
    
    # Also delete all associated dogs
    db.query(ExternalDog).filter(ExternalDog.external_shelter_id == shelter_id).delete()
    db.delete(shelter)
    db.commit()
    
    return {"message": "External shelter deleted successfully"}

@router.get("/external-shelters/{shelter_id}/dogs", response_model=List[ExternalDogResponse])
async def get_external_shelter_dogs(
    shelter_id: int,
    db: Session = Depends(get_db),
    available_only: bool = True
):
    """Obtener perros de una perrera externa específica - público"""
    
    shelter = db.query(ExternalShelter).filter(ExternalShelter.id == shelter_id).first()
    if not shelter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External shelter not found"
        )
    
    query = db.query(ExternalDog).filter(ExternalDog.external_shelter_id == shelter_id)
    
    if available_only:
        query = query.filter(ExternalDog.is_available == True)
    
    dogs = query.all()
    return [ExternalDogResponse.from_orm(dog) for dog in dogs]

@router.get("/external-dogs", response_model=List[ExternalDogResponse])
async def get_all_external_dogs(
    db: Session = Depends(get_db),
    available_only: bool = True,
    limit: int = 50,
    offset: int = 0
):
    """Obtener todos los perros de perreras externas - público"""
    
    query = db.query(ExternalDog)
    
    if available_only:
        query = query.filter(ExternalDog.is_available == True)
    
    dogs = query.offset(offset).limit(limit).all()
    return [ExternalDogResponse.from_orm(dog) for dog in dogs]

@router.post("/external-shelters/{shelter_id}/sync", response_model=SyncResult)
async def sync_external_shelter(
    shelter_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Sincronizar una perrera externa manualmente - solo administradores"""
    
    shelter = db.query(ExternalShelter).filter(ExternalShelter.id == shelter_id).first()
    if not shelter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External shelter not found"
        )
    
    # Add sync task to background
    background_tasks.add_task(sync_shelter_data, shelter_id, db)
    
    return SyncResult(
        shelter_id=shelter_id,
        success=True,
        dogs_found=0,
        dogs_created=0,
        dogs_updated=0,
        dogs_marked_unavailable=0,
        sync_time=datetime.utcnow()
    )

@router.post("/external-shelters/sync-all")
async def sync_all_external_shelters(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Sincronizar todas las perreras externas - solo administradores"""
    
    active_shelters = db.query(ExternalShelter).filter(
        ExternalShelter.status == ExternalShelterStatus.ACTIVE
    ).all()
    
    for shelter in active_shelters:
        background_tasks.add_task(sync_shelter_data, shelter.id, db)
    
    return {
        "message": f"Sync started for {len(active_shelters)} shelters",
        "shelters_count": len(active_shelters)
    }

async def sync_shelter_data(shelter_id: int, db: Session):
    """Background task to sync shelter data"""
    try:
        shelter = db.query(ExternalShelter).filter(ExternalShelter.id == shelter_id).first()
        if not shelter:
            return
        
        # Update last sync time
        shelter.last_sync = datetime.utcnow()
        shelter.last_error = None
        
        # Here we would implement the actual scraping/API logic
        # For now, just mark as synced
        
        db.commit()
        
    except Exception as e:
        # Log error
        shelter = db.query(ExternalShelter).filter(ExternalShelter.id == shelter_id).first()
        if shelter:
            shelter.last_error = str(e)
            shelter.status = ExternalShelterStatus.ERROR
            db.commit()
