"""
Punto de entrada principal de la aplicación Rutas Puebla (FastAPI + Redis Cloud).

Configura la instancia de FastAPI, habilita CORS, monta los archivos estáticos
del frontend interactivo (HTML/CSS/JS con Leaflet) y expone las rutas base
de inicio y monitoreo de salud de Redis.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import router
from app.database import probar_conexion

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Rutas Puebla",
    description="CRUD de paradas de transporte público en Puebla con Redis Cloud",
    version="1.1.0"
)

# Configuración de CORS para permitir peticiones desde clientes externos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Registro de rutas de la API (/paradas) y carpeta de recursos estáticos
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", summary="Interfaz principal web")
def inicio() -> FileResponse:
    """Sirve la página principal del frontend interactivo (`static/index.html`)."""
    return FileResponse("static/index.html")


@app.get("/estado", summary="Verificar estado del servicio y Redis")
def estado() -> dict:
    """Retorna el estado operativo de la aplicación y la conexión a Redis Cloud."""
    return {
        "proyecto": "Rutas Puebla",
        "redis_conectado": probar_conexion()
    }