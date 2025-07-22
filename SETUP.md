# 🚀 Guía de Configuración - FosterDogs

Esta guía te ayudará a configurar y ejecutar la plataforma FosterDogs en tu entorno local.

## ✅ Verificación de Requisitos

Antes de comenzar, asegúrate de tener instalado:

- **Docker Desktop** (versión 4.0 o superior)
- **Docker Compose** (incluido con Docker Desktop)
- **Git** para clonar el repositorio

### Verificar instalación
```bash
docker --version
docker-compose --version
git --version
```

## 🏁 Inicio Rápido (5 minutos)

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd foster-dogs
```

### 2. Configuración inicial
```bash
# Hacer el script de desarrollo ejecutable
chmod +x dev-scripts.sh

# Ejecutar configuración automática
./dev-scripts.sh setup
```

### 3. ¡Listo! 🎉
- **Frontend:** http://localhost
- **API:** http://localhost/api/docs
- **Backend directo:** http://localhost:8000

## 📋 Comandos de Desarrollo

### Usar el script de desarrollo
```bash
# Ver todos los comandos disponibles
./dev-scripts.sh help

# Inicializar el proyecto
./dev-scripts.sh setup

# Iniciar servicios
./dev-scripts.sh start

# Ver logs en tiempo real
./dev-scripts.sh logs-f

# Acceder al shell del backend
./dev-scripts.sh shell-be

# Reiniciar servicios
./dev-scripts.sh restart

# Limpiar todo y empezar de cero
./dev-scripts.sh clean
```

### Comandos Docker Compose directos
```bash
# Construir e iniciar
docker-compose up --build

# Iniciar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar servicios
docker-compose down

# Reiniciar un servicio específico
docker-compose restart backend
docker-compose restart frontend
```

## 🗄️ Base de Datos

### Inicializar con datos de ejemplo
```bash
./dev-scripts.sh init-db
```

### Usuarios de prueba creados automáticamente:
```
👨‍💼 Admin:
Email: admin@fosterdogs.com
Password: admin123

🏠 Refugio:
Email: refugio@madrid.com
Password: refugio123

👨‍👩‍👧‍👦 Familia:
Email: familia@gmail.com
Password: familia123
```

### Resetear base de datos
```bash
./dev-scripts.sh reset-db
```

## 🔧 Desarrollo

### Frontend (React + Vite)
```bash
# Acceder al contenedor
./dev-scripts.sh shell-fe

# O desarrollo local
cd frontend
npm install
npm run dev
```

### Backend (FastAPI)
```bash
# Acceder al contenedor
./dev-scripts.sh shell-be

# O desarrollo local
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🌐 URLs de Desarrollo

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | http://localhost | Aplicación React |
| Backend API | http://localhost/api | API REST |
| API Docs | http://localhost/api/docs | Documentación Swagger |
| Backend directo | http://localhost:8000 | FastAPI directo |

## 📁 Estructura del Proyecto

```
foster-dogs/
├── 🎨 frontend/           # React + Vite + TailwindCSS
│   ├── src/
│   │   ├── components/    # Componentes UI
│   │   ├── pages/        # Páginas de la app
│   │   ├── contexts/     # Context providers
│   │   ├── services/     # API calls
│   │   └── hooks/        # Custom hooks
│   ├── public/           # Assets estáticos
│   └── Dockerfile.dev    # Container desarrollo
├── 🛠️ backend/           # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── core/         # Config y database
│   │   ├── models/       # Modelos de datos
│   │   ├── schemas/      # Validación Pydantic
│   │   ├── routers/      # Endpoints API
│   │   └── init_db.py    # Script inicialización
│   ├── uploads/          # Archivos subidos
│   └── Dockerfile.dev    # Container desarrollo
├── 🐳 docker-compose.yml # Orquestación completa
├── 🔧 dev-scripts.sh     # Scripts de desarrollo
└── 📖 README.md          # Documentación
```

## 🐛 Solución de Problemas

### El frontend no carga
```bash
# Verificar logs
./dev-scripts.sh logs-fe

# Reiniciar solo el frontend
docker-compose restart frontend
```

### El backend no responde
```bash
# Verificar logs
./dev-scripts.sh logs-be

# Verificar que la DB existe
./dev-scripts.sh shell-be
ls -la *.db

# Reinicializar DB si es necesario
./dev-scripts.sh reset-db
```

### Problemas de puertos
```bash
# Verificar qué está usando los puertos
netstat -tulpn | grep :80
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000

# Parar servicios que puedan estar en conflicto
./dev-scripts.sh stop
```

### Hot reload no funciona
```bash
# En macOS/Windows, Docker Desktop necesita:
# Settings > General > "Use file sharing implementation based on Virtualization framework"
# Activado

# Verificar volúmenes en docker-compose.yml
docker-compose down
docker-compose up --build
```

### Permisos en Linux
```bash
# Si hay problemas de permisos con archivos
sudo chown -R $USER:$USER .
chmod +x dev-scripts.sh
```

## 🚀 Pasar a Producción

### Variables de entorno de producción
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con valores seguros
nano .env
```

### Construir para producción
```bash
# Frontend
cd frontend
npm run build

# Backend (no requiere build especial)
# Usar uvicorn con configuración de producción
```

## 📝 Comandos Útiles

```bash
# Ver estado de todos los contenedores
./dev-scripts.sh status

# Acceder a la base de datos SQLite
./dev-scripts.sh shell-be
sqlite3 foster_dogs.db
.tables
.schema users

# Ver logs específicos
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx

# Limpiar espacio de Docker
docker system prune -af
docker volume prune -f
```

## ✨ Características Implementadas

- ✅ **Autenticación JWT** completa
- ✅ **CRUD de perros** con validación
- ✅ **Sistema de acogida** con aplicaciones
- ✅ **Búsqueda avanzada** por múltiples criterios
- ✅ **Interfaz responsive** mobile-first
- ✅ **Hot reload** para desarrollo
- ✅ **Base de datos** con datos de ejemplo
- ✅ **API documentada** con Swagger
- ✅ **Docker compose** completo
- ✅ **Scripts de desarrollo** automatizados

## 🔄 Flujo de Desarrollo Recomendado

1. **Hacer cambios** en el código
2. **Ver logs** con `./dev-scripts.sh logs-f`
3. **Probar en navegador** http://localhost
4. **Reiniciar servicios** si es necesario
5. **Confirmar cambios** con git

---

¿Necesitas ayuda? Revisa el [README.md](README.md) o abre un issue en GitHub.