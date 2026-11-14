from typing import Protocol


class GeneradorAleatorio(Protocol):
    def siguiente_double(self) -> float:
        """Actualiza el estado y devuelve un valor finito en [0, 1)."""
        ...
