from model.configuracion_experimento import ConfiguracionExperimento
from model.generador_aleatorio import GeneradorAleatorio
from model.resultado_experimento import ResultadoExperimento
import math


class EstimadorPi:
    def estimar(
        self, configuracion: ConfiguracionExperimento, generador: GeneradorAleatorio
    ) -> ResultadoExperimento:
        nc = 0
        for _ in range(configuracion.n):
            x = generador.siguiente_double()
            y = generador.siguiente_double()
            if x * x + y * y <= 1.0:
                nc += 1
        pi_estimado = 4.0 * nc / configuracion.n
        return ResultadoExperimento(
            configuracion.n, configuracion.semilla, nc, pi_estimado,
            abs(pi_estimado - math.pi),
        )
