from math import sqrt

from scipy.stats import kstwobign

from model.resultado_prueba import ResultadoPrueba


class KolmogorovSmirnov:
    def __init__(self, alfa: float) -> None:
        self.alfa = alfa

    def evaluar(self, secuencia: list[float]) -> ResultadoPrueba:
        if not secuencia:
            raise ValueError("La secuencia no puede estar vacía")
        if any(valor < 0 or valor > 1 for valor in secuencia):
            raise ValueError("Todos los valores deben pertenecer a [0, 1]")

        ordenada = sorted(secuencia)
        n = len(ordenada)
        diferencias_positivas = [i / n - valor for i, valor in enumerate(ordenada, 1)]
        diferencias_negativas = [valor - (i - 1) / n for i, valor in enumerate(ordenada, 1)]
        d_mas = max(diferencias_positivas)
        d_menos = max(diferencias_negativas)
        estadistico = max(d_mas, d_menos)
        # Método asintótico bilateral, compartido con la implementación Java.
        valor_p = float(kstwobign.sf(sqrt(n) * estadistico))
        decision = "se rechaza H0" if valor_p < self.alfa else "no se rechaza H0"
        return ResultadoPrueba(
            "Kolmogorov-Smirnov",
            estadistico,
            valor_p,
            decision,
            {"d_mas": d_mas, "d_menos": d_menos, "n": n, "ordenada": ordenada},
        )

