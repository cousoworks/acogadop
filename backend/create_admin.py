#!/usr/bin/env python3
"""
Script to create an admin user for the FosterDogs platform.
"""

import sys

# Add the current directory to the Python path
sys.path.append('/app')

from app.core.database import get_db
from app.models.user import User, UserType
from app.core.security import get_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings

def create_admin_user():
    """Create the initial admin user"""
    
    # Create database connection
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.email == 'admin@acogadop.com').first()
        
        if admin_user:
            print('⚠️ El usuario administrador ya existe')
            print(f'📧 Email: admin@acogadop.com')
            print('🔑 Para cambiar la contraseña, usa el panel de admin en la web')
            return True
        
        # Create admin user
        admin_user = User(
            email='admin@acogadop.com',
            hashed_password=get_password_hash('admin123'),
            name='Administrador Principal',
            user_type=UserType.ADMIN,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        
        print('✅ Usuario administrador creado exitosamente!')
        print('📧 Email: admin@acogadop.com')
        print('🔑 Contraseña: admin123')
        print('⚠️ IMPORTANTE: Cambia esta contraseña después del primer login')
        print('')
        print('🎯 Accede al panel de administración en:')
        print('   http://localhost:3000/admin')
        print('')
        print('💡 Desde allí podrás:')
        print('   - Gestionar todos los usuarios')
        print('   - Aprobar perreras')
        print('   - Ver estadísticas del sistema')
        print('   - Configurar integraciones externas')
        
        return True
        
    except Exception as e:
        print(f'❌ Error creando usuario administrador: {e}')
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Creando usuario administrador...")
    print("=" * 50)
    success = create_admin_user()
    if success:
        print("=" * 50)
        print("🎉 ¡Configuración completada!")
    else:
        sys.exit(1)
