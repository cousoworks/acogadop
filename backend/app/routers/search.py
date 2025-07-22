from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.dog import Dog
from app.schemas.dog import DogResponse

router = APIRouter()

@router.get("/dogs", response_model=List[DogResponse])
async def search_dogs(
    q: str = Query(None, description="Search query"),
    breed: str = Query(None, description="Filter by breed"),
    size: str = Query(None, description="Filter by size"),
    location: str = Query(None, description="Filter by location"),
    good_with_kids: bool = Query(None, description="Good with kids"),
    good_with_dogs: bool = Query(None, description="Good with dogs"),
    good_with_cats: bool = Query(None, description="Good with cats"),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(Dog)
    
    # Text search
    if q:
        query = query.filter(
            Dog.name.ilike(f"%{q}%") | 
            Dog.breed.ilike(f"%{q}%") |
            Dog.description.ilike(f"%{q}%")
        )
    
    # Filters
    if breed:
        query = query.filter(Dog.breed.ilike(f"%{breed}%"))
    if size:
        query = query.filter(Dog.size == size)
    if location:
        query = query.filter(Dog.location.ilike(f"%{location}%"))
    if good_with_kids is not None:
        query = query.filter(Dog.good_with_kids == good_with_kids)
    if good_with_dogs is not None:
        query = query.filter(Dog.good_with_dogs == good_with_dogs)
    if good_with_cats is not None:
        query = query.filter(Dog.good_with_cats == good_with_cats)
    
    dogs = query.offset(skip).limit(limit).all()
    return [DogResponse.from_orm(dog) for dog in dogs]

@router.get("/breeds")
async def get_breeds(db: Session = Depends(get_db)):
    breeds = db.query(Dog.breed).distinct().filter(Dog.breed.isnot(None)).all()
    return [breed[0] for breed in breeds if breed[0]]

@router.get("/locations")
async def get_locations(
    q: str = Query(None, description="Search query for locations"),
    db: Session = Depends(get_db)
):
    query = db.query(Dog.location).distinct().filter(Dog.location.isnot(None))
    
    if q:
        query = query.filter(Dog.location.ilike(f"%{q}%"))
    
    locations = query.all()
    return [location[0] for location in locations if location[0]]