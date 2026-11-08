from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class LCGParameters:
    multiplier: int = 1_664_525
    increment: int = 1_013_904_223
    modulus: int = 2**32


class NumberGenerator(ABC):
    """Strategy used by the controller to generate a sequence."""

    @abstractmethod
    def generate(self, seed: int, count: int) -> list[tuple[int, float]]:
        raise NotImplementedError


class LinearCongruentialGenerator(NumberGenerator):
    def __init__(self, parameters: LCGParameters | None = None) -> None:
        self.parameters = parameters or LCGParameters()

    def generate(self, seed: int, count: int) -> list[tuple[int, float]]:
        if count < 0:
            raise ValueError("La cantidad no puede ser negativa")

        p = self.parameters
        state = seed % p.modulus
        sequence: list[tuple[int, float]] = []
        for _ in range(count):
            state = (p.multiplier * state + p.increment) % p.modulus
            sequence.append((state, state / p.modulus))
        return sequence

    def has_full_period(self) -> bool:
        """Hull-Dobell specialized for m=2^32."""
        p = self.parameters
        return p.increment % 2 == 1 and (p.multiplier - 1) % 4 == 0
