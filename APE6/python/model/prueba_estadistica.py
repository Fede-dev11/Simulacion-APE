from typing import Protocol

from model.resultado_prueba import ResultadoPrueba


class PruebaEstadistica(Protocol):
    def evaluar(self, secuencia: list[float]) -> ResultadoPrueba: ...

