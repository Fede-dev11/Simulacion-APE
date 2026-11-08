import csv
import platform
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path

from model.configuracion import Configuracion
from model.generador_lcg import DatoGenerado
from model.resultado_prueba import ResultadoPrueba


class ExportadorCSV:
    def __init__(self, directorio: Path) -> None:
        self.directorio = directorio

    def exportar(
        self,
        configuracion: Configuracion,
        datos: list[DatoGenerado],
        resultados: list[ResultadoPrueba],
    ) -> list[Path]:
        self.directorio.mkdir(parents=True, exist_ok=True)
        rutas = [
            self._configuracion(configuracion),
            self._secuencia(datos),
            self._frecuencias(resultados[0]),
            self._resultados(resultados),
            self._versiones(),
        ]
        return rutas

    def _configuracion(self, configuracion: Configuracion) -> Path:
        ruta = self.directorio / "configuracion.csv"
        with ruta.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["parametro", "valor"])
            escritor.writerows(asdict(configuracion).items())
        return ruta

    def _versiones(self) -> Path:
        ruta = self.directorio / "versiones.txt"
        ruta.write_text(
            "\n".join(
                [
                    f"Python {platform.python_version()}",
                    f"SciPy {version('scipy')}",
                    f"Matplotlib {version('matplotlib')}",
                    "Chi-cuadrado: scipy.stats.chi2.sf(estadistico, gl)",
                    "KS bilateral asintótico: scipy.stats.kstwobign.sf(sqrt(N) * D)",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        return ruta

    def _secuencia(self, datos: list[DatoGenerado]) -> Path:
        ruta = self.directorio / "secuencia.csv"
        with ruta.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["indice", "estado", "valor_normalizado"])
            for dato in datos:
                escritor.writerow([dato.indice, dato.estado, format(dato.valor, ".17g")])
        return ruta

    def _frecuencias(self, resultado: ResultadoPrueba) -> Path:
        ruta = self.directorio / "frecuencias_chi_cuadrado.csv"
        with ruta.open("w", newline="", encoding="utf-8") as archivo:
            campos = ["inferior", "superior", "observada", "esperada", "contribucion"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(resultado.detalles["intervalos"])
        return ruta

    def _resultados(self, resultados: list[ResultadoPrueba]) -> Path:
        ruta = self.directorio / "resultados_pruebas.csv"
        with ruta.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["prueba", "estadistico", "valor_p", "decision", "d_mas", "d_menos", "gl"])
            for resultado in resultados:
                escritor.writerow(
                    [
                        resultado.nombre,
                        format(resultado.estadistico, ".17g"),
                        format(resultado.valor_p, ".17g"),
                        resultado.decision,
                        resultado.detalles.get("d_mas", ""),
                        resultado.detalles.get("d_menos", ""),
                        resultado.detalles.get("grados_libertad", ""),
                    ]
                )
        return ruta

