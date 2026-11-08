from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ResultadoPrueba:
    nombre: str
    estadistico: float
    valor_p: float
    decision: str
    detalles: dict[str, Any]

