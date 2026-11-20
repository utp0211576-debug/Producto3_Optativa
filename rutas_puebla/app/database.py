"""
Módulo de conexión a la base de datos Redis Cloud.

Carga las variables de entorno desde `.env`, inicializa el cliente global
de Redis con decodificación automática a texto (UTF-8) y provee una función
de diagnóstico para verificar el estado de la conexión.
"""

import os
import redis
from dotenv import load_dotenv

# Cargar variables de entorno definidas en el archivo .env
load_dotenv()

# Inicializar cliente global de Redis a partir de la URL de conexión
redis_client = redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True
)


def probar_conexion() -> bool:
    """Verifica si la conexión con el servidor de Redis está activa.

    Envía un comando `PING` al servidor configurado.

    Returns:
        bool: `True` si Redis responde correctamente; `False` si ocurre algún error.
    """
    try:
        return redis_client.ping()
    except Exception:
        return False