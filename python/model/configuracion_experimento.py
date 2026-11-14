from dataclasses import dataclass


@dataclass(frozen=True)
class ConfiguracionExperimento:
    n: int
    semilla: int

    def __post_init__(self) -> None:
        if type(self.n) is not int or self.n <= 0:
            raise ValueError("N debe ser un entero positivo.")
        if type(self.semilla) is not int or not 0 <= self.semilla < 2**32:
            raise ValueError("La semilla debe ser un entero con 0 <= semilla < 2^32.")
