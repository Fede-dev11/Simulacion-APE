from pathlib import Path

from model.configuracion import Configuracion
from model.generador_lcg import GeneradorLCG
from model.prueba_estadistica import PruebaEstadistica
from storage.exportador_csv import ExportadorCSV
from views.consola import VistaConsola
from views.graficas import VistaGraficas


class Controlador:
    def __init__(
        self,
        generador: GeneradorLCG,
        pruebas: list[PruebaEstadistica],
        consola: VistaConsola,
        graficas: VistaGraficas,
        exportador: ExportadorCSV,
    ) -> None:
        self.generador = generador
        self.pruebas = pruebas
        self.consola = consola
        self.graficas = graficas
        self.exportador = exportador

    def ejecutar(self, configuracion: Configuracion) -> None:
        configuracion.validar()
        datos = self.generador.generar(configuracion)
        secuencia = [dato.valor for dato in datos]
        resultados = [prueba.evaluar(secuencia) for prueba in self.pruebas]

        self.consola.mostrar_configuracion(configuracion)
        self.consola.mostrar_secuencia(datos)
        for resultado in resultados:
            self.consola.mostrar_resultado(resultado)

        archivos = self.exportador.exportar(configuracion, datos, resultados)
        archivos += self.graficas.guardar(secuencia, configuracion.k, self.exportador.directorio)
        self.consola.mostrar_archivos([str(archivo) for archivo in archivos])

