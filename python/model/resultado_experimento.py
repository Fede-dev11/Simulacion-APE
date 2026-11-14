from dataclasses import dataclass, replace


@dataclass(frozen=True)
class ResultadoExperimento:
    n: int
    semilla: int
    nc: int
    pi_estimado: float
    error_absoluto: float
    tiempo_segundos: float = 0.0

    def con_tiempo(self, segundos: float) -> "ResultadoExperimento":
        return replace(self, tiempo_segundos=segundos)
