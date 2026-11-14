from controller.experimento_controller import ExperimentoController
from model.configuracion_experimento import ConfiguracionExperimento
from model.estimador_pi import EstimadorPi
from model.generador_congruencial import GeneradorCongruencial
from view.consola_view import ConsolaView


def main() -> None:
    configuraciones = [
        ConfiguracionExperimento(n=n, semilla=12345)
        for n in (1_000, 10_000, 100_000, 1_000_000)
    ]
    controlador = ExperimentoController(
        EstimadorPi(), ConsolaView(), GeneradorCongruencial,
    )
    controlador.ejecutar(configuraciones)


if __name__ == "__main__":
    main()
