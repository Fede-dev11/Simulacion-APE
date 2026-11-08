from dataclasses import dataclass


@dataclass(frozen=True)
class Configuracion:
    """Parámetros explícitos de una ejecución del generador LCG."""

    n: int = 10_000
    semilla: int = 12_345
    a: int = 1_664_525
    c: int = 1_013_904_223
    m: int = 2**32
    k: int = 10
    alfa: float = 0.05

    def validar(self) -> None:
        enteros = {
            "N": self.n,
            "semilla": self.semilla,
            "a": self.a,
            "c": self.c,
            "m": self.m,
            "k": self.k,
        }
        for nombre, valor in enteros.items():
            if isinstance(valor, bool) or not isinstance(valor, int):
                raise ValueError(f"{nombre} debe ser un entero")
        if self.n <= 0:
            raise ValueError("N debe ser positivo")
        if self.m <= 1:
            raise ValueError("m debe ser mayor que 1")
        if self.k <= 1:
            raise ValueError("k debe ser mayor que 1")
        for nombre, valor in (("semilla", self.semilla), ("a", self.a), ("c", self.c)):
            if not 0 <= valor < self.m:
                raise ValueError(f"{nombre} debe cumplir 0 <= {nombre} < m")
        if isinstance(self.alfa, bool) or not isinstance(self.alfa, (int, float)):
            raise ValueError("alfa debe ser numérico")
        if not 0 < self.alfa < 1:
            raise ValueError("alfa debe estar entre 0 y 1")

