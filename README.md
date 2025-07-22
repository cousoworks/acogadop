# 🐕 FosterDogs - Plataforma de Acogida y Adopción

Una plataforma web moderna para conectar perros en necesidad con familias acogedoras y adoptantes.

## 🚀 Características

### ✨ Funcionalidades Principales
- **Registro y autenticación** de usuarios (familias acogedoras, refugios, administradores)
- **Gestión de perros** con fichas completas (fotos, información médica, comportamiento)
- **Sistema de acogida** y adopción con seguimiento de aplicaciones
- **Búsqueda avanzada** por raza, tamaño, edad, ubicación y compatibilidad
- **Gestión de favoritos** para usuarios registrados
- **Panel de administración** para refugios y administradores
- **Generación de carteles** "Adóptame" descargables
- **Diseño responsive** y mobile-first

### 🛠 Stack Tecnológico

**Frontend:**
- React 18 + JavaScript
- Vite (build tool)
- TailwindCSS (styling)
- Framer Motion (animaciones)
- React Router (navegación)
- React Query (state management)
- Axios (HTTP client)
- React Hook Form (formularios)

**Backend:**
- Python 3.11
- FastAPI (framework web)
- SQLAlchemy (ORM)
- SQLite (base de datos)
- JWT (autenticación)
- Pydantic (validación)
- Uvicorn (servidor ASGI)

**DevOps:**
- Docker & Docker Compose
- Hot reload para desarrollo
- Nginx (proxy reverso)
- GitHub Actions (CI/CD)

## 🏗 Estructura del Proyecto

```
foster-dogs/
├── frontend/                 # React + Vite application
│   ├── src/
│   │   ├── components/      # Componentes reutilizables
│   │   ├── pages/          # Páginas de la aplicación
│   │   ├── contexts/       # Context providers (Auth, etc.)
│   │   ├── services/       # APIs y servicios
│   │   ├── hooks/          # Custom hooks
│   │   └── utils/          # Utilidades
│   ├── public/             # Assets estáticos
│   ├── Dockerfile.dev      # Docker para desarrollo
│   └── package.json
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── core/           # Configuración y database
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── routers/        # Endpoints API
│   │   └── services/       # Lógica de negocio
│   ├── uploads/            # Archivos subidos
│   ├── Dockerfile.dev      # Docker para desarrollo
│   └── requirements.txt
├── docker-compose.yml       # Orquestación completa
├── nginx.conf              # Configuración proxy
└── README.md
```

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker y Docker Compose
- Git

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd foster-dogs
```

### 2. Levantar con Docker
```bash
# Construir e iniciar todos los servicios
docker-compose up --build

# En modo detached (background)
docker-compose up -d --build
```

### 3. Inicializar la base de datos
```bash
# Ejecutar el script de inicialización (solo la primera vez)
docker-compose exec backend python app/init_db.py
```

### 4. Acceder a la aplicación
- **Frontend:** http://localhost (puerto 80)
- **Backend API:** http://localhost/api
- **Documentación API:** http://localhost/api/docs

## 👥 Usuarios de Prueba

Después de ejecutar el script de inicialización, tendrás estos usuarios:

```
Admin:
- Email: admin@fosterdogs.com
- Password: admin123

Refugio:
- Email: refugio@madrid.com
- Password: refugio123

Familia Acogedora:
- Email: familia@gmail.com
- Password: familia123
```

## 🛠 Desarrollo

### Frontend (React)
```bash
# Instalar dependencias
cd frontend
npm install

# Desarrollo sin Docker
npm run dev
```

### Backend (FastAPI)
```bash
# Crear entorno virtual
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Desarrollo sin Docker
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 🔄 Hot Reload
Los Dockerfiles están configurados para hot reload:
- **Frontend:** Cambios en `src/` se reflejan automáticamente
- **Backend:** Cambios en `app/` se reflejan automáticamente

### 📊 Base de Datos
```bash
# Recrear la base de datos
docker-compose exec backend python app/init_db.py

# Ver logs del backend
docker-compose logs backend

# Acceder al contenedor del backend
docker-compose exec backend bash
```

## 🌐 API Endpoints

### Autenticación
- `POST /auth/register` - Registro de usuario
- `POST /auth/login` - Inicio de sesión
- `GET /auth/me` - Información del usuario actual

### Perros
- `GET /dogs` - Listar perros con filtros
- `GET /dogs/{id}` - Obtener perro específico
- `POST /dogs` - Crear nuevo perro (requiere auth)
- `PUT /dogs/{id}` - Actualizar perro (requiere auth)
- `DELETE /dogs/{id}` - Eliminar perro (requiere auth)

### Acogida
- `POST /fosters/apply/{dog_id}` - Aplicar para acoger
- `GET /fosters/my-applications` - Mis aplicaciones
- `PUT /fosters/{id}/status` - Actualizar estado (admin/refugio)

### Búsqueda
- `GET /search/dogs` - Búsqueda avanzada de perros
- `GET /search/breeds` - Listar razas disponibles
- `GET /search/locations` - Listar ubicaciones

## 🎨 Diseño y UX

### Paleta de Colores
- **Primary:** Tonos naranjas cálidos (`#ed7a47`)
- **Secondary:** Azules confiables (`#0ea5e9`)
- **Accent:** Grises neutros para texto y fondos

### Principios de Diseño
- **Mobile-first:** Optimizado para dispositivos móviles
- **Accesibilidad:** Contrastes apropiados y navegación clara
- **Emocional:** Diseño que transmite calidez y confianza
- **Responsive:** Adaptación perfecta a todas las pantallas

## 🔧 Scripts Útiles

```bash
# Reiniciar solo el frontend
docker-compose restart frontend

# Reiniciar solo el backend
docker-compose restart backend

# Ver logs en tiempo real
docker-compose logs -f

# Limpiar y reconstruir
docker-compose down
docker-compose up --build

# Acceder a la base de datos SQLite
docker-compose exec backend sqlite3 foster_dogs.db
```

## 📈 Próximas Funcionalidades

- [ ] **Sistema de mensajería** entre usuarios
- [ ] **Calendario de eventos** de adopción
- [ ] **Geolocalización** para búsquedas por proximidad
- [ ] **Sistema de puntuación** y reviews
- [ ] **Notificaciones push** para móviles
- [ ] **Integración con redes sociales**
- [ ] **Dashboard de analytics** para administradores
- [ ] **API para aplicaciones móviles**

## 🤝 Contribuir

1. Fork del proyecto
2. Crear rama de feature (`git checkout -b feature/amazing-feature`)
3. Commit de cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

¿Problemas o preguntas? 
- Abrir un [issue](https://github.com/user/foster-dogs/issues)
- Contactar al equipo de desarrollo

---

**¡Gracias por ayudar a crear una plataforma que cambia vidas! 🐕❤️**
