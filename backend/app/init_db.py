from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserType
from app.models.dog import Dog, DogStatus, DogSize, DogGender
import json

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)

def create_sample_data():
    """Create sample data for development"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Sample data already exists")
            return
        
        # Create sample users
        users_data = [
            {
                "email": "admin@fosterdogs.com",
                "name": "Admin FosterDogs",
                "user_type": UserType.ADMIN,
                "password": "admin123",
                "location": "Madrid",
                "phone": "+34 600 000 001"
            },
            {
                "email": "refugio@madrid.com",
                "name": "Refugio Madrid",
                "user_type": UserType.SHELTER,
                "password": "refugio123",
                "location": "Madrid",
                "phone": "+34 600 000 002"
            },
            {
                "email": "familia@gmail.com",
                "name": "María García",
                "user_type": UserType.FOSTER,
                "password": "familia123",
                "location": "Barcelona",
                "phone": "+34 600 000 003"
            }
        ]
        
        created_users = []
        for user_data in users_data:
            password = user_data.pop("password")
            user = User(
                **user_data,
                hashed_password=get_password_hash(password),
                is_active=True,
                is_verified=True
            )
            db.add(user)
            created_users.append(user)
        
        db.commit()
        
        # Refresh to get IDs
        for user in created_users:
            db.refresh(user)
        
        # Create sample dogs
        dogs_data = [
            {
                "name": "Luna",
                "breed": "Labrador Mix",
                "age": 24,  # 2 years in months
                "size": DogSize.LARGE,
                "gender": DogGender.FEMALE,
                "weight": 25.0,
                "location": "Madrid",
                "description": "Luna es una perrita muy cariñosa que busca una familia que la ame. Le encanta jugar y es muy obediente.",
                "medical_info": "Vacunada y esterilizada. Necesita revisiones veterinarias regulares.",
                "behavior_notes": "Muy sociable con personas y otros perros. Le gusta pasear y jugar en el parque.",
                "status": DogStatus.AVAILABLE,
                "good_with_kids": True,
                "good_with_dogs": True,
                "good_with_cats": False,
                "needs_yard": True,
                "owner_id": created_users[1].id,  # Refugio Madrid
                "photos": json.dumps([])
            },
            {
                "name": "Max",
                "breed": "Pastor Alemán",
                "age": 36,  # 3 years in months
                "size": DogSize.LARGE,
                "gender": DogGender.MALE,
                "weight": 30.0,
                "location": "Barcelona",
                "description": "Max es un perro muy inteligente y leal, perfecto para familias activas que buscan un compañero fiel.",
                "medical_info": "Vacunado. Necesita ejercicio diario para mantener su bienestar.",
                "behavior_notes": "Excelente perro guardián, muy protector pero cariñoso con su familia.",
                "status": DogStatus.AVAILABLE,
                "good_with_kids": True,
                "good_with_dogs": False,
                "good_with_cats": False,
                "needs_yard": True,
                "owner_id": created_users[1].id,  # Refugio Madrid
                "photos": json.dumps([])
            },
            {
                "name": "Coco",
                "breed": "French Bulldog",
                "age": 12,  # 1 year in months
                "size": DogSize.SMALL,
                "gender": DogGender.MALE,
                "weight": 12.0,
                "location": "Valencia",
                "description": "Coco es un cachorro juguetón que adora a los niños y se adapta perfectamente a la vida en apartamento.",
                "medical_info": "Vacunado. Pendiente de esterilización por edad.",
                "behavior_notes": "Muy energético y cariñoso. Le gusta estar siempre cerca de las personas.",
                "status": DogStatus.FOSTERED,
                "good_with_kids": True,
                "good_with_dogs": True,
                "good_with_cats": True,
                "needs_yard": False,
                "owner_id": created_users[1].id,  # Refugio Madrid
                "photos": json.dumps([])
            },
            {
                "name": "Bella",
                "breed": "Golden Retriever",
                "age": 48,  # 4 years in months
                "size": DogSize.LARGE,
                "gender": DogGender.FEMALE,
                "weight": 28.0,
                "location": "Sevilla",
                "description": "Bella es perfecta para familias con niños, muy paciente y cariñosa. Una verdadera compañera de vida.",
                "medical_info": "Vacunada y esterilizada. Excelente salud.",
                "behavior_notes": "Extremadamente dulce y paciente. Ideal para familias con niños pequeños.",
                "status": DogStatus.AVAILABLE,
                "good_with_kids": True,
                "good_with_dogs": True,
                "good_with_cats": True,
                "needs_yard": True,
                "owner_id": created_users[1].id,  # Refugio Madrid
                "photos": json.dumps([])
            },
        ]
        
        for dog_data in dogs_data:
            dog = Dog(**dog_data)
            db.add(dog)
        
        db.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def init_database():
    """Initialize database with tables and sample data"""
    print("Creating database tables...")
    create_tables()
    print("Creating sample data...")
    create_sample_data()
    print("Database initialization complete!")

if __name__ == "__main__":
    init_database()