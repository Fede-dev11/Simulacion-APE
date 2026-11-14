class GeneradorCongruencial:
    """Mismo algoritmo, parámetros y orden de actualización que en Java."""

    MODULO = 2**32
    MULTIPLICADOR = 1_664_525
    INCREMENTO = 1_013_904_223

    def __init__(self, semilla: int) -> None:
        if type(semilla) is not int or not 0 <= semilla < self.MODULO:
            raise ValueError("La semilla debe ser un entero con 0 <= semilla < 2^32.")
        self._estado = semilla

    def siguiente_double(self) -> float:
        self._estado = (
            self.MULTIPLICADOR * self._estado + self.INCREMENTO
        ) % self.MODULO
        return self._estado / float(self.MODULO)
