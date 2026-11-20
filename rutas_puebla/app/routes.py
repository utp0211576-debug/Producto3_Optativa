"""
Definición de endpoints REST para el CRUD de paradas de transporte público.

Gestiona el almacenamiento, consulta, actualización y eliminación de objetos
JSON serializados dentro de Redis bajo el patrón de claves `parada:{id}`.
"""

import json
from fastapi import APIRouter, HTTPException
from app.models import Parada
from app.database import redis_client

router = APIRouter(prefix="/paradas", tags=["Paradas"])


@router.post("/", status_code=201, summary="Crear nueva parada")
def crear_parada(parada: Parada) -> dict:
    """Registra una nueva parada en Redis si su ID no existe previamente.

    Args:
        parada (Parada): Objeto validado con los datos de la parada.

    Raises:
        HTTPException: 409 Conflict si ya existe una parada con el mismo ID.

    Returns:
        dict: Mensaje de confirmación e ID de la parada creada.
    """
    clave = f"parada:{parada.id}"
    if redis_client.exists(clave):
        raise HTTPException(status_code=409, detail="La parada ya existe")

    redis_client.set(clave, parada.model_dump_json())
    return {"mensaje": "Parada creada", "id": parada.id}


@router.get("/", summary="Listar todas las paradas")
def listar_paradas() -> dict:
    """Recupera todas las paradas almacenadas en Redis mediante escaneo de claves.

    Returns:
        dict: Total de registros encontrados y lista de paradas deserializadas.
    """
    claves = redis_client.scan_iter(match="parada:*")
    paradas = []
    for clave in claves:
        datos = redis_client.get(clave)
        if datos:
            paradas.append(json.loads(datos))

    return {"total": len(paradas), "paradas": paradas}


@router.get("/{parada_id}", summary="Obtener parada por ID")
def obtener_parada(parada_id: str) -> dict:
    """Consulta los datos de una parada específica mediante su identificador.

    Args:
        parada_id (str): Identificador único de la parada (ej. `pue-1a2b3c4d`).

    Raises:
        HTTPException: 404 Not Found si la clave no existe en Redis.

    Returns:
        dict: Diccionario con los datos completos de la parada.
    """
    clave = f"parada:{parada_id}"
    datos = redis_client.get(clave)
    if not datos:
        raise HTTPException(status_code=404, detail="Parada no encontrada")

    return json.loads(datos)


@router.put("/{parada_id}", summary="Actualizar parada existente")
def actualizar_parada(parada_id: str, parada: Parada) -> dict:
    """Reemplaza los datos de una parada existente manteniendo su ID original.

    Args:
        parada_id (str): Identificador de la parada a modificar.
        parada (Parada): Nuevos datos validados de la parada.

    Raises:
        HTTPException: 404 Not Found si la parada no existe en Redis.

    Returns:
        dict: Mensaje de confirmación y objeto actualizado.
    """
    clave = f"parada:{parada_id}"
    if not redis_client.exists(clave):
        raise HTTPException(status_code=404, detail="Parada no encontrada")

    parada.id = parada_id
    redis_client.set(clave, parada.model_dump_json())
    return {"mensaje": "Parada actualizada", "parada": parada}


@router.delete("/{parada_id}", summary="Eliminar parada")
def eliminar_parada(parada_id: str) -> dict:
    """Elimina permanentemente una parada de Redis.

    Args:
        parada_id (str): Identificador de la parada a eliminar.

    Raises:
        HTTPException: 404 Not Found si la parada no existe en Redis.

    Returns:
        dict: Mensaje de confirmación e ID eliminado.
    """
    clave = f"parada:{parada_id}"
    if not redis_client.exists(clave):
        raise HTTPException(status_code=404, detail="Parada no encontrada")

    redis_client.delete(clave)
    return {"mensaje": "Parada eliminada", "id": parada_id}