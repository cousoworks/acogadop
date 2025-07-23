from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.core.config import settings
from app.routers import auth, dogs, fosters, search, shelters, external_shelters
from app.services.scheduler import scheduler_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler_service.start()
    yield
    # Shutdown
    scheduler_service.stop()

app = FastAPI(
    title="FosterDogs API",
    description="API para la plataforma de acogida y adopción de perros",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://frontend:3000",
]

if settings.CORS_ORIGINS:
    origins.extend(settings.CORS_ORIGINS.split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(dogs.router, prefix="/dogs", tags=["dogs"])
app.include_router(fosters.router, prefix="/fosters", tags=["fosters"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(shelters.router, prefix="/api", tags=["shelters"])
app.include_router(external_shelters.router, prefix="/api", tags=["external_shelters"])

@app.get("/")
async def root():
    return {"message": "FosterDogs API is running! 🐕"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}