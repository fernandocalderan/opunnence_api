from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users

# Ensure database tables exist on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Opunnence API",
    description="Backend con FastAPI + PostgreSQL + SQLAlchemy",
    version="2.0.0",
)

# Register route modules
app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/")
def home():
    return {"message": "Welcome to Opunnence API 🚀", "status": "online"}


@app.get("/health")
def health_check():
    return {"health": "✅ healthy"}
