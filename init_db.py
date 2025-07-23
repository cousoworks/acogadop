#!/usr/bin/env python3
"""
Script to initialize the database with new tables for shelter management and external integrations.
Run this script to create the new tables in your existing database.
"""

import sys
import os

# Add the backend directory to the Python path
# Check if we're running in Docker or locally
if os.path.exists('/app'):
    # Running in Docker container
    sys.path.append('/app')
else:
    # Running locally
    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from sqlalchemy import create_engine, text
    from app.core.config import settings
    from app.core.database import Base
    from app.models import User, Dog, FosterApplication, ExternalShelter, ExternalDog
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the correct directory or Docker container")
    sys.exit(1)

def create_tables():
    """Create new tables for shelter management and external integrations"""
    
    # Create engine
    engine = create_engine(settings.DATABASE_URL)
    
    print("Creating new tables...")
    
    try:
        # Create all tables (this will only create tables that don't exist)
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # Add any necessary initial data
        with engine.connect() as connection:
            # Check if we need to add any default data
            print("Database initialization completed!")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    return True

def add_sample_external_shelter():
    """Add a sample external shelter for testing"""
    
    from sqlalchemy.orm import sessionmaker
    from app.models.external_shelter import ExternalShelter, ExternalShelterType, ExternalShelterStatus
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if sample shelter already exists
        existing = db.query(ExternalShelter).filter(
            ExternalShelter.name == "Perrera Municipal Ejemplo"
        ).first()
        
        if existing:
            print("Sample external shelter already exists")
            return
        
        # Create sample external shelter
        sample_shelter = ExternalShelter(
            name="Perrera Municipal Ejemplo",
            website_url="https://example-shelter.com",
            integration_type=ExternalShelterType.SCRAPER,
            status=ExternalShelterStatus.INACTIVE,  # Inactive by default
            location="Madrid, España",
            contact_email="info@example-shelter.com",
            description="Perrera municipal de ejemplo para pruebas de integración",
            scraping_config={
                "listing_url": "https://example-shelter.com/dogs",
                "dog_url_selector": "a.dog-link",
                "selectors": {
                    "name": "h1.dog-name",
                    "breed": ".dog-breed",
                    "age": ".dog-age",
                    "size": ".dog-size",
                    "gender": ".dog-gender",
                    "description": ".dog-description",
                    "photos": "img.dog-photo"
                }
            },
            sync_frequency_hours=24
        )
        
        db.add(sample_shelter)
        db.commit()
        
        print("✅ Sample external shelter added successfully!")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🐕 FosterDogs Database Initialization")
    print("=" * 50)
    
    # Create tables
    if create_tables():
        print("\n📝 Adding sample data...")
        add_sample_external_shelter()
        
        print("\n🎉 Database initialization completed!")
        print("\nNext steps:")
        print("1. Start your backend server: cd backend && uvicorn app.main:app --reload")
        print("2. Start your frontend: cd frontend && npm start")
        print("3. Visit the admin panel to configure external shelters")
        print("4. Register as a shelter to test the approval workflow")
    else:
        print("\n❌ Database initialization failed!")
        sys.exit(1)
