from collections.abc import Callable
from time import perf_counter

from model.configuracion_experimento import ConfiguracionExperimento
from model.estimador_pi import EstimadorPi
from model.generador_aleatorio import GeneradorAleatorio
from model.resultado_experimento import ResultadoExperimento
from view.consola_view import ConsolaView


class ExperimentoController:
    def __init__(
        self,
        estimador: EstimadorPi,
        vista: ConsolaView,
        crear_generador: Callable[[int], GeneradorAleatorio],
    ) -> None:
        self._estimador = estimador
        self._vista = vista
        self._crear_generador = crear_generador

    def ejecutar(
        self, configuraciones: list[ConfiguracionExperimento]
    ) -> list[ResultadoExperimento]:
        if not configuraciones:
            raise ValueError("Debe existir al menos una configuración.")
        # Mismo procedimiento que Java: una simulación con la muestra mayor.
        calentamiento = max(configuraciones, key=lambda c: c.n)
        self._estimador.estimar(
            calentamiento, self._crear_generador(calentamiento.semilla)
        )
        resultados = []
        for configuracion in configuraciones:
            generador = self._crear_generador(configuracion.semilla)
            inicio = perf_counter()
            resultado = self._estimador.estimar(configuracion, generador)
            duracion = perf_counter() - inicio
            resultados.append(resultado.con_tiempo(duracion))
        self._vista.mostrar_resultados(resultados)
        return resultados
