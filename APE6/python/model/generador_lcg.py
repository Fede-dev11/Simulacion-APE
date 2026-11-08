from dataclasses import dataclass

from model.configuracion import Configuracion


@dataclass(frozen=True)
class DatoGenerado:
    indice: int
    estado: int
    valor: float


class GeneradorLCG:
    def generar(self, configuracion: Configuracion) -> list[DatoGenerado]:
        configuracion.validar()
        estado = configuracion.semilla
        datos: list[DatoGenerado] = []
        for indice in range(1, configuracion.n + 1):
            estado = (configuracion.a * estado + configuracion.c) % configuracion.m
            datos.append(DatoGenerado(indice, estado, estado / configuracion.m))
        return datos

