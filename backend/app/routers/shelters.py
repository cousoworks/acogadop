from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User, UserType, ShelterStatus
from app.schemas.user import ShelterRegistration, ShelterApplicationResponse, ShelterApproval, UserResponse
from app.core.security import get_password_hash, create_access_token

router = APIRouter()

@router.post("/shelters/register", response_model=dict)
async def register_shelter(shelter_data: ShelterRegistration, db: Session = Depends(get_db)):
    """Registro de perreras - requiere aprobación del administrador"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == shelter_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new shelter user with pending status
    hashed_password = get_password_hash(shelter_data.password)
    db_user = User(
        email=shelter_data.email,
        name=shelter_data.name,
        phone=shelter_data.phone,
        location=shelter_data.location,
        user_type=UserType.SHELTER,
        hashed_password=hashed_password,
        shelter_name=shelter_data.shelter_name,
        shelter_license=shelter_data.shelter_license,
        shelter_address=shelter_data.shelter_address,
        shelter_website=shelter_data.shelter_website,
        shelter_description=shelter_data.shelter_description,
        shelter_status=ShelterStatus.PENDING,
        is_active=False  # Inactive until approved
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "message": "Shelter registration submitted successfully. Your application will be reviewed by an administrator.",
        "user_id": db_user.id,
        "status": "pending_approval"
    }

@router.get("/shelters/pending", response_model=List[ShelterApplicationResponse])
async def get_pending_shelters(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener perreras pendientes de aprobación - solo administradores"""
    
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can view pending shelter applications"
        )
    
    pending_shelters = db.query(User).filter(
        User.user_type == UserType.SHELTER,
        User.shelter_status == ShelterStatus.PENDING
    ).all()
    
    return [ShelterApplicationResponse.from_orm(shelter) for shelter in pending_shelters]

@router.post("/shelters/approve", response_model=dict)
async def approve_shelter(
    approval_data: ShelterApproval,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Aprobar o rechazar una perrera - solo administradores"""
    
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can approve shelter applications"
        )
    
    # Find the shelter user
    shelter_user = db.query(User).filter(User.id == approval_data.user_id).first()
    if not shelter_user or shelter_user.user_type != UserType.SHELTER:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shelter application not found"
        )
    
    if approval_data.approved:
        # Approve the shelter
        shelter_user.shelter_status = ShelterStatus.APPROVED
        shelter_user.user_type = UserType.SHELTER_ADMIN
        shelter_user.is_active = True
        shelter_user.is_verified = True
        message = f"Shelter '{shelter_user.shelter_name}' has been approved"
    else:
        # Reject the shelter
        shelter_user.shelter_status = ShelterStatus.REJECTED
        message = f"Shelter '{shelter_user.shelter_name}' has been rejected"
    
    # Add admin notes if provided
    if approval_data.admin_notes:
        shelter_user.admin_notes = approval_data.admin_notes
    
    db.commit()
    
    return {
        "message": message,
        "user_id": shelter_user.id,
        "approved": approval_data.approved
    }

@router.get("/shelters/approved", response_model=List[UserResponse])
async def get_approved_shelters(db: Session = Depends(get_db)):
    """Obtener perreras aprobadas - público"""
    
    approved_shelters = db.query(User).filter(
        User.user_type == UserType.SHELTER_ADMIN,
        User.shelter_status == ShelterStatus.APPROVED,
        User.is_active == True
    ).all()
    
    return [UserResponse.from_orm(shelter) for shelter in approved_shelters]

@router.get("/shelters/my-status", response_model=dict)
async def get_my_shelter_status(
    current_user: User = Depends(get_current_user)
):
    """Obtener el estado de la solicitud de perrera del usuario actual"""
    
    if current_user.user_type not in [UserType.SHELTER, UserType.SHELTER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not a shelter"
        )
    
    return {
        "user_id": current_user.id,
        "shelter_name": current_user.shelter_name,
        "status": current_user.shelter_status.value if current_user.shelter_status else "unknown",
        "is_active": current_user.is_active,
        "admin_notes": current_user.admin_notes,
        "can_manage_dogs": current_user.user_type == UserType.SHELTER_ADMIN and current_user.is_active
    }
