"""
Modelos de validación de datos (Pydantic) para las paradas de transporte público.

Define la estructura, tipos de datos y valores por defecto que debe cumplir
cada parada antes de ser serializada y almacenada en Redis.
"""

from datetime import datetime, timezone
from typing import List
import uuid
from pydantic import BaseModel, Field


class Parada(BaseModel):
    """Modelo que representa una parada de transporte público en Puebla."""

    id: str = Field(
        default_factory=lambda: f"pue-{uuid.uuid4().hex[:8]}",
        description="Identificador único autogenerado con prefijo 'pue-'."
    )
    nombre: str = Field(
        description="Nombre descriptivo o referencia de la parada (ej. Parada Zócalo)."
    )
    colonia: str = Field(
        description="Colonia o barrio donde se ubica la parada."
    )
    municipio: str = Field(
        default="Puebla",
        description="Municipio de ubicación (por defecto 'Puebla')."
    )
    latitud: float = Field(
        description="Coordenada geográfica de latitud."
    )
    longitud: float = Field(
        description="Coordenada geográfica de longitud."
    )
    rutas: List[str] = Field(
        default=[],
        description="Lista de líneas o rutas de transporte que pasan por esta parada."
    )
    activa: bool = Field(
        default=True,
        description="Indica si la parada se encuentra actualmente en operación."
    )
    creado_en: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Marca de tiempo UTC de creación del registro."
    )