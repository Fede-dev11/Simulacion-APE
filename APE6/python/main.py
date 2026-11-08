from pathlib import Path

from controller.controlador import Controlador
from model.chi_cuadrado import ChiCuadrado
from model.configuracion import Configuracion
from model.generador_lcg import GeneradorLCG
from model.kolmogorov_smirnov import KolmogorovSmirnov
from storage.exportador_csv import ExportadorCSV
from views.consola import VistaConsola
from views.graficas import VistaGraficas


def main() -> None:
    # Parámetros propuestos y configurables; no son valores obligatorios de la guía.
    configuracion = Configuracion()
    controlador = Controlador(
        generador=GeneradorLCG(),
        pruebas=[
            ChiCuadrado(configuracion.k, configuracion.alfa),
            KolmogorovSmirnov(configuracion.alfa),
        ],
        consola=VistaConsola(),
        graficas=VistaGraficas(),
        exportador=ExportadorCSV(Path(__file__).parent / "resultados"),
    )
    controlador.ejecutar(configuracion)


if __name__ == "__main__":
    main()

