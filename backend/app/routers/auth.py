from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func
from jose import JWTError, jwt
from typing import List, Optional
from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.config import settings
from app.models.user import User, UserType, ShelterStatus
from app.models.dog import Dog
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate

router = APIRouter()
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=dict)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        name=user_data.name,
        phone=user_data.phone,
        location=user_data.location,
        user_type=user_data.user_type,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token = create_access_token(subject=db_user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(db_user)
    }

@router.post("/login", response_model=dict)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is deactivated"
        )
    
    # Create access token
    access_token = create_access_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse.from_orm(current_user)

# ===== ADMIN ROUTES FOR USER MANAGEMENT =====

def require_admin(current_user: User = Depends(get_current_user)):
    """Dependency to require admin access"""
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this resource"
        )
    return current_user

@router.get("/admin/users", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    user_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all users with filtering - Admin only"""
    
    query = db.query(User)
    
    # Search by name or email
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (User.name.ilike(search_term)) | 
            (User.email.ilike(search_term))
        )
    
    # Filter by user type
    if user_type:
        try:
            user_type_enum = UserType(user_type)
            query = query.filter(User.user_type == user_type_enum)
        except ValueError:
            pass
    
    # Order by creation date (newest first)
    query = query.order_by(User.created_at.desc())
    
    users = query.offset(skip).limit(limit).all()
    return [UserResponse.from_orm(user) for user in users]

@router.get("/admin/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get a specific user by ID - Admin only"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.from_orm(user)

@router.put("/admin/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update a user - Admin only"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from demoting themselves
    if user.id == current_user.id and user_update.user_type and user_update.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot change your own admin status"
        )
    
    # Update fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "password" and value:
            # Hash password if provided
            setattr(user, "hashed_password", get_password_hash(value))
        else:
            setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return UserResponse.from_orm(user)

@router.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete a user - Admin only"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own account"
        )
    
    # Prevent deleting the main admin account
    if user.email == "admin@acogadop.com":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete the main admin account"
        )
    
    # Store user info for response
    user_info = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
    
    # Delete related data first (if any foreign key constraints)
    from app.models.foster_application import FosterApplication
    from app.models.dog import Dog
    
    # Delete foster applications
    foster_applications = db.query(FosterApplication).filter(FosterApplication.user_id == user_id).all()
    for application in foster_applications:
        db.delete(application)
    
    # If user is a shelter, handle their dogs
    dogs = []
    if user.user_type in [UserType.SHELTER, UserType.SHELTER_ADMIN]:
        # Reassign dogs to no owner (orphaned) or handle as needed
        dogs = db.query(Dog).filter(Dog.owner_id == user_id).all()
        for dog in dogs:
            dog.owner_id = None  # Mark as orphaned
    
    db.delete(user)
    db.commit()
    
    return {
        "message": f"User '{user_info['name']}' ({user_info['email']}) deleted successfully",
        "deleted_user": user_info,
        "related_data_deleted": {
            "foster_applications": len(foster_applications),
            "dogs_affected": len(dogs)
        }
    }

@router.post("/admin/users/{user_id}/toggle-status")
async def toggle_user_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Toggle user active status - Admin only"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deactivating themselves
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot change your own status"
        )
    
    user.is_active = not user.is_active
    db.commit()
    
    status_text = "activated" if user.is_active else "deactivated"
    
    return {
        "message": f"User '{user.name}' has been {status_text}",
        "user_id": user.id,
        "is_active": user.is_active
    }

@router.get("/admin/stats")
async def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get admin dashboard statistics"""
    
    stats = {
        "total_users": db.query(User).count(),
        "active_users": db.query(User).filter(User.is_active == True).count(),
        "total_shelters": db.query(User).filter(User.user_type == UserType.SHELTER_ADMIN).count(),
        "pending_shelters": db.query(User).filter(
            User.user_type == UserType.SHELTER,
            User.shelter_status == ShelterStatus.PENDING
        ).count(),
        "total_dogs": db.query(Dog).count(),
        "available_dogs": db.query(Dog).filter(Dog.status == "available").count(),
    }
    
    # User type breakdown
    user_types = db.query(User.user_type, func.count(User.id)).group_by(User.user_type).all()
    stats["user_types"] = {user_type.value: count for user_type, count in user_types}
    
    return stats