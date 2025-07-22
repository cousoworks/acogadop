from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.foster_application import FosterApplication
from app.models.dog import Dog
from app.models.user import User
from app.schemas.foster_application import (
    FosterApplicationCreate, 
    FosterApplicationResponse, 
    FosterApplicationUpdate
)
from app.routers.auth import get_current_user

router = APIRouter()

@router.post("/apply/{dog_id}", response_model=FosterApplicationResponse)
async def apply_for_foster(
    dog_id: int,
    application_data: FosterApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if dog exists
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dog not found"
        )
    
    # Check if user already applied for this dog
    existing_application = db.query(FosterApplication).filter(
        FosterApplication.user_id == current_user.id,
        FosterApplication.dog_id == dog_id
    ).first()
    
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this dog"
        )
    
    # Create application
    db_application = FosterApplication(
        user_id=current_user.id,
        dog_id=dog_id,
        message=application_data.message,
        experience=application_data.experience,
        living_situation=application_data.living_situation,
        availability=application_data.availability
    )
    
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    
    return FosterApplicationResponse.from_orm(db_application)

@router.get("/my-applications", response_model=List[FosterApplicationResponse])
async def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    applications = db.query(FosterApplication).filter(
        FosterApplication.user_id == current_user.id
    ).all()
    
    return [FosterApplicationResponse.from_orm(app) for app in applications]

@router.put("/{application_id}/status", response_model=FosterApplicationResponse)
async def update_application_status(
    application_id: int,
    status_update: FosterApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only admins and shelter owners can update application status
    if current_user.user_type.value not in ["admin", "shelter"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    application = db.query(FosterApplication).filter(
        FosterApplication.id == application_id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    application.status = status_update.status
    if status_update.admin_notes:
        application.admin_notes = status_update.admin_notes
    
    db.commit()
    db.refresh(application)
    
    return FosterApplicationResponse.from_orm(application)