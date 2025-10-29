from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

# Importar módulos internos
from app import models, schemas
from app.database import Base, engine, get_db

# Crear las tablas automáticamente
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación
app = FastAPI(
    title="Opunnence API",
    description="Backend unificado con frontend estático para Opunnence",
    version="2.1.0"
)

# --- 💠 RUTAS DE API --- #

@app.get("/health")
def health_check():
    """Verifica el estado general del backend."""
    return {"health": "✅ OK", "database": str(engine.url)}

@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Obtiene todos los usuarios de la base de datos."""
    users = db.query(models.User).all()
    return users

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario."""
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado.")
    new_user = models.User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# --- 🌐 FRONTEND --- #

# Montar la carpeta estática
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
else:
    print("⚠️ Carpeta frontend no encontrada. Asegúrate de tener /frontend/index.html")

# Servir el index.html en la raíz
@app.get("/", include_in_schema=False)
def serve_home():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend no disponible. Verifica tu carpeta /frontend."}


# --- 🧠 ENDPOINT DE INFORMACIÓN GENERAL --- #

@app.get("/info")
def info():
    """Información básica del proyecto."""
    return {
        "app": "Opunnence API + Frontend",
        "version": "2.1.0",
        "frontend_dir": os.path.abspath(frontend_dir),
        "status": "online"
    }


# --- 🔹 EJECUCIÓN LOCAL --- #
# Solo para pruebas locales: `python app/main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
