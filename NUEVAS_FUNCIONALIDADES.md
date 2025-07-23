# 🐕 FosterDogs - Nuevas Funcionalidades

Este documento describe las nuevas funcionalidades implementadas para el proyecto FosterDogs:

Email: admin@acogadop.com
Contraseña: admin123

## 📋 Nuevas Funcionalidades

### 1. **Registro de Perreras sin Web**

- ✅ Sistema de registro para perreras que no tienen sitio web propio
- ✅ Flujo de aprobación por administrador
- ✅ Roles específicos para perreras aprobadas (`shelter_admin`)
- ✅ Capacidad de publicar, editar y eliminar anuncios de perros

### 2. **Integración con Perreras Externas**

- ✅ Sistema de scraping web para perreras con sitio web
- ✅ Soporte para APIs REST
- ✅ Soporte para feeds RSS
- ✅ Sincronización automática diaria
- ✅ Gestión de perros externos en base de datos separada

## 🏗️ Arquitectura Implementada

### Backend (FastAPI)

#### Nuevos Modelos:

- **User**: Extendido con campos para perreras (shelter_name, shelter_license, etc.)
- **ExternalShelter**: Gestión de perreras externas con configuración de integración
- **ExternalDog**: Almacenamiento de perros obtenidos de fuentes externas

#### Nuevas Rutas:

- `/api/shelters/register` - Registro de perreras
- `/api/shelters/pending` - Ver solicitudes pendientes (admin)
- `/api/shelters/approve` - Aprobar/rechazar perreras (admin)
- `/api/external-shelters/*` - Gestión de perreras externas
- `/dogs/all` - Lista combinada de perros locales y externos

#### Servicios:

- **SyncService**: Coordinación de sincronización
- **WebScraper**: Scraping de sitios web
- **APIScraper**: Integración con APIs
- **RSSFeedScraper**: Procesamiento de feeds RSS
- **SchedulerService**: Programación de tareas automáticas

### Frontend (React)

#### Nuevas Páginas:

- **ShelterRegister**: Formulario de registro para perreras
- **AdminPanel**: Panel de administración para gestionar solicitudes
- **AddDog**: Formulario mejorado para añadir perros (solo perreras aprobadas)

#### Actualizaciones:

- **Navbar**: Enlaces dinámicos basados en rol de usuario
- **Login**: Enlace para registro de perreras
- **App.jsx**: Nuevas rutas

## 🚀 Instalación y Configuración

### 1. Actualizar Dependencias

```bash
# Backend
cd backend
pip install -r requirements.txt
```

### 2. Actualizar Base de Datos

```bash
# Desde la raíz del proyecto
python init_db.py
```

### 3. Configurar Variables de Entorno

Añade las siguientes variables al archivo `.env` del backend:

```env
# Configuración de Scraping
SCRAPING_USER_AGENT=FosterDogs Bot 1.0
SCRAPING_DELAY=2
SCRAPING_TIMEOUT=30

# Configuración de Scheduler
SCHEDULER_ENABLED=true
DAILY_SYNC_HOUR=2
DAILY_SYNC_MINUTE=0
```

### 4. Iniciar Servicios

```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm start
```

## 📖 Guía de Uso

### Para Administradores

1. **Gestión de Solicitudes de Perreras:**

   - Accede al panel de administración (`/admin`)
   - Revisa las solicitudes pendientes
   - Aprueba o rechaza con notas explicativas
2. **Configuración de Perreras Externas:**

   - Usa las APIs `/api/external-shelters/` para configurar integraciones
   - Configura selectores CSS para scraping
   - Programa sincronizaciones

### Para Perreras

1. **Registro:**

   - Usa el formulario de registro de perreras (`/shelter-register`)
   - Proporciona información completa y verificable
   - Espera la aprobación del administrador
2. **Gestión de Perros:**

   - Una vez aprobado, accede a "Añadir Perro"
   - Completa toda la información del formulario
   - Edita o elimina tus propios anuncios

### Para Usuarios

1. **Búsqueda Mejorada:**
   - La página de perros ahora incluye perros de fuentes externas
   - Filtros por raza, tamaño, ubicación
   - Indicadores visuales para diferenciar fuentes

## 🔧 Configuración de Scraping

### Ejemplo de Configuración para Web Scraping:

```json
{
  "listing_url": "https://ejemplo-perrera.com/perros",
  "dog_url_selector": "a.dog-link",
  "selectors": {
    "name": "h1.dog-name",
    "breed": ".breed",
    "age": ".age",
    "size": ".size",
    "gender": ".gender",
    "description": ".description",
    "photos": "img.photo"
  }
}
```

### Ejemplo de Configuración para API:

```json
{
  "headers": {
    "Authorization": "Bearer token_here",
    "User-Agent": "FosterDogs Bot"
  },
  "field_mapping": {
    "id": "dog_id",
    "name": "dog_name",
    "breed": "breed_name",
    "age": "age_months",
    "photos": "image_urls"
  }
}
```

## 🔒 Seguridad

- **Autenticación**: Solo usuarios autenticados pueden gestionar perros
- **Autorización**: Roles específicos para diferentes funcionalidades
- **Validación**: Formularios con validación completa
- **Rate Limiting**: Delays entre requests de scraping
- **Error Handling**: Manejo robusto de errores en integraciones

## 📊 Monitoreo

### Logs de Sincronización:

- Revisa logs de sincronización en el backend
- Estado de cada perrera externa
- Estadísticas de perros encontrados/actualizados

### Panel de Administración:

- Estado general de todas las integraciones
- Últimas sincronizaciones exitosas
- Perreras con errores

## 🚀 Próximos Pasos

1. **Implementar upload de imágenes** para formulario de perros
2. **Sistema de notificaciones** para cambios de estado
3. **Dashboard analytics** para administradores
4. **API pública** para que otras plataformas integren con FosterDogs
5. **Sistema de reviews** para perreras

## 📞 Soporte

Para reportar problemas o solicitar nuevas funcionalidades, contacta al equipo de desarrollo o crea un issue en el repositorio.

---

**¡Gracias por usar FosterDogs! 🐕❤️**
