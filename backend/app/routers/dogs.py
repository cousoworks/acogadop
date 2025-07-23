from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.dog import Dog
from app.models.user import User, UserType
from app.models.external_shelter import ExternalDog
from app.schemas.dog import DogCreate, DogResponse, DogUpdate
from app.schemas.external_shelter import ExternalDogResponse
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[DogResponse])
async def get_dogs(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    breed: Optional[str] = None,
    size: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Dog)
    
    if status:
        query = query.filter(Dog.status == status)
    if breed:
        query = query.filter(Dog.breed.ilike(f"%{breed}%"))
    if size:
        query = query.filter(Dog.size == size)
    if location:
        query = query.filter(Dog.location.ilike(f"%{location}%"))
    
    dogs = query.offset(skip).limit(limit).all()
    return [DogResponse.from_orm(dog) for dog in dogs]

@router.get("/all", response_model=List[Union[DogResponse, ExternalDogResponse]])
async def get_all_dogs(
    skip: int = 0,
    limit: int = 20,
    breed: Optional[str] = None,
    size: Optional[str] = None,
    location: Optional[str] = None,
    include_external: bool = True,
    db: Session = Depends(get_db)
):
    """Get all dogs (local and external) with unified filtering"""
    
    all_dogs = []
    
    # Get local dogs
    local_query = db.query(Dog).filter(Dog.status == "available")
    
    if breed:
        local_query = local_query.filter(Dog.breed.ilike(f"%{breed}%"))
    if size:
        local_query = local_query.filter(Dog.size == size)
    if location:
        local_query = local_query.filter(Dog.location.ilike(f"%{location}%"))
    
    local_dogs = local_query.offset(skip).limit(limit).all()
    all_dogs.extend([{"type": "local", "data": DogResponse.from_orm(dog)} for dog in local_dogs])
    
    # Get external dogs if requested
    if include_external:
        external_query = db.query(ExternalDog).filter(ExternalDog.is_available == True)
        
        if breed:
            external_query = external_query.filter(ExternalDog.breed.ilike(f"%{breed}%"))
        if size:
            external_query = external_query.filter(ExternalDog.size.ilike(f"%{size}%"))
        if location:
            external_query = external_query.filter(ExternalDog.location.ilike(f"%{location}%"))
        
        remaining_limit = max(0, limit - len(local_dogs))
        external_dogs = external_query.offset(0).limit(remaining_limit).all()
        all_dogs.extend([{"type": "external", "data": ExternalDogResponse.from_orm(dog)} for dog in external_dogs])
    
    # Sort by creation date (newest first)
    all_dogs.sort(key=lambda x: x["data"].created_at, reverse=True)
    
    return [dog["data"] for dog in all_dogs[:limit]]

@router.get("/{dog_id}", response_model=DogResponse)
async def get_dog(dog_id: int, db: Session = Depends(get_db)):
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dog not found"
        )
    return DogResponse.from_orm(dog)

@router.post("/", response_model=DogResponse)
async def create_dog(
    dog_data: DogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if user can create dogs (shelter_admin or admin)
    if current_user.user_type not in [UserType.SHELTER_ADMIN, UserType.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only approved shelters and administrators can add dogs"
        )
    
    db_dog = Dog(
        **dog_data.dict(),
        owner_id=current_user.id
    )
    
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    
    return DogResponse.from_orm(db_dog)

@router.put("/{dog_id}", response_model=DogResponse)
async def update_dog(
    dog_id: int,
    dog_update: DogUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dog not found"
        )
    
    # Check if user owns the dog or is admin
    if dog.owner_id != current_user.id and current_user.user_type not in [UserType.ADMIN, UserType.SHELTER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update fields
    update_data = dog_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dog, field, value)
    
    db.commit()
    db.refresh(dog)
    
    return DogResponse.from_orm(dog)

@router.delete("/{dog_id}")
async def delete_dog(
    dog_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dog not found"
        )
    
    # Check if user owns the dog or is admin
    if dog.owner_id != current_user.id and current_user.user_type not in [UserType.ADMIN, UserType.SHELTER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(dog)
    db.commit()
    
    return {"message": "Dog deleted successfully"}