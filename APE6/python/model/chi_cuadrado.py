from scipy.stats import chi2

from model.resultado_prueba import ResultadoPrueba


class ChiCuadrado:
    def __init__(self, k: int, alfa: float) -> None:
        self.k = k
        self.alfa = alfa

    def evaluar(self, secuencia: list[float]) -> ResultadoPrueba:
        if not secuencia:
            raise ValueError("La secuencia no puede estar vacía")
        if self.k <= 1:
            raise ValueError("k debe ser mayor que 1")
        if any(valor < 0 or valor >= 1 for valor in secuencia):
            raise ValueError("Todos los valores deben pertenecer a [0, 1)")

        n = len(secuencia)
        esperada = n / self.k
        if esperada < 5:
            raise ValueError("E < 5: aumente N o reduzca k antes de aplicar Chi-cuadrado")

        observadas = [0] * self.k
        for valor in secuencia:
            indice = min(int(valor * self.k), self.k - 1)
            observadas[indice] += 1

        contribuciones = [((observada - esperada) ** 2) / esperada for observada in observadas]
        estadistico = sum(contribuciones)
        grados_libertad = self.k - 1
        valor_p = float(chi2.sf(estadistico, grados_libertad))
        decision = "se rechaza H0" if valor_p < self.alfa else "no se rechaza H0"
        intervalos = [
            {
                "inferior": i / self.k,
                "superior": (i + 1) / self.k,
                "observada": observadas[i],
                "esperada": esperada,
                "contribucion": contribuciones[i],
            }
            for i in range(self.k)
        ]
        return ResultadoPrueba(
            "Chi-cuadrado",
            estadistico,
            valor_p,
            decision,
            {"grados_libertad": grados_libertad, "intervalos": intervalos},
        )

